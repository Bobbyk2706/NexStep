from __future__ import annotations

"""
Deterministic date finder.

Used to (a) rank passages by how date-dense they are and (b) check that
a date reported by the LLM really occurs in the document. Day-first
numeric dates (Indian convention) are assumed.
"""

import re
from dataclasses import dataclass
from datetime import date

_MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7,
    "jul": 7, "august": 8, "aug": 8, "september": 9, "sep": 9,
    "sept": 9, "october": 10, "oct": 10, "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

_MONTH_RE = (
    r"(?:january|february|march|april|may|june|july|august|september|"
    r"october|november|december|jan|feb|mar|apr|jun|jul|aug|sept|sep|"
    r"oct|nov|dec)\.?"
)
_ORD = r"(?:st|nd|rd|th)?"
_DAY = rf"(\d{{1,2}}){_ORD}"
_DAY_NC = rf"\d{{1,2}}{_ORD}"

# "February 6 & 7, 2027", "Feb 6, 7 and 8, 2027", "February 6-7, 2027"
_MONTH_DAYLIST = re.compile(
    rf"\b({_MONTH_RE})\s+((?:{_DAY_NC})(?:\s*(?:,|&|and|to|-|–|—)\s*(?:{_DAY_NC}))*)"
    rf"\s*,?\s*(\d{{4}})\b",
    re.IGNORECASE,
)
# "6 & 7 February 2027", "6-7 February, 2027", "6th to 8th Feb 2027"
_DAYLIST_MONTH = re.compile(
    rf"\b((?:{_DAY_NC})(?:\s*(?:,|&|and|to|-|–|—)\s*(?:{_DAY_NC}))*)\s+"
    rf"({_MONTH_RE})\s*,?\s*(\d{{4}})\b",
    re.IGNORECASE,
)
# "Sep 22 – Sep 30, 2026", "Aug 14, 2026 to Sep 21, 2026"
_MONTH_TO_MONTH = re.compile(
    rf"\b({_MONTH_RE})\s+{_DAY}(?:\s*,?\s*(\d{{4}}))?\s*(?:to|-|–|—)\s*"
    rf"({_MONTH_RE})\s+{_DAY}\s*,?\s*(\d{{4}})\b",
    re.IGNORECASE,
)
_NUMERIC = re.compile(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4}|\d{2})\b")
_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_RANGE_SEP = re.compile(r"to|-|–|—", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class DateMention:
    value: date
    start: int
    end: int


def _month(token: str) -> int | None:
    return _MONTHS.get(token.lower().rstrip("."))


def _safe(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _expand_days(daylist: str) -> list[int]:
    """'6 & 7' -> [6, 7]; '6-8' / '6 to 8' -> [6, 7, 8]."""
    numbers = [int(n) for n in re.findall(r"\d{1,2}", daylist)]
    if len(numbers) == 2 and _RANGE_SEP.search(daylist) and numbers[0] < numbers[1] <= 31:
        return list(range(numbers[0], numbers[1] + 1))
    return numbers


def find_dates(text: str) -> list[DateMention]:
    found: list[DateMention] = []

    for m in _MONTH_DAYLIST.finditer(text):
        month, year = _month(m.group(1)), int(m.group(3))
        for day in _expand_days(m.group(2)):
            d = month and _safe(year, month, day)
            if d:
                found.append(DateMention(d, m.start(), m.end()))

    for m in _DAYLIST_MONTH.finditer(text):
        month, year = _month(m.group(2)), int(m.group(3))
        for day in _expand_days(m.group(1)):
            d = month and _safe(year, month, day)
            if d:
                found.append(DateMention(d, m.start(), m.end()))

    for m in _MONTH_TO_MONTH.finditer(text):
        year_end = int(m.group(6))
        year_start = int(m.group(3)) if m.group(3) else year_end
        for month_tok, day, year in (
            (m.group(1), m.group(2), year_start),
            (m.group(4), m.group(5), year_end),
        ):
            month = _month(month_tok)
            d = month and _safe(year, month, int(day))
            if d:
                found.append(DateMention(d, m.start(), m.end()))

    for m in _ISO.finditer(text):
        d = _safe(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if d:
            found.append(DateMention(d, m.start(), m.end()))

    for m in _NUMERIC.finditer(text):
        year = int(m.group(3))
        year += 2000 if year < 100 else 0
        d = _safe(year, int(m.group(2)), int(m.group(1)))
        if d:
            found.append(DateMention(d, m.start(), m.end()))

    return found


def date_set(text: str) -> set[date]:
    return {mention.value for mention in find_dates(text)}


def count_dates(text: str) -> int:
    return len(find_dates(text))
