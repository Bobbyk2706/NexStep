from __future__ import annotations

"""
Deterministic relevance filtering for parsed document sections.

This module does NOT call an AI provider.

Its job is to reduce a large official notification to the sections
that are potentially useful for downstream extraction.

The source document remains the authority.
This module only decides which sections deserve further processing.
"""

from dataclasses import dataclass
import re
from typing import Iterable

from app.ai.document_models import DocumentSection, SectionedDocument


@dataclass(frozen=True, slots=True)
class SectionRelevance:
    section_id: str
    title: str
    score: float
    relevant: bool
    reasons: tuple[str, ...]
    page_numbers: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class RelevantSectionSet:
    sections: tuple[DocumentSection, ...]
    decisions: tuple[SectionRelevance, ...]

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def page_numbers(self) -> list[int]:
        pages: set[int] = set()

        for section in self.sections:
            pages.update(section.page_numbers)

        return sorted(pages)


# ---------------------------------------------------------------------------
# Positive title signals
# ---------------------------------------------------------------------------
#
# These are deliberately broad at this stage.
#
# The purpose is NOT to perfectly understand the section.
# The purpose is to avoid sending irrelevant pages to an LLM.
#

_STRONG_TITLE_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "eligibility",
        (
            "eligibility",
            "eligible",
            "who can apply",
            "qualification criteria",
            "eligibility criteria",
        ),
    ),
    (
        "dates",
        (
            "important dates",
            "key dates",
            "schedule",
            "application dates",
            "exam dates",
            "date",
        ),
    ),
    (
        "application",
        (
            "application process",
            "online application",
            "apply",
            "registration",
            "application fee",
            "fee",
            "application form",
        ),
    ),
    (
        "documents",
        (
            "supporting documents",
            "documents required",
            "required documents",
            "photograph",
            "signature",
            "certificate",
            "proof",
        ),
    ),
    (
        "exam",
        (
            "examination",
            "exam pattern",
            "test pattern",
            "types of questions",
            "marking scheme",
            "question paper",
            "test paper",
            "syllabus",
        ),
    ),
    (
        "results",
        (
            "result",
            "results",
            "scorecard",
            "score",
            "cutoff",
            "rank",
        ),
    ),
    (
        "admit_card",
        (
            "admit card",
            "hall ticket",
            "call letter",
        ),
    ),
    (
        "special_support",
        (
            "pwd",
            "persons with disability",
            "scribe",
            "reservation",
            "category",
            "relaxation",
        ),
    ),
    (
        "overview",
        (
            "highlights",
            "about gate",
            "about the examination",
            "general information",
            "introduction",
            "preamble",
        ),
    ),
)


# ---------------------------------------------------------------------------
# Negative title signals
# ---------------------------------------------------------------------------

_NEGATIVE_TITLE_PATTERNS = (
    re.compile(r"\bapplication\s+form\b", re.I),
    re.compile(r"\bdeclaration\b", re.I),
    re.compile(r"\bundertaking\b", re.I),
    re.compile(r"\bcertificate\b.*\bto\s+be\s+filled\b", re.I),
    re.compile(r"\bfor\s+office\s+use\b", re.I),
    re.compile(r"\bdo\s+hereby\s+undertake\b", re.I),
    re.compile(r"\bthis\s+is\s+to\s+certify\b", re.I),
)


# ---------------------------------------------------------------------------
# Negative content signals
# ---------------------------------------------------------------------------

_NEGATIVE_TEXT_PATTERNS = (
    re.compile(r"\bMr\.?/Ms\.?/Mrs\.?\b", re.I),
    re.compile(r"\bI\s+hereby\s+(certify|declare|undertake)\b", re.I),
    re.compile(r"\bSignature\s+of\b", re.I),
    re.compile(r"\bName\s+of\s+the\s+candidate\b", re.I),
    re.compile(r"\bAffix\b.*\bphotograph\b", re.I),
)


_MAX_UNSIGNALLED_CHARS = 50_000


