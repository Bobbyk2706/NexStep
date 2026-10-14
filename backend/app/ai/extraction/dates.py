from __future__ import annotations

"""
Deterministic date finder.

Used to:
1. rank passages by how date-dense they are, and
2. verify that dates reported by the LLM actually occur in the document.

Day-first numeric dates are assumed for ambiguous numeric formats,
which matches the Indian convention used by NexStep.

Examples supported:

    6 February 2027
    February 6, 2027
    6th February 2027
    1st of August, 2025
    February 6 & 7, 2027
    6 & 7 February 2027
    February 6-8, 2027
    6-8 February 2027
    Sep 22 - Sep 30, 2026
    Aug 14, 2026 to Sep 21, 2026
    06/02/2027
    06-02-2027
    06.02.2027
    2027-02-06
"""

import re
from dataclasses import dataclass
from datetime import date


_MONTHS = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "sept": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}


_MONTH = (
    r"(?:"
    r"january|february|march|april|may|june|july|august|"
    r"september|october|november|december|"
    r"jan|feb|mar|apr|jun|jul|aug|sept|sep|oct|nov|dec"
    r")"
)

_ORDINAL = r"(?:st|nd|rd|th)?"

_DAY = rf"(\d{{1,2}}){_ORDINAL}"
_DAY_NC = rf"\d{{1,2}}{_ORDINAL}"


# ---------------------------------------------------------------------------
# Month + day list
#
# Examples:
#   February 6 & 7, 2027
#   Feb 6, 7 and 8, 2027
#   February 6-7, 2027
#   February 6 to 8, 2027
# ---------------------------------------------------------------------------

