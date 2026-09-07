import re
from datetime import datetime
def extract_exam_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    candidates = []

    for index, line in enumerate(lines[:40]):

        lower = line.lower()

        if len(line) < 5 or len(line) > 150:
            continue

        score = 0

        if "examination" in lower:
            score += 4

        elif "exam" in lower:
            score += 3

        if any(char.isdigit() for char in line):
            score += 1

        if line.isupper():
            score += 2

        if index < 10:
            score += 2

        if any(
            word in lower
            for word in [
                "commission",
                "department",
                "university",
                "government"
            ]
        ):
            score -= 2

        candidates.append((score, line))

    if not candidates:
        return None

    candidates.sort(
        key=lambda candidate: candidate[0],
        reverse=True
    )

    return candidates[0][1]
import re


def extract_dates(text):

    months = (
        r"(?:January|Jan|February|Feb|March|Mar|April|Apr|May|"
        r"June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|"
        r"November|Nov|December|Dec)"
    )

    day_month_year = (
        rf"\d{{1,2}}(?:st|nd|rd|th)?\s+"
        rf"{months}[, ]+\d{{4}}"
    )

    month_day_year = (
        rf"{months}\s+\d{{1,2}}[, ]+\d{{4}}"
    )

    numeric_date = (
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    )

    iso_date = (
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}"
    )

    pattern = (
        rf"{day_month_year}"
        rf"|{month_day_year}"
        rf"|{numeric_date}"
        rf"|{iso_date}"
    )

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    return matches
import re
from datetime import datetime


def normalize_date(date_string):

    date_string = date_string.strip()

    formats = [
        # Day Month Year
        "%d %B %Y",      # 10 February 2026
        "%d %b %Y",      # 10 Feb 2026
        "%dst %B %Y",    # 1st February 2026
        "%dnd %B %Y",    # 2nd February 2026
        "%drd %B %Y",    # 3rd February 2026
        "%dth %B %Y",    # 10th February 2026

        "%dst %b %Y",     # 1st Feb 2026
        "%dnd %b %Y",     # 2nd Feb 2026
        "%drd %b %Y",     # 3rd Feb 2026
        "%dth %b %Y",     # 10th Feb 2026

        # Month Day Year
        "%B %d, %Y",      # February 10, 2026
        "%B %d %Y",       # February 10 2026
        "%b %d, %Y",      # Feb 10, 2026
        "%b %d %Y",       # Feb 10 2026

        # Numeric
        "%d/%m/%Y",       # 10/02/2026
        "%d/%m/%y",       # 10/02/26
        "%d-%m-%Y",       # 10-02-2026
        "%d-%m-%y",       # 10-02-26
        "%d.%m.%Y",       # 10.02.2026
        "%d.%m.%y",       # 10.02.26

        # ISO
        "%Y-%m-%d",       # 2026-02-10
        "%Y/%m/%d",       # 2026/02/10
        "%Y.%m.%d",       # 2026.02.10
    ]

    # Remove ordinal suffixes: 1st → 1, 2nd → 2, etc.
    date_string = re.sub(
        r"(\d{1,2})(st|nd|rd|th)",
        r"\1",
        date_string,
        flags=re.IGNORECASE
    )

    for date_format in formats:

        try:
            dt = datetime.strptime(
                date_string,
                date_format
            )

            return dt.strftime("%Y-%m-%d")

        except ValueError:
            continue

    return None