def _normalise(value: str) -> str:
    """
    Normalise whitespace and casing for deterministic matching.
    """
    return " ".join(value.lower().split())


def _title_signals(title: str) -> list[tuple[str, float]]:
    """
    Return positive signals found in a section title.
    """
    normalized = _normalise(title)

    signals: list[tuple[str, float]] = []

    for group, phrases in _STRONG_TITLE_GROUPS:
        for phrase in phrases:
            if phrase in normalized:
                signals.append(
                    (
                        f"title:{group}",
                        3.0,
                    )
                )
                break

    return signals


def _negative_signals(
    section: DocumentSection,
) -> list[tuple[str, float]]:
    """
    Detect sections that look like forms, declarations,
    certificates, or other non-informational material.
    """
    title = section.title.strip()
    text = section.text

    signals: list[tuple[str, float]] = []

    for pattern in _NEGATIVE_TITLE_PATTERNS:
        if pattern.search(title):
            signals.append(
                (
                    f"negative-title:{pattern.pattern}",
                    -6.0,
                )
            )

    # Only inspect the beginning of a section for template/form signals.
    # This avoids unnecessary processing of extremely large sections.
    prefix = text[:8_000]

    for pattern in _NEGATIVE_TEXT_PATTERNS:
        if pattern.search(prefix):
            signals.append(
                (
                    f"negative-text:{pattern.pattern}",
                    -2.5,
                )
            )

    if section.character_count > _MAX_UNSIGNALLED_CHARS:
        signals.append(
            (
                "very-large-section",
                -1.5,
            )
        )

    return signals


def score_section(
    section: DocumentSection,
) -> SectionRelevance:
    """
    Score one section using deterministic signals only.

    Positive signals:
        +3.0  semantic title group
        +1.5  eligibility content
        +1.0  fee/payment content
        +1.0  qualification content
        +1.0  application content
        +1.0  result content
        +0.75 exam/question content
        +0.5  date/schedule content

    Negative signals:
        -6.0  obvious form/declaration title
        -2.5  form/declaration content
        -1.5  unusually large unsignalled section

    A section is normally retained at >= 2.5.
    """

    title = _normalise(section.title)
    text = section.text

    positive_signals = _title_signals(section.title)
    negative_signals = _negative_signals(section)

    score = sum(
        weight
        for _, weight in positive_signals
    )

    score += sum(
        weight
        for _, weight in negative_signals
    )

    # -----------------------------------------------------------------------
    # Content-level signals
    # -----------------------------------------------------------------------

    content_checks = (
        (
            "content:eligibility",
            r"\beligib(?:le|ility)\b",
            1.5,
        ),
        (
            "content:date",
            r"\b(?:date|deadline|schedule|2027)\b",
            0.5,
        ),
        (
            "content:fee",
            r"\b(?:fee|fees|payment)\b",
            1.0,
        ),
        (
            "content:qualification",
            r"\b(?:degree|qualification|graduat|diploma)\b",
            1.0,
        ),
        (
            "content:application",
            r"\b(?:apply|application|registration)\b",
            1.0,
        ),
        (
            "content:exam",
            r"\b(?:examination|exam|question|marking)\b",
            0.75,
        ),
        (
            "content:result",
            r"\b(?:result|scorecard|score|rank)\b",
            1.0,
        ),
    )

    lower_text = text.lower()

    for reason, pattern, weight in content_checks:
        if re.search(pattern, lower_text):
            positive_signals.append(
                (
                    reason,
                    weight,
                )
            )

            score += weight

    # -----------------------------------------------------------------------
    # Overview sections
    # -----------------------------------------------------------------------

    if any(
        token in title
        for token in (
            "highlight",
            "overview",
            "preamble",
        )
    ):
        score = max(
            score,
            2.5,
        )

        positive_signals.append(
            (
                "overview-section",
                1.0,
            )
        )

    # -----------------------------------------------------------------------
    # Decide relevance
    # -----------------------------------------------------------------------

    hard_negative = any(
        weight <= -6.0
        for _, weight in negative_signals
    )

    positive_groups = {
        reason.split(":", 1)[1]
        for reason, _ in positive_signals
        if reason.startswith("title:")
    }

    # Obvious forms/templates should not survive merely because
    # they contain words such as "application" or "certificate".
    if hard_negative:
        relevant = False
    else:
        relevant = score >= 2.5

    # -----------------------------------------------------------------------
    # Clamp score so downstream consumers have predictable values.
    # -----------------------------------------------------------------------

    score = round(
        max(
            -10.0,
            min(
                score,
                15.0,
            ),
        ),
        2,
    )

    reasons = tuple(
        reason
        for reason, _ in (
            *positive_signals,
            *negative_signals,
        )
    )

    return SectionRelevance(
        section_id=section.section_id,
        title=section.title,
        score=score,
        relevant=relevant,
        reasons=reasons,
        page_numbers=tuple(section.page_numbers),
    )


