from __future__ import annotations

"""
Grounding: nothing the model says is trusted until it is found in the
source document.

Quotes are located in passages with page numbers and section.
Dates must exist somewhere in the document.
Extracted values can additionally be checked against their supporting quote.
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

    text = re.sub(
        r"""["'“”‘’`•*_#\[\]|]+""",
        " ",
        text,
    )

    text = re.sub(
        r"[^\w\s\-/.,:;()&%₹]",
        " ",
        text,
    )

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
    """Find the passage a quote comes from, checking the cited passage first."""

    if not quote or len(_norm(quote)) < 4:
        return None

    needle = _norm(quote)

    order = (
        ([cited] if cited in passages else [])
        + [pid for pid in passages if pid != cited]
    )

    # Exact normalized match.
    for pid in order:
        if needle in _norm(passages[pid].text):
            return Location(passages[pid], True)

    # Fuzzy match.
    #
    # This tolerates small formatting differences such as:
    # - line breaks
    # - hyphen differences
    # - table separators
    words = set(_words(quote))

    if len(words) >= 3:
        best = None
        best_ratio = 0.0

        for pid in order:
            have = set(_words(passages[pid].text))

            if not words:
                continue

            ratio = len(words & have) / len(words)

            if ratio > best_ratio:
                best = passages[pid]
                best_ratio = ratio

        if best is not None and best_ratio >= 0.85:
            return Location(best, False)

    return None


@dataclass
class Grounder:
    """Collect evidence, issues and conflicts while facts are checked."""

    passages: dict[str, Passage]
    doc_dates: set[date]

    evidence: list[ExtractionEvidence] = field(default_factory=list)
    issues: list[ExtractionIssue] = field(default_factory=list)
    conflicts: list[ExtractionConflict] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Issues
    # ------------------------------------------------------------------

    def issue(
        self,
        severity: str,
        code: str,
        message: str,
        field_name: str | None = None,
    ) -> None:
        self.issues.append(
            ExtractionIssue(
                severity=severity,
                code=code,
                field=field_name,
                message=message,
            )
        )

    def conflict(
        self,
        field_name: str,
        options: list[ConflictOption],
        chosen: str | None,
        reason: str,
    ) -> None:
        self.conflicts.append(
            ExtractionConflict(
                field=field_name,
                options=options,
                chosen=chosen,
                reason=reason,
            )
        )

    # ------------------------------------------------------------------
    # Evidence
    # ------------------------------------------------------------------

    def support(
        self,
        label: str,
        quote: str | None,
        cited: str | None,
        *,
        required: bool = True,
    ) -> bool:
        """
        Record evidence for `label`.

        Returns True when the quote was found in the source.

        Unverifiable quotes still produce an evidence entry marked
        verified=False so the reviewer can see the claim.
        """

        location = locate_quote(
            quote,
            cited,
            self.passages,
        )

        if location is not None:
            passage = location.passage

            self.evidence.append(
                ExtractionEvidence(
                    chunk_number=int(passage.id[1:]),
                    page_numbers=passage.pages,
                    source_text=_excerpt(
                        passage.text,
                        quote,
                    ),
                    field=label,
                    verified=True,
                    section=passage.section or None,
                )
            )

            return True

        cited_passage = self.passages.get(cited or "")

        self.evidence.append(
            ExtractionEvidence(
                chunk_number=(
                    int(cited_passage.id[1:])
                    if cited_passage
                    else 0
                ),
                page_numbers=(
                    cited_passage.pages
                    if cited_passage
                    else []
                ),
                source_text=(
                    quote or "(no supporting quote provided)"
                )[:400],
                field=label,
                verified=False,
                section=(
                    cited_passage.section or None
                    if cited_passage
                    else None
                ),
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

    # ------------------------------------------------------------------
    # Value grounding
    # ------------------------------------------------------------------

    def value_backs_quote(
        self,
        value: str | None,
        quote: str | None,
    ) -> bool:
        """
        Check whether an extracted value is supported by its quote.

        This is intentionally conservative.

        The value is accepted when:

        1. There is no value, because there is nothing to validate.
        2. There is no quote, because the caller may perform another
           grounding check separately.
        3. The normalized value occurs directly in the quote.
        4. A substantial proportion of the value's words occurs in the
           quote, while important numeric tokens must also agree.

        This method does not attempt to perform semantic reasoning.
        The LLM is still responsible for proposing the fact; this method
        only checks whether the evidence is compatible with that proposal.
        """

        if not value:
            return True

        if not quote:
            return True

        normalized_value = _norm(value)
        normalized_quote = _norm(quote)

        if not normalized_value:
            return True

        # Strongest case: exact normalized value occurs in the quote.
        if normalized_value in normalized_quote:
            return True

        value_words = _words(value)
        quote_words = set(_words(quote))

        if not value_words:
            return True

        # Every numeric token in the extracted value must appear in the
        # quote. This prevents cases such as:
        #
        #   value = "GATE 2027"
        #   quote = "GATE 2026"
        #
        # from passing through fuzzy matching.
        value_numbers = {
            token
            for token in value_words
            if any(char.isdigit() for char in token)
        }

        quote_numbers = {
            token
            for token in quote_words
            if any(char.isdigit() for char in token)
        }

        if value_numbers and not value_numbers.issubset(quote_numbers):
            return False

        # For multi-word values, require a strong lexical overlap.
        matched = sum(
            1
            for word in value_words
            if word in quote_words
        )

        ratio = matched / len(value_words)

        return ratio >= 0.85

    # ------------------------------------------------------------------
    # Dates
    # ------------------------------------------------------------------

    def date_is_grounded(self, value: date) -> bool:
        return value in self.doc_dates

    def quote_backs_date(
        self,
        value: date,
        quote: str | None,
    ) -> bool:
        """
        True when the quote is silent about dates or contains this date.

        A quote with no detectable date is treated as silent because some
        evidence may support a fact indirectly or through surrounding
        document context.
        """

        if not quote:
            return True

        mentioned = date_set(quote)

        return not mentioned or value in mentioned


def _excerpt(
    text: str,
    quote: str | None,
    width: int = 700,
) -> str:
    """Return the part of the passage around the quote."""

    if len(text) <= width:
        return text

    if quote:
        index = text.lower().find(
            quote.lower()[:40]
        )

        if index >= 0:
            start = max(
                0,
                index - width // 3,
            )

            return text[start:start + width]

    return text[:width]


def document_dates(
    pages_text: list[str],
) -> set[date]:
    found: set[date] = set()

    for text in pages_text:
        found |= date_set(text)

    return found