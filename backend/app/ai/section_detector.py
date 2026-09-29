from __future__ import annotations

import re
from dataclasses import dataclass

from app.ai.document_models import (
    DocumentPage,
    DocumentSection,
    ParsedDocument,
    SectionedDocument,
)


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_NUMBERED_HEADING_RE = re.compile(
    r"^\s*(\d+(?:\.\d+)*)[\.\)]?\s+(.+?)\s*$"
)

_EXPLICIT_SECTION_RE = re.compile(
    r"^\s*(SECTION|CHAPTER|PART)\s+"
    r"([A-Z0-9IVX]+(?:\.\d+)*)"
    r"[\s:.\-–—]*(.*)$",
    re.IGNORECASE,
)

_UPPERCASE_HEADING_RE = re.compile(
    r"^[A-Z][A-Z0-9&(),:/+\-–—' ]{4,100}$"
)


_NOISE_EXACT = {
    "CONTENTS",
    "TABLE OF CONTENTS",
    "PAGE",
    "PAGES",
    "INDEX",
    "ANNEXURE",
    "ANNEXURES",
    "APPENDIX",
    "APPENDICES",
}


# ---------------------------------------------------------------------------
# Internal model
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class _DetectedHeading:
    page_number: int
    title: str
    level: int | None
    confidence: float


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def _normalize_heading(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    # Remove TOC leader dots + page number.
    text = re.sub(
        r"(?:\.{2,}|…{2,}|\s{3,})\s*\d+\s*$",
        "",
        text,
    )

    text = re.sub(
        r"[.\-–—:]+$",
        "",
        text,
    ).strip()

    return text


# ---------------------------------------------------------------------------
# Noise detection
# ---------------------------------------------------------------------------

def _is_code_like(text: str) -> bool:
    """
    Examples:

        B1.2
        B2.6
        XE0.7
        XH5.11
        XL0.9
    """

    return bool(
        re.fullmatch(
            r"[A-Z]{1,4}\d+(?:\.\d+)*[:.]?",
            text.strip(),
            re.IGNORECASE,
        )
    )


def _is_bare_structural_label(text: str) -> bool:
    """
    Reject:

        Section 2
        Section 5
        Section B1.2
        Section XE0.7
        Part 2
    """

    return bool(
        re.fullmatch(
            r"(section|chapter|part)\s+"
            r"[A-Z0-9IVX]+(?:\.\d+)*",
            text.strip(),
            re.IGNORECASE,
        )
    )


def _looks_like_sentence(text: str) -> bool:
    words = text.split()

    if len(text) > 120:
        return True

    if (
        len(words) >= 8
        and text.endswith(
            (".", "?", "!")
        )
    ):
        return True

    return False


def _looks_like_noise(text: str) -> bool:
    normalized = text.strip()

    if not normalized:
        return True

    if normalized.upper() in _NOISE_EXACT:
        return True

    if not re.search(
        r"[A-Za-z]",
        normalized,
    ):
        return True

    if _is_code_like(normalized):
        return True

    if _is_bare_structural_label(normalized):
        return True

    if re.fullmatch(
        r"\d+\s*[:.)]?",
        normalized,
    ):
        return True

    return False


# ---------------------------------------------------------------------------
# Heading confidence
# ---------------------------------------------------------------------------

def _heading_confidence(
    text: str,
    *,
    numbered: bool,
    explicit_structural: bool,
    uppercase: bool,
) -> float:
    score = 0.0

    words = text.split()

    # Has meaningful alphabetic words.
    if len(words) >= 2:
        score += 0.20

    # Reasonable heading length.
    if 8 <= len(text) <= 100:
        score += 0.15

    # Explicit numbered structure is strong evidence.
    if numbered:
        score += 0.30

    # Explicit structural heading.
    if explicit_structural:
        score += 0.25

    # Uppercase-only headings are weaker.
    if uppercase:
        score += 0.05

    # Sentence-like text is weak evidence.
    if _looks_like_sentence(text):
        score -= 0.45

    # Too many digits usually means table/form content.
    digit_count = sum(
        char.isdigit()
        for char in text
    )

    if len(text) > 0:
        digit_ratio = digit_count / len(text)

        if digit_ratio > 0.30:
            score -= 0.25

    return max(
        0.0,
        min(1.0, score),
    )


# ---------------------------------------------------------------------------
# Detect heading from one line
# ---------------------------------------------------------------------------

def _detect_heading_from_line(
    line: str,
) -> tuple[str, int | None, float] | None:

    original = line.strip()

    if not original:
        return None

    normalized = _normalize_heading(
        original
    )

    if _looks_like_noise(normalized):
        return None

    # ---------------------------------------------------------------
    # Explicit SECTION / CHAPTER / PART
    # ---------------------------------------------------------------

    match = _EXPLICIT_SECTION_RE.match(
        normalized
    )

    if match:
        prefix = match.group(1)
        number = match.group(2)
        title = match.group(3).strip()

        # Bare structural labels are rejected.
        if not title:
            return None

        if _is_code_like(title):
            return None

        if len(title.split()) < 2:
            return None

        confidence = _heading_confidence(
            normalized,
            numbered=False,
            explicit_structural=True,
            uppercase=False,
        )

        if confidence < 0.50:
            return None

        return (
            normalized,
            1,
            confidence,
        )

    # ---------------------------------------------------------------
    # Numbered headings
    # ---------------------------------------------------------------

    match = _NUMBERED_HEADING_RE.match(
        normalized
    )

    if match:

        number = match.group(1)
        title = match.group(2).strip()

        level = number.count(".") + 1

        if level > 3:
            return None

        if len(title.split()) < 2:
            return None

        if _looks_like_sentence(title):
            return None

        if _is_code_like(title):
            return None

        confidence = _heading_confidence(
            normalized,
            numbered=True,
            explicit_structural=False,
            uppercase=False,
        )

        if confidence < 0.55:
            return None

        return (
            normalized,
            level,
            confidence,
        )

    # ---------------------------------------------------------------
    # Uppercase headings
    # ---------------------------------------------------------------

    if _UPPERCASE_HEADING_RE.fullmatch(
        normalized
    ):

        words = normalized.split()

        if len(words) < 2:
            return None

        confidence = _heading_confidence(
            normalized,
            numbered=False,
            explicit_structural=False,
            uppercase=True,
        )

        if confidence < 0.60:
            return None

        return (
            normalized,
            1,
            confidence,
        )

    return None


# ---------------------------------------------------------------------------
# Page heading detection
# ---------------------------------------------------------------------------

def _detect_page_headings(
    page: DocumentPage,
) -> list[_DetectedHeading]:

    headings: list[_DetectedHeading] = []

    for line in page.text.splitlines():

        detected = _detect_heading_from_line(
            line
        )

        if detected is None:
            continue

        title, level, confidence = detected

        headings.append(
            _DetectedHeading(
                page_number=page.page_number,
                title=title,
                level=level,
                confidence=confidence,
            )
        )

    return headings


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _deduplicate_headings(
    headings: list[_DetectedHeading],
) -> list[_DetectedHeading]:

    if not headings:
        return []

    result: list[_DetectedHeading] = []

    for heading in headings:

        normalized_title = re.sub(
            r"\s+",
            " ",
            heading.title.lower().strip(),
        )

        duplicate = False

        for previous in reversed(
            result[-5:]
        ):

            previous_title = re.sub(
                r"\s+",
                " ",
                previous.title.lower().strip(),
            )

            if (
                normalized_title
                == previous_title
                and abs(
                    heading.page_number
                    - previous.page_number
                )
                <= 1
            ):

                # Keep the stronger candidate.
                if (
                    heading.confidence
                    > previous.confidence
                ):
                    result[-1] = heading

                duplicate = True
                break

        if not duplicate:
            result.append(heading)

    return result


# ---------------------------------------------------------------------------
# Structural region filtering
# ---------------------------------------------------------------------------

def _filter_structural_headings(
    headings: list[_DetectedHeading],
) -> list[_DetectedHeading]:
    """
    The PDF contains several different document regions.

    We keep headings that are structurally useful for the main
    information document and discard obvious form/syllabus/table
    fragments.

    This is deliberately conservative and does NOT delete page
    content. It only prevents noisy lines from becoming section
    boundaries.
    """

    filtered: list[_DetectedHeading] = []

    for heading in headings:

        title = heading.title.strip()

        # -----------------------------------------------------------
        # Obvious form/syllabus codes
        # -----------------------------------------------------------

        if re.search(
            r"\b(?:XE|XH|XL)\d+\.\d+\b",
            title,
            re.IGNORECASE,
        ):
            continue

        # -----------------------------------------------------------
        # Obvious fragment patterns
        # -----------------------------------------------------------

        if re.fullmatch(
            r"[A-Z,\s]+",
            title,
        ):
            # Example:
            #
            # CY, DA, EY, GE, GG, MA, PH, RA
            #
            continue

        if title.startswith(
            (
                "TDS,",
                "BOD,",
                "COD",
            )
        ):
            continue

        # -----------------------------------------------------------
        # Form/certificate prose fragments
        # -----------------------------------------------------------

        if re.match(
            r"^\d+\.\s+(This certificate|I do hereby)",
            title,
            re.IGNORECASE,
        ):
            continue

        # -----------------------------------------------------------
        # Very likely syllabus/question content
        # -----------------------------------------------------------

        if re.match(
            r"^Part A consists of",
            title,
            re.IGNORECASE,
        ):
            continue

        # -----------------------------------------------------------
        # Weak uppercase candidates
        # -----------------------------------------------------------

        if (
            heading.level == 1
            and heading.confidence < 0.70
        ):
            # Keep explicitly numbered headings,
            # but reject weak generic candidates.
            if not re.match(
                r"^\d+(?:\.\d+)*[\.\)]?\s+",
                title,
            ):
                continue

        filtered.append(heading)

    return filtered


# ---------------------------------------------------------------------------
# Build sections
# ---------------------------------------------------------------------------

def _build_sections(
    document: ParsedDocument,
    headings: list[_DetectedHeading],
) -> list[DocumentSection]:

    if not headings:

        return [
            DocumentSection(
                section_id="section-001",
                title="Document",
                pages=document.pages.copy(),
                heading_level=None,
                start_page=(
                    document.pages[0].page_number
                    if document.pages
                    else None
                ),
                end_page=(
                    document.pages[-1].page_number
                    if document.pages
                    else None
                ),
                metadata={
                    "detected_heading": False,
                },
            )
        ]

    sections: list[DocumentSection] = []

    first_heading_page = headings[0].page_number

    preamble_pages = [
        page
        for page in document.pages
        if (
            page.page_number
            < first_heading_page
            and page.has_text
        )
    ]

    if preamble_pages:

        sections.append(
            DocumentSection(
                section_id="section-001",
                title="Preamble",
                pages=preamble_pages,
                heading_level=None,
                start_page=(
                    preamble_pages[0].page_number
                ),
                end_page=(
                    preamble_pages[-1].page_number
                ),
                metadata={
                    "detected_heading": False,
                },
            )
        )

    for index, heading in enumerate(
        headings
    ):

        start_page = heading.page_number

        if index + 1 < len(headings):
            end_page = (
                headings[index + 1].page_number
                - 1
            )
        else:
            end_page = (
                document.pages[-1].page_number
            )

        section_pages = [
            page
            for page in document.pages
            if (
                start_page
                <= page.page_number
                <= end_page
                and page.has_text
            )
        ]

        if not section_pages:
            continue

        sections.append(
            DocumentSection(
                section_id=(
                    f"section-"
                    f"{len(sections) + 1:03d}"
                ),
                title=heading.title,
                pages=section_pages,
                heading_level=heading.level,
                start_page=(
                    section_pages[0].page_number
                ),
                end_page=(
                    section_pages[-1].page_number
                ),
                metadata={
                    "detected_heading": True,
                    "heading_confidence": (
                        heading.confidence
                    ),
                },
            )
        )

    return sections


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_document_sections(
    document: ParsedDocument,
) -> SectionedDocument:
    """
    Detect logical document sections while preserving
    page provenance.

    The detector identifies structural candidates only.
    It does not attempt to decide whether a section is
    relevant to exam extraction.
    """

    detected_headings: list[
        _DetectedHeading
    ] = []

    for page in document.pages:

        detected_headings.extend(
            _detect_page_headings(page)
        )

    detected_headings = (
        _deduplicate_headings(
            detected_headings
        )
    )

    detected_headings = (
        _filter_structural_headings(
            detected_headings
        )
    )

    sections = _build_sections(
        document,
        detected_headings,
    )

    return SectionedDocument(
        document=document,
        sections=sections,
        metadata={
            "detected_heading_count": len(
                detected_headings
            ),
            "section_count": len(
                sections
            ),
            "detector_version": "4",
        },
    )