def rank_section_relevance(
    document: SectionedDocument,
) -> list[SectionRelevance]:
    """
    Score every section and return the results ranked by relevance.

    Higher scores come first.
    Page number is used as a deterministic tie-breaker.
    """

    decisions = [
        score_section(section)
        for section in document.sections
    ]

    return sorted(
        decisions,
        key=lambda item: (
            -item.score,
            item.page_numbers[0]
            if item.page_numbers
            else 10**9,
        ),
    )


def select_relevant_sections(
    document: SectionedDocument,
    *,
    min_score: float = 2.5,
    max_sections: int = 20,
) -> RelevantSectionSet:
    """
    Select the relevant sections from a SectionedDocument.

    Selection is capped so a noisy document cannot accidentally
    send hundreds of sections downstream.
    """

    if min_score < 0:
        raise ValueError(
            "min_score must be non-negative."
        )

    if max_sections <= 0:
        raise ValueError(
            "max_sections must be greater than zero."
        )

    all_decisions = rank_section_relevance(
        document
    )

    selected_ids = {
        decision.section_id
        for decision in all_decisions
        if decision.relevant
        and decision.score >= min_score
    }

    selected = [
        section
        for section in document.sections
        if section.section_id in selected_ids
    ]

    # Restore document order.
    selected.sort(
        key=lambda section: (
            section.start_page
            if section.start_page is not None
            else 10**9,
            section.section_id,
        )
    )

    selected = selected[:max_sections]

    return RelevantSectionSet(
        sections=tuple(selected),
        decisions=tuple(all_decisions),
    )


def filter_relevant_sections(
    sections: Iterable[DocumentSection],
    *,
    min_score: float = 2.5,
    max_sections: int = 20,
) -> RelevantSectionSet:
    """
    Convenience function for callers that already have a list
    of DocumentSection objects instead of a SectionedDocument.
    """

    section_list = list(sections)

    if not section_list:
        return RelevantSectionSet(
            sections=tuple(),
            decisions=tuple(),
        )

    if min_score < 0:
        raise ValueError(
            "min_score must be non-negative."
        )

    if max_sections <= 0:
        raise ValueError(
            "max_sections must be greater than zero."
        )

    decisions = [
        score_section(section)
        for section in section_list
    ]

    ranked = sorted(
        decisions,
        key=lambda item: (
            -item.score,
            item.page_numbers[0]
            if item.page_numbers
            else 10**9,
        ),
    )

    selected_ids = {
        item.section_id
        for item in ranked
        if item.relevant
        and item.score >= min_score
    }

    selected = [
        section
        for section in section_list
        if section.section_id in selected_ids
    ]

    selected.sort(
        key=lambda section: (
            section.start_page
            if section.start_page is not None
            else 10**9,
            section.section_id,
        )
    )

    return RelevantSectionSet(
        sections=tuple(
            selected[:max_sections]
        ),
        decisions=tuple(ranked),
    )