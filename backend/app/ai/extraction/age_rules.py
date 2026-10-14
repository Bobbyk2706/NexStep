from __future__ import annotations

"""
Deterministic age / date-of-birth helpers.

Pure Python (no pydantic, no database), so every function here can be
unit-tested on its own.

Why this module exists
----------------------

Notices word age limits in two different ways:

    "must not exceed 32 years"            -> age <= 32  (inclusive)
    "must not have attained 32 years"     -> age <= 31  (exclusive)

The LLM copies the number (32) in both cases. Treating both as
"age <= 32" gives a date-of-birth boundary that is exactly one year too
generous for the second wording (UPSC uses it). The wording is therefore
read from the quoted sentence, deterministically.

Many notices also state the birth-date window outright:

    "born not earlier than 2nd August, 1993 and not later than
     1st August, 2004"

When that sentence exists it is the authority, so it is parsed here
instead of being recomputed from an age.
"""

import re
from datetime import date, timedelta

from app.ai.extraction.dates import find_dates


# ---------------------------------------------------------------------------
# Date arithmetic
# ---------------------------------------------------------------------------

def subtract_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year - years)
    except ValueError:
        # 29 February
        return d.replace(year=d.year - years, day=28)


def dob_boundary(
    kind: str,
    years: int,
    reference: date,
    *,
    exclusive: bool = False,
) -> tuple[str, date]:
    """
    Convert an age limit into a date-of-birth rule.

    Returns (operator, date) for the rule "Date of Birth <operator> date".

    kind="maximum", exclusive=False  ->  age <= N  on `reference`
        born on or after (reference - (N+1) years) + 1 day

    kind="maximum", exclusive=True   ->  age <  N  on `reference`
        born on or after (reference - N years) + 1 day

    kind="minimum", exclusive=False  ->  age >= N  on `reference`
        born on or before (reference - N years)

    kind="minimum", exclusive=True   ->  age >  N  on `reference`
        born on or before (reference - (N+1) years)
    """

    if kind == "maximum":
        effective = years - 1 if exclusive else years
        boundary = subtract_years(reference, effective + 1) + timedelta(days=1)
        return ">=", boundary

    effective = years + 1 if exclusive else years
    return "<=", subtract_years(reference, effective)


# ---------------------------------------------------------------------------
# Inclusive / exclusive wording
# ---------------------------------------------------------------------------

_MAX_EXCLUSIVE = re.compile(
    r"""
    \b(?:
        (?:must\s+|should\s+|shall\s+)?not\s+(?:have\s+|yet\s+)?
            (?:attained|completed|reached)
      | (?:have|has)\s+not\s+(?:yet\s+)?(?:attained|completed|reached)
      | below\s+(?:the\s+age\s+of\s+)?\d
      | less\s+than\s+(?:the\s+age\s+of\s+)?\d
      | under\s+(?:the\s+age\s+of\s+)?\d
      | younger\s+than\s+\d
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

_MIN_EXCLUSIVE = re.compile(
    r"\b(?:more\s+than|older\s+than|above|over)\s+(?:the\s+age\s+of\s+)?\d",
    re.IGNORECASE,
)


def is_exclusive(kind: str, quote: str | None) -> bool:
    """True when the quoted wording excludes the stated age itself."""

    if not quote:
        return False

    pattern = _MAX_EXCLUSIVE if kind == "maximum" else _MIN_EXCLUSIVE

    return bool(pattern.search(quote))


# ---------------------------------------------------------------------------
# Explicit date-of-birth windows
# ---------------------------------------------------------------------------

_EARLIEST = re.compile(
    r"(?:born\s+)?(?:not\s+earlier\s+than|on\s+or\s+after|not\s+before)\s*",
    re.IGNORECASE,
)

_LATEST = re.compile(
    r"(?:not\s+later\s+than|on\s+or\s+before|not\s+after)\s*",
    re.IGNORECASE,
)

_BORN = re.compile(r"\bborn\b", re.IGNORECASE)


def _first_date_after(text: str, position: int, reach: int = 45) -> date | None:
    window = text[position : position + reach]

    mentions = sorted(find_dates(window), key=lambda m: m.start)

    return mentions[0].value if mentions else None


def parse_explicit_dob_limits(
    text: str,
    exclude: re.Pattern[str] | None = None,
) -> dict:
    """
    Find birth-date limits written out in the notice.

    Returns
        {"earliest": (date, snippet) | None,
         "latest":   (date, snippet) | None,
         "varies":   bool}

    Only text that follows the word "born" is considered, so sentences
    such as "applications not later than 11.02.2025" are never mistaken
    for a birth-date limit.

    Some notices give different limits for different posts ("posts with an
    age limit up to 30 years: born not earlier than 02.08.1996 ...; posts
    up to 32 years: born not earlier than 02.08.1994 ..."). A candidate who
    is eligible for any post is eligible for the exam, so the most generous
    limit is returned and `varies` is set so the reviewer is told.

    `exclude` is a pattern (category words such as SC/ST/ex-servicemen);
    a "born ..." sentence that starts with one of those words describes a
    concession, not the general limit, and is skipped.
    """

    earliest: list[tuple[date, str]] = []
    latest: list[tuple[date, str]] = []

    for born in _BORN.finditer(text):
        start = born.start()

        if exclude is not None:
            lead = re.split(r"[.\n;]", text[max(0, start - 80) : start])[-1]

            if exclude.search(lead):
                continue

        window = text[start : start + 260]

        for match in _EARLIEST.finditer(window):
            found = _first_date_after(window, match.end())

            if found:
                snippet = window[: min(len(window), match.end() + 45)]
                earliest.append((found, " ".join(snippet.split())))

        for match in _LATEST.finditer(window):
            found = _first_date_after(window, match.end())

            if found:
                snippet = window[: min(len(window), match.end() + 45)]
                latest.append((found, " ".join(snippet.split())))

    varies = (
        len({d for d, _ in earliest}) > 1
        or len({d for d, _ in latest}) > 1
    )

    return {
        "earliest": min(earliest, key=lambda item: item[0]) if earliest else None,
        "latest": max(latest, key=lambda item: item[0]) if latest else None,
        "varies": varies,
    }


# ---------------------------------------------------------------------------
# "as on" reference date
# ---------------------------------------------------------------------------

_AGE_SENTENCE = re.compile(r"\bage\b|\bborn\b|\byears\b", re.IGNORECASE)

_AS_ON = re.compile(
    r"(?:as\s+on|as\s+of|reckoned\s+(?:as\s+)?on|calculated\s+(?:as\s+)?on|"
    r"counted\s+(?:as\s+)?on|on\s+the)\s*",
    re.IGNORECASE,
)


def find_age_reference_date(text: str) -> date | None:
    """
    The single date on which age is counted, when the notice states it.

    Returns None unless exactly one distinct "as on <date>" date occurs in
    sentences that talk about age, so an ambiguous document never gets a
    guessed reference date.
    """

    candidates: set[date] = set()

    for line in re.split(r"(?<=[.;])\s+|\n", text):
        if not _AGE_SENTENCE.search(line):
            continue

        for match in _AS_ON.finditer(line):
            found = _first_date_after(line, match.end(), reach=32)

            if found:
                candidates.add(found)

    return next(iter(candidates)) if len(candidates) == 1 else None