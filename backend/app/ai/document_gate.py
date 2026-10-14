from __future__ import annotations

"""
Decide whether a downloaded PDF is the exam's notification at all.

Discovery used to check only the file name, the link text and whether the
exam's name occurred in the first two pages. That accepts documents that
carry the right name but are not a notification:

    * a yearly calendar ("PROGRAMME OF EXAMINATIONS ... - 2027")
    * an "examination schedule" notice
    * admit-card, city-intimation, result and answer-key notices
    * last year's notification, when this year's is not yet published

Rejecting these makes discovery try the next candidate and, when there is
none, report NOT_FOUND, which is the honest answer for an exam whose
notification has not been published.

Pure Python (no pydantic, no database), so it can be unit-tested directly.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    ok: bool
    reason: str = ""


# Headline wording of documents that are about an exam but are not the
# notification that sets out who may apply.
_NON_NOTIFICATION_HEADING = re.compile(
    r"""
    \b(?:
        programme\s+of\s+examinations?
      | calendar
      | examination\s+schedule
      | exam\s+schedule
      | schedule\s+of\s+(?:the\s+)?(?:examination|exam)s?
      | tentative\s+schedule
      | admit\s+card
      | hall\s+ticket
      | intimation\s+slip
      | city\s+intimation
      | answer\s+key
      | provisional\s+answer
      | final\s+result
      | result\s+of
      | cut-?\s?off\s+marks
      | merit\s+list
      | scorecard
    )\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

_ELIGIBILITY_WORDING = re.compile(
    r"\beligib\w*|\bage\s+limit|\beducational\s+qualification|"
    r"\bnationality\b|\bcitizen|\bqualifying\s+examination|"
    r"\bminimum\s+qualification",
    re.IGNORECASE,
)

_YEAR = re.compile(r"(?<!\d)(20\d{2})(?!\d)")

# How much of the document is read for the heading and for the year.
_HEADING_CHARS = 400
_YEAR_CHARS = 6000


def classify_document(
    pages: list[str],
    exam_name: str = "",
) -> GateResult:
    """
    pages: the text of each page, in order (empty strings for scanned pages).

    Returns GateResult(ok=False, reason=...) only when it is fairly sure
    the document is not the notification. When there is not enough text to
    tell (a scanned PDF), the document is let through, because the
    extraction step reports that problem itself.
    """

    text = "\n".join(page or "" for page in pages)

    if len(text.strip()) < 300:
        return GateResult(True)

    first_page = (pages[0] if pages else "") or ""

    heading = " ".join(first_page.split())[:_HEADING_CHARS]

    match = _NON_NOTIFICATION_HEADING.search(heading)

    if match:
        return GateResult(
            False,
            "the document heading says it is a "
            f"'{match.group(0).lower()}' document, not a notification",
        )

    if len(_ELIGIBILITY_WORDING.findall(text)) < 2:
        return GateResult(
            False,
            "the document has no eligibility section (age limit, "
            "qualification, nationality), so it is not the notification",
        )

    wanted = set(_YEAR.findall(exam_name or ""))

    if wanted:
        found = set(_YEAR.findall(text[:_YEAR_CHARS]))

        if found and not (found & wanted):
            return GateResult(
                False,
                "the document is for "
                f"{', '.join(sorted(found))}, not {', '.join(sorted(wanted))}; "
                "this year's notification may not be published yet",
            )

    return GateResult(True)
