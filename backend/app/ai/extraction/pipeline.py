from __future__ import annotations

"""
Extraction pipeline v2 - the single entry point used by every workflow
(discovery, admin retry, monitoring, main pipeline).

    PDF -> parse -> passages -> retrieve per topic -> LLM facts
        -> ground in source -> compile rules -> normalize -> validate
"""

import os
import time
from pathlib import Path
from typing import Any

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
    ExtractionIssue,
)
from app.ai.complete_extraction_normalizer import normalize_complete_extraction
from app.ai.complete_extraction_validation import validate_complete_extraction
from app.ai.document_models import ParsedDocument
from app.ai.exam_schemas import EligibilityInformation, ExamInformation
from app.ai.extraction import compiler, facts
from app.ai.extraction.grounding import Grounder, document_dates
from app.ai.extraction.llm import call_structured
from app.ai.extraction.parsing import add_tables_to_pages, parse_pdf
from app.ai.extraction.retrieval import (
    ContextPack,
    Facet,
    build_index,
    facets_from_feedback,
    retrieve,
)
from app.ai.extraction.structure import build_passages
from app.ai.extraction_schemas import CompleteExtractionData
from app.ai.eligibility_schemas import EligibilityRulesData
from app.ai.provider_manager import AIProviderManager, AllAIProvidersFailedError
from app.ai.token_budget import estimate_tokens

PIPELINE_VERSION = "2.0"

# Output tokens reserved per topic (counted against the TPM budget).
_MAX_OUTPUT = {Facet.IDENTITY: 500, Facet.DATES: 1000, Facet.ELIGIBILITY: 1500}

_TASKS = {
    Facet.IDENTITY: (facts.IDENTITY_TASK, facts.IdentityDraft),
    Facet.DATES: (facts.DATES_TASK, facts.DatesDraft),
    Facet.ELIGIBILITY: (facts.ELIGIBILITY_TASK, facts.EligibilityDraft),
}


class ExtractionError(ValueError):
    """The document could not be turned into a usable extraction."""


_default_manager: AIProviderManager | None = None


def default_manager() -> AIProviderManager:
    global _default_manager
    if _default_manager is None:
        _default_manager = AIProviderManager()
    return _default_manager


def _request_budget(manager: AIProviderManager) -> int:
    ceiling = int(os.getenv("NEXSTEP_MAX_REQUEST_TOKENS", "7000"))
    capacity = manager.request_capacity()
    return min(ceiling, capacity - 200) if capacity else ceiling


def _context_budget(facet: Facet, request_budget: int) -> int:
    task, model = _TASKS[facet]
    overhead = estimate_tokens(
        facts.build_messages(task, "", None),
        facts.inline_schema(model),
    )
    return max(800, request_budget - overhead - _MAX_OUTPUT[facet] - 250)


