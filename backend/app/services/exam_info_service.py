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


import re
from datetime import datetime


def normalize_date(date_string):

    date_string = date_string.strip()

    date_string = re.sub(
        r"(\d{1,2})(st|nd|rd|th)",
        r"\1",
        date_string,
        flags=re.IGNORECASE
    )

    time_pattern = (
        r"\b\d{1,2}(?::\d{2}(?::\d{2})?)?"
        r"\s*(?:AM|PM|am|pm|hrs?|hours?)?\b"
    )

    time_match = re.search(
        time_pattern,
        date_string,
        re.IGNORECASE
    )

    time_value = None

    if time_match and (
        ":" in time_match.group()
        or re.search(r"\b(?:AM|PM)\b", time_match.group(), re.IGNORECASE)
    ):
        time_value = time_match.group().strip()

        date_string = (
            date_string[:time_match.start()]
            + date_string[time_match.end():]
        ).strip()

        date_string = re.sub(
            r"\s+(at|up to|till|until)\s*$",
            "",
            date_string,
            flags=re.IGNORECASE
        ).strip(" ,.-")

    formats = [
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%b %d %Y",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%d-%m-%Y",
        "%d-%m-%y",
        "%d.%m.%Y",
        "%d.%m.%y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
    ]

    normalized_date = None

    for date_format in formats:

        try:
            dt = datetime.strptime(
                date_string,
                date_format
            )

            normalized_date = dt.strftime("%Y-%m-%d")
            break

        except ValueError:
            continue

    if normalized_date is None:
        return None

    normalized_time = None

    if time_value:

        time_value = re.sub(
            r"\s*(hrs?|hours?)\s*$",
            "",
            time_value,
            flags=re.IGNORECASE
        ).strip()

        if re.fullmatch(r"24:00(?::00)?", time_value):
            normalized_time = "24:00"

        else:

            time_formats = [
                "%I:%M %p",
                "%I %p",
                "%H:%M",
                "%H:%M:%S",
            ]

            for time_format in time_formats:

                try:
                    time_obj = datetime.strptime(
                        time_value.upper(),
                        time_format
                    )

                    normalized_time = time_obj.strftime("%H:%M")
                    break

                except ValueError:
                    continue

    return {
        "date": normalized_date,
        "time": normalized_time
    }