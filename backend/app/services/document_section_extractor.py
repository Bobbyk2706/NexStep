from __future__ import annotations


# Section headings that are commonly relevant to
# examination information and eligibility extraction.
_RELEVANT_SECTION_KEYWORDS = (
    "eligibility",
    "educational qualification",
    "qualification",
    "nationality",
    "age limit",
    "age",
    "application",
    "examination",
    "exam",
    "important dates",
    "dates",
    "fee",
    "experience",
    "reservation",
    "category",
    "syllabus",
    "scheme",
    "selection",
)


def extract_relevant_sections(
    text: str,
) -> str:
    """
    Extract sections that are potentially relevant to
    examination-information and eligibility processing.

    This function is a deterministic convenience helper.

    It must NOT be used as the authoritative extraction
    pipeline because filtering document text can discard
    information required by later processing.

    The full-document lossless pipeline should continue to
    use the original document text.
    """

    if not text:
        return ""

    lines = text.splitlines()

    selected: list[str] = []
    collecting = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if collecting:
                selected.append(line)
            continue

        normalized = stripped.lower()

        is_relevant_heading = any(
            keyword in normalized
            for keyword in _RELEVANT_SECTION_KEYWORDS
        )

        if is_relevant_heading:
            collecting = True

        if collecting:
            selected.append(line)

    return "\n".join(selected)