def run_extraction(
    source: bytes | bytearray | str | os.PathLike | ParsedDocument,
    *,
    exam_name_hint: str | None = None,
    admin_feedback: str | None = None,
    manager: AIProviderManager | None = None,
    source_url: str = "",
    document_hash: str = "",
) -> AggregatedExtractionResult:
    started = time.monotonic()
    manager = manager or default_manager()

    # ---- 1. parse ------------------------------------------------------
    if isinstance(source, ParsedDocument):
        document, pdf_source = source, None
    else:
        document = parse_pdf(source, source_url=source_url, document_hash=document_hash)
        pdf_source = source

    if document.character_count < 200:
        raise ExtractionError("The document contains no extractable text (it may be a scanned image).")

    issues: list[ExtractionIssue] = []
    scanned = document.metadata.get("scanned_pages", [])
    if scanned and len(scanned) / max(1, document.page_count) > 0.25:
        issues.append(
            ExtractionIssue(
                severity="error",
                code="scanned-document",
                message=f"{len(scanned)} of {document.page_count} pages have no text layer (scanned); "
                "their content could not be read.",
            )
        )

    # ---- 2. passages + first retrieval to learn which pages matter -------
    request_budget = _request_budget(manager)
    budgets = {f: _context_budget(f, request_budget) for f in Facet}
    focus = facets_from_feedback(admin_feedback)

    def feedback_for(facet: Facet) -> str | None:
        return admin_feedback if (not focus or facet in focus) else None

    def select() -> dict[Facet, ContextPack]:
        passages = build_passages(document)
        index = build_index(passages)
        return {
            f: retrieve(passages, f, token_budget=budgets[f], feedback=feedback_for(f), index=index)
            for f in Facet
        }

    packs = select()

    # ---- 3. render tables only on the pages actually needed ------------------
    if pdf_source is not None:
        wanted = sorted({p for pack in packs.values() for p in pack.pages})
        if add_tables_to_pages(document, pdf_source, wanted):
            packs = select()

    all_passages = {p.id: p for pack in packs.values() for p in pack.passages}
    grounder = Grounder(
        passages=all_passages,
        doc_dates=document_dates([p.text for p in document.pages]),
        issues=issues,
    )

    # ---- 4. LLM: one small call per topic --------------------------------
    drafts: dict[Facet, Any] = {}
    calls: list[dict[str, Any]] = []

    for facet in Facet:
        pack = packs[facet]
        task, model = _TASKS[facet]

        if not pack.passages:
            grounder.issue("error", "no-context", f"No text relevant to '{facet.value}' was found in the document.")
            continue

        context = pack.text
        if facet is Facet.IDENTITY and document.metadata.get("running_header"):
            context = f"[Running page header: {document.metadata['running_header']}]\n\n" + context

        try:
            draft, record = call_structured(
                manager,
                facet=facet.value,
                task=task,
                context=context,
                model_cls=model,
                feedback=feedback_for(facet),
                max_tokens=_MAX_OUTPUT[facet],
            )
            drafts[facet] = draft
            calls.append(
                {
                    "facet": facet.value,
                    "provider": record.provider,
                    "estimated_tokens": record.est_tokens,
                    "corrective_retry": record.corrective_retry,
                    "attempts": record.attempts,
                }
            )
        except AllAIProvidersFailedError as error:
            grounder.issue("error", "ai-failed", f"AI extraction of '{facet.value}' failed: {str(error)[:300]}")
            calls.append({"facet": facet.value, "provider": None, "error": str(error)[:300]})

    if not drafts:
        raise ExtractionError("AI extraction failed for every topic: " + "; ".join(i.message for i in issues))

    # ---- 5. compile ------------------------------------------------------------
    identity: facts.IdentityDraft | None = drafts.get(Facet.IDENTITY)
    exam_name = conducting_body = release_date = None

    if identity is not None:
        exam_name = (identity.exam_name.value or "").strip() or None
        conducting_body = (identity.conducting_body.value or "").strip() or None
        if exam_name:
            grounder.support("Exam name", identity.exam_name.quote, identity.exam_name.passage)
        if conducting_body:
            grounder.support("Conducting body", identity.conducting_body.quote, identity.conducting_body.passage)
        parsed_release = compiler.iso(identity.release_date.value)
        if parsed_release and grounder.date_is_grounded(parsed_release):
            release_date = parsed_release.isoformat()
            grounder.support("Release date", identity.release_date.quote, identity.release_date.passage)
        elif identity.release_date.value:
            grounder.issue("warning", "date-not-in-document", "Release date is not written in the document; left empty.", "Release date")

    if not exam_name and exam_name_hint:
        exam_name = exam_name_hint.strip()
        grounder.issue("warning", "name-from-admin", "The exam name was not found in the document; the administrator's entry was used.", "Exam name")

    date_fields = {"application_start_date": None, "application_end_date": None, "exam_dates": []}
    if Facet.DATES in drafts:
        tba = "to be announced" in packs[Facet.DATES].text.lower() or " tba" in packs[Facet.DATES].text.lower()
        date_fields = compiler.compile_dates(drafts[Facet.DATES], grounder, tba)

    eligibility_info = EligibilityInformation()
    rules = EligibilityRulesData()
    if Facet.ELIGIBILITY in drafts:
        eligibility_info, rules = compiler.compile_eligibility(
            drafts[Facet.ELIGIBILITY], grounder, packs[Facet.ELIGIBILITY].text
        )

    extraction = CompleteExtractionData(
        exam_information=ExamInformation(
            exam_name=exam_name,
            conducting_body=conducting_body,
            release_date=release_date,
            eligibility=eligibility_info,
            **date_fields,
        ),
        eligibility_rules=rules,
    )

    # ---- 6. normalize + validate (same gates as approval) ---------------------------
    try:
        extraction = normalize_complete_extraction(extraction)
    except Exception as error:
        grounder.issue("error", "normalization", f"Normalization failed: {error}")

    for message in validate_complete_extraction(extraction):
        grounder.issue("error", "validation", message)

    # ---- 7. reviewer context -----------------------------------------------------
    superseded = document.metadata.get("superseded_text", [])
    if superseded:
        sample = "; ".join(f"'{s['text']}' (p.{s['page']})" for s in superseded[:4])
        grounder.issue(
            "info",
            "superseded-ignored",
            f"{len(superseded)} struck-out (superseded) values in the document were ignored, e.g. {sample}.",
        )

    result = AggregatedExtractionResult(
        extraction=extraction,
        evidence=grounder.evidence,
        conflicts=grounder.conflicts,
        issues=_dedupe(grounder.issues),
        pipeline={
            "version": PIPELINE_VERSION,
            "parser": document.metadata.get("parser"),
            "pages": document.page_count,
            "characters": document.character_count,
            "request_budget_tokens": request_budget,
            "feedback_used": bool(admin_feedback),
            "seconds": round(time.monotonic() - started, 1),
            "topics": {
                f.value: {"pages": packs[f].pages, "context_tokens": packs[f].tokens, "passages": len(packs[f].passages)}
                for f in Facet
            },
            "calls": calls,
        },
    )
    return result