_MONTH_DAYLIST = re.compile(
    rf"\b({_MONTH})\s+"
    rf"({_DAY_NC}"
    rf"(?:\s*(?:,|&|and|to|-|–|—)\s*{_DAY_NC})*)"
    rf"\s*,?\s*(\d{{4}})\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Day list + month
#
# Examples:
#   6 & 7 February 2027
#   6-7 February, 2027
#   6th to 8th Feb 2027
# ---------------------------------------------------------------------------

_DAYLIST_MONTH = re.compile(
    rf"\b("
    rf"{_DAY_NC}"
    rf"(?:\s*(?:,|&|and|to|-|–|—)\s*{_DAY_NC})*"
    rf")\s+(?:of\s+)?"
    rf"({_MONTH})\s*,?\s*(\d{{4}})\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Month-to-month ranges
#
# Examples:
#   Sep 22 - Sep 30, 2026
#   Aug 14, 2026 to Sep 21, 2026
# ---------------------------------------------------------------------------

_MONTH_TO_MONTH = re.compile(
    rf"\b"
    rf"({_MONTH})\s+{_DAY}"
    rf"(?:\s*,?\s*(\d{{4}}))?"
    rf"\s*(?:to|-|–|—)\s*"
    rf"({_MONTH})\s+{_DAY}"
    rf"\s*,?\s*(\d{{4}})"
    rf"\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Numeric dates
#
# Indian/day-first interpretation:
#
#   06/02/2027 -> 6 February 2027
#   06-02-2027 -> 6 February 2027
#   06.02.2027 -> 6 February 2027
#
# Two-digit years are interpreted as 2000-2099.
# ---------------------------------------------------------------------------

_NUMERIC = re.compile(
    r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2}|\d{4})\b"
)


# ---------------------------------------------------------------------------
# ISO dates
# ---------------------------------------------------------------------------

_ISO = re.compile(
    r"\b(\d{4})-(\d{2})-(\d{2})\b"
)


# ---------------------------------------------------------------------------
# Range separators used when expanding day lists
# ---------------------------------------------------------------------------

_RANGE_SEP = re.compile(
    r"\b(?:to)\b|[-–—]",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class DateMention:
    value: date
    start: int
    end: int


def _month(token: str) -> int | None:
    return _MONTHS.get(
        token.lower().rstrip(".")
    )


def _safe(
    year: int,
    month: int,
    day: int,
) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _expand_days(daylist: str) -> list[int]:
    """
    Expand a day list.

    Examples:

        "6 & 7"  -> [6, 7]
        "6, 7, 8" -> [6, 7, 8]
        "6-8"    -> [6, 7, 8]
        "6 to 8" -> [6, 7, 8]
    """

    numbers = [
        int(number)
        for number in re.findall(
            r"\d{1,2}",
            daylist,
        )
    ]

    if (
        len(numbers) == 2
        and _RANGE_SEP.search(daylist)
        and numbers[0] < numbers[1] <= 31
    ):
        return list(
            range(
                numbers[0],
                numbers[1] + 1,
            )
        )

    return numbers


def _year(value: int) -> int:
    """
    Convert a two-digit year to the 2000s.
    """

    if value < 100:
        return 2000 + value

    return value


def find_dates(text: str) -> list[DateMention]:
    """
    Find all recognizable dates in text.

    Invalid calendar dates are silently ignored.
    """

    found: list[DateMention] = []

    # ---------------------------------------------------------------
    # Month followed by day list
    # ---------------------------------------------------------------

    for match in _MONTH_DAYLIST.finditer(text):
        month = _month(match.group(1))
        year = int(match.group(3))

        if month is None:
            continue

        for day in _expand_days(match.group(2)):
            parsed = _safe(
                year,
                month,
                day,
            )

            if parsed is not None:
                found.append(
                    DateMention(
                        parsed,
                        match.start(),
                        match.end(),
                    )
                )

    # ---------------------------------------------------------------
    # Day list followed by month
    # ---------------------------------------------------------------

    for match in _DAYLIST_MONTH.finditer(text):
        month = _month(match.group(2))
        year = int(match.group(3))

        if month is None:
            continue

        for day in _expand_days(match.group(1)):
            parsed = _safe(
                year,
                month,
                day,
            )

            if parsed is not None:
                found.append(
                    DateMention(
                        parsed,
                        match.start(),
                        match.end(),
                    )
                )

    # ---------------------------------------------------------------
    # Month-to-month ranges
    # ---------------------------------------------------------------

    for match in _MONTH_TO_MONTH.finditer(text):
        start_month_token = match.group(1)
        start_day = int(match.group(2))
        start_year = (
            int(match.group(3))
            if match.group(3)
            else int(match.group(6))
        )

        end_month_token = match.group(4)
        end_day = int(match.group(5))
        end_year = int(match.group(6))

        start_month = _month(start_month_token)
        end_month = _month(end_month_token)

        if start_month is not None:
            parsed = _safe(
                start_year,
                start_month,
                start_day,
            )

            if parsed is not None:
                found.append(
                    DateMention(
                        parsed,
                        match.start(),
                        match.end(),
                    )
                )

        if end_month is not None:
            parsed = _safe(
                end_year,
                end_month,
                end_day,
            )

            if parsed is not None:
                found.append(
                    DateMention(
                        parsed,
                        match.start(),
                        match.end(),
                    )
                )

    # ---------------------------------------------------------------
    # ISO
    # ---------------------------------------------------------------

    for match in _ISO.finditer(text):
        parsed = _safe(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )

        if parsed is not None:
            found.append(
                DateMention(
                    parsed,
                    match.start(),
                    match.end(),
                )
            )

    # ---------------------------------------------------------------
    # Numeric day-first dates
    # ---------------------------------------------------------------

    for match in _NUMERIC.finditer(text):
        parsed = _safe(
            _year(int(match.group(3))),
            int(match.group(2)),
            int(match.group(1)),
        )

        if parsed is not None:
            found.append(
                DateMention(
                    parsed,
                    match.start(),
                    match.end(),
                )
            )

    return found


def date_set(text: str) -> set[date]:
    """
    Return unique dates found in text.
    """

    return {
        mention.value
        for mention in find_dates(text)
    }


def count_dates(text: str) -> int:
    """
    Return the number of date mentions found in text.
    """

    return len(
        find_dates(text)
    )