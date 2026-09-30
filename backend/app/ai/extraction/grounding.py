from __future__ import annotations

"""
Grounding: nothing the model says is trusted until it is found in the
source document. Quotes are located in the passages (with page numbers
and section), and dates must exist somewhere in the document.
"""

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date

from app.ai.aggregated_extraction_result import (
    ConflictOption,
    ExtractionConflict,
    ExtractionIssue,
)
from app.ai.extraction.dates import date_set, find_dates
from app.ai.extraction.structure import Passage
from app.ai.extraction_evidence import ExtractionEvidence


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").lower()
    text = re.sub(r"[\u2010-\u2015\-]+", "-", text)
    text = re.sub(r"[\"'“”‘’`•*_#\[\]|]+", " ", text)
    text = re.sub(r"[^\w\s\-/.,:;()&%₹]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _words(text: str) -> list[str]:
    return re.findall(r"\w+", _norm(text))


@dataclass(slots=True)
class Location:
    passage: Passage
    exact: bool


def locate_quote(
    quote: str | None,
    cited: str | None,
    passages: dict[str, Passage],
) -> Location | None:
    """Find the passage a quote comes from (cited passage first)."""

    if not quote or len(_norm(quote)) < 4:
        return None

    needle = _norm(quote)
    order = ([cited] if cited in passages else []) + [
        pid for pid in passages if pid != cited
    ]

    for pid in order:
        if needle in _norm(passages[pid].text):
            return Location(passages[pid], True)

    # Fuzzy: nearly all words of the quote occur in one passage. Tolerates
    # the model dropping a hyphen, table separator or line break.
    words = set(_words(quote))
    if len(words) >= 3:
        best, best_ratio = None, 0.0
        for pid in order:
            have = set(_words(passages[pid].text))
            ratio = len(words & have) / len(words)
            if ratio > best_ratio:
                best, best_ratio = passages[pid], ratio
        if best is not None and best_ratio >= 0.85:
            return Location(best, False)

    return None


@dataclass
class Grounder:
    """Collects evidence, issues and conflicts while facts are checked."""

    passages: dict[str, Passage]
    doc_dates: set[date]
    evidence: list[ExtractionEvidence] = field(default_factory=list)
    issues: list[ExtractionIssue] = field(default_factory=list)
    conflicts: list[ExtractionConflict] = field(default_factory=list)

    # --- issues -------------------------------------------------------

    def issue(self, severity: str, code: str, message: str, field_name: str | None = None) -> None:
        self.issues.append(
            ExtractionIssue(severity=severity, code=code, field=field_name, message=message)
        )

    def conflict(
        self,
        field_name: str,
        options: list[ConflictOption],
        chosen: str | None,
        reason: str,
    ) -> None:
        self.conflicts.append(
            ExtractionConflict(field=field_name, options=options, chosen=chosen, reason=reason)
        )

    # --- evidence -----------------------------------------------------

    def support(
        self,
        label: str,
        quote: str | None,
        cited: str | None,
        *,
        required: bool = True,
    ) -> bool:
        """
        Record evidence for `label`. Returns True when the quote was
        found in the source. Unverifiable quotes still produce an entry
        (marked verified=False) so the reviewer can see the claim.
        """

        location = locate_quote(quote, cited, self.passages)

        if location is not None:
            passage = location.passage
            self.evidence.append(
                ExtractionEvidence(
                    chunk_number=int(passage.id[1:]),
                    page_numbers=passage.pages,
                    source_text=_excerpt(passage.text, quote),
                    field=label,
                    verified=True,
                    section=passage.section or None,
                )
            )
            return True

        cited_passage = self.passages.get(cited or "")
        self.evidence.append(
            ExtractionEvidence(
                chunk_number=int(cited_passage.id[1:]) if cited_passage else 0,
                page_numbers=cited_passage.pages if cited_passage else [],
                source_text=(quote or "(no supporting quote provided)")[:400],
                field=label,
                verified=False,
                section=(cited_passage.section or None) if cited_passage else None,
            )
        )

        if required:
            self.issue(
                "warning",
                "unverified-quote",
                f"{label}: the supporting quote could not be found in the document.",
                label,
            )
        return False

    # --- dates --------------------------------------------------------

    def date_is_grounded(self, value: date) -> bool:
        return value in self.doc_dates

    def quote_backs_date(self, value: date, quote: str | None) -> bool:
        """True when the quote is silent about dates or contains this one."""

        if not quote:
            return True
        mentioned = date_set(quote)
        return not mentioned or value in mentioned


def _excerpt(text: str, quote: str | None, width: int = 700) -> str:
    """The part of the passage around the quote (whole passage if short)."""

    if len(text) <= width:
        return text

    if quote:
        index = text.lower().find(quote.lower()[:40])
        if index >= 0:
            start = max(0, index - width // 3)
            return text[start : start + width]

    return text[:width]


def document_dates(pages_text: list[str]) -> set[date]:
    found: set[date] = set()
    for text in pages_text:
        found |= date_set(text)
    return found