def ensure_usable(result: AggregatedExtractionResult) -> None:
    """Raise ExtractionError when there is nothing worth showing a reviewer."""

    info = result.extraction.exam_information
    has_content = bool(info.exam_name) and (
        info.exam_dates
        or info.application_end_date
        or result.extraction.eligibility_rules.rule_groups
    )
    if not has_content:
        raise ExtractionError(
            "The extraction found no usable exam information: "
            + "; ".join(i.message for i in result.issues if i.severity == "error")[:600]
        )


def summarize(result: AggregatedExtractionResult) -> str:
    """Deterministic plain-language summary (no LLM, so it cannot drift)."""

    info = result.extraction.exam_information
    parts = [f"{info.exam_name or 'Exam'}" + (f" conducted by {info.conducting_body}" if info.conducting_body else "") + "."]
    if info.application_start_date or info.application_end_date:
        parts.append(
            f"Applications: {info.application_start_date or 'start date not announced'} to {info.application_end_date or 'unknown'}."
        )
    if info.exam_dates:
        parts.append("Exam: " + ", ".join(
            r.start_date if r.start_date == r.end_date else f"{r.start_date} to {r.end_date}" for r in info.exam_dates
        ) + ".")
    n_rules = sum(len(g.rules) + sum(len(c.rules) for c in g.child_groups) for g in result.extraction.eligibility_rules.rule_groups)
    parts.append(f"{n_rules} eligibility rule(s) extracted.")
    if result.blocking_issues:
        parts.append(f"{len(result.blocking_issues)} issue(s) need review before approval.")
    return " ".join(parts)


def _dedupe(issues: list[ExtractionIssue]) -> list[ExtractionIssue]:
    seen, out = set(), []
    for issue in issues:
        key = (issue.severity, issue.code, issue.message)
        if key not in seen:
            seen.add(key)
            out.append(issue)
    order = {"error": 0, "warning": 1, "info": 2}
    return sorted(out, key=lambda i: order[i.severity])
