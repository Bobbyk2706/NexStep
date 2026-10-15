from __future__ import annotations

"""
Facts -> the structures NexStep stores.

Everything here is deterministic: age limits become date-of-birth
boundaries, accepted qualifications become an OR group, and so on.

Important grounding rule:

- Informational facts may remain visible as warnings when they cannot
  be verified.
- Executable/authoritative rules must only be created when their
  supporting evidence can actually be located in the source document.
"""

import re
from datetime import date, timedelta

from app.ai.aggregated_extraction_result import ConflictOption
from app.ai.eligibility_rule_normalizer import normalize_date as normalize_any_date
from app.ai.eligibility_schemas import (
    EligibilityRuleData,
    EligibilityRuleGroupData,
    EligibilityRulesData,
)
from app.ai.exam_schemas import EligibilityInformation, ExamDateRange
from app.ai.extraction.facts import (
    AgeLimit,
    DatesDraft,
    EligibilityDraft,
    Fact,
)
from app.ai.extraction.dates import find_dates
from app.ai.extraction.age_rules import (
    dob_boundary,
    find_age_reference_date,
    is_exclusive,
    parse_explicit_dob_limits,
    subtract_years,  # re-exported: other modules and tests import it from here
)
from app.ai.extraction.grounding import Grounder, locate_quote


_LEVEL_ORDER = [
    "10th",
    "12th / Senior Secondary",
    "Diploma",
    "Bachelor's",
    "Master's",
    "PhD",
]


_CATEGORY_WORDS = re.compile(
    r"\b(obc|sc|st|ews|pwd|pwbd|ph|women|female|male|reserved|categor\w*|"
    r"ex-?servicem[ae]n|servicem[ae]n|relaxation|relaxable|domicile|defence|"
    r"handicapped|disab\w*|scheduled|castes?|tribes?|backward|benchmark\w*|"
    r"widows?|divorced|government\s+servants?|departmental)\b",
    re.IGNORECASE,
)

# Wording that introduces a concession on top of the general limit
# ("up to a maximum of five years in the case of ...").
_RELAXATION_WORDS = re.compile(
    r"\b(relax\w*|up\s+to\s+a\s+maximum\s+of|in\s+the\s+case\s+of|"
    r"(?:three|five|ten|\d+)\s+years?\s+(?:if|for|in))\b",
    re.IGNORECASE,
)

_GENERAL_WORDS = re.compile(
    r"\b(all|general|unreserved|ur|everyone|any|open)\b",
    re.IGNORECASE,
)

_COUNTRY_PREFIX = re.compile(
    r"^(?:citizens?|subjects?|nationals?)\s+of\s+(?:the\s+)?",
    re.IGNORECASE,
)

# A "country" that is really a sentence cannot be compared with a
# student's nationality.
_FREE_TEXT_COUNTRY = re.compile(
    r"[(),;]|\borigin\b|\brefugee\w*\b|\bmigrat\w*\b|\bwho\b|\bbefore\b|"
    r"\bafter\b|\bpermanent\w*\b|\bpersons?\b",
    re.IGNORECASE,
)

# Wording that identifies each accepted educational level. Used to check a
# level against its quote ("Bachelor's" is backed by "a degree of a
# recognised university") and to find a quote when the model gave none.
_LEVEL_PATTERNS = {
    "10th": re.compile(
        r"\b(?:10th|tenth|matric\w*|class\s*(?:x|10)\b|high\s+school)",
        re.IGNORECASE,
    ),
    "12th / Senior Secondary": re.compile(
        r"(?:\b(?:12th|twelfth|10\s*\+\s*2|senior\s+secondary|"
        r"higher\s+secondary|intermediate|hsc|class\s*(?:xii|12)\b)|\+\s*2\b)",
        re.IGNORECASE,
    ),
    "Diploma": re.compile(r"\bdiploma\b", re.IGNORECASE),
    "Bachelor's": re.compile(
        r"\b(?:bachelor\w*|graduat\w*|undergraduate|degree|btech|bsc|bca|"
        r"b\.\s?(?:tech|e|sc|a|com|arch)\b)",
        re.IGNORECASE,
    ),
    "Master's": re.compile(
        r"\b(?:master\w*|post\s*-?\s*graduat\w*|mtech|msc|mca|mba|"
        r"m\.\s?(?:tech|e|sc|a)\b)",
        re.IGNORECASE,
    ),
    "PhD": re.compile(r"\b(?:ph\.?\s?d|doctor\w*)", re.IGNORECASE),
}

_BACHELOR_SPECIFIC = re.compile(
    r"\b(?:bachelor\w*|undergraduate|btech|bsc|bca|b\.\s?(?:tech|e|sc|a|com|arch)\b)",
    re.IGNORECASE,
)

_HIGHER_WORDS = re.compile(
    r"\b(?:master\w*|post\s*-?\s*graduat\w*|doctor\w*|ph\.?\s?d)",
    re.IGNORECASE,
)

_NATIONALITY_SENTENCE = re.compile(
    r"\b(?:citizen|national|subject)s?\b.{0,60}"
    r"\b(?:india|nepal|bhutan|bangladesh|sri\s+lanka)\b"
    r"|\bindian\s+(?:citizen|national)s?\b",
    re.IGNORECASE,
)

# "... or (d) a person of Indian origin who has migrated from Pakistan,
# Burma, Sri Lanka ..." -- the countries after this phrase are where such
# people came from, not nationalities that may apply.
_ORIGIN_START = re.compile(
    r"\b(?:persons?\s+of\s+indian\s+origin|indian\s+origin|"
    r"migrated\s+from|came\s+over\s+from)\b",
    re.IGNORECASE,
)

_PASSAGE_TAG = re.compile(r"^\[(P\d+) \| [^\n]*\]\s*$", re.MULTILINE)

_NUMBER_WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "eleven": "11", "twelve": "12", "fifteen": "15", "twenty": "20",
    "thirty": "30",
}


_DEMONYMS = {
    "indian": "India",
    "nepali": "Nepal",
    "nepalese": "Nepal",
    "bhutanese": "Bhutan",
    "bangladeshi": "Bangladesh",
    "sri lankan": "Sri Lanka",
    "pakistani": "Pakistan",
    "american": "United States",
    "british": "United Kingdom",
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def iso(value: str | None) -> date | None:
    if not value:
        return None

    try:
        return date.fromisoformat(
            normalize_any_date(value.strip())
        )
    except Exception:
        return None


# subtract_years now lives in age_rules.py (imported above) so that the
# date arithmetic can be unit-tested without pydantic or a database.


def canonical_country(name: str) -> str:
    cleaned = _COUNTRY_PREFIX.sub("", name.strip().strip("."))

    return _DEMONYMS.get(
        cleaned.lower(),
        cleaned,
    )


# ---------------------------------------------------------------------------
# Exam dates
# ---------------------------------------------------------------------------

def compile_dates(
    draft: DatesDraft,
    g: Grounder,
    tba_hint: bool,
    context_text: str = "",
) -> dict:
    """
    Validate and ground every date.

    A date is stored only when:
      1. it parses correctly,
      2. it occurs somewhere in the document,
      3. its supporting quote can be located, and
      4. the quote is compatible with the extracted date.

    This prevents an LLM-generated date from becoming authoritative
    merely because the date happens to appear somewhere in the PDF.
    """

    def scalar(
        fact: Fact,
        label: str,
    ) -> str | None:
        quote, passage, value = fact.quote, fact.passage, fact.value
        if not value:
            recovered_fact = _recover_application_date(context_text, label)
            if recovered_fact is None:
                return None
            value, quote, passage = recovered_fact

        parsed = iso(value)

        if parsed is None:
            g.issue(
                "warning",
                "date-unparsed",
                f"{label}: '{value}' is not a valid date.",
                label,
            )
            return None

        # The date must occur somewhere in the source document.
        if not g.date_is_grounded(parsed):
            g.issue(
                "warning",
                "date-not-in-document",
                (
                    f"{label}: {parsed} does not appear anywhere in "
                    "the document, so it was left empty."
                ),
                label,
            )
            return None

        if not _date_quote_located(g, quote, passage, parsed):
            recovered = _recover_date_quote(context_text, parsed, label)
            if recovered is not None:
                quote, passage = recovered

        # The supporting quote must specifically support the date.
        if not g.quote_backs_date(parsed, quote):
            g.issue(
                "warning",
                "date-quote-mismatch",
                (
                    f"{label}: {parsed} is not supported by the "
                    "quoted text, so it was left empty."
                ),
                label,
            )
            return None

        # The quote must actually be found in the source document.
        supported = g.support(
            label,
            quote,
            passage,
            required=False,
        )

        if not supported:
            g.issue(
                "warning",
                "date-unverified",
                (
                    f"{label}: the supporting quote could not be "
                    "located in the document, so the date was left empty."
                ),
                label,
            )
            return None

        return parsed.isoformat()

    def _date_quote_located(
        grounder: Grounder,
        quote: str | None,
        passage: str | None,
        value: date,
    ) -> bool:
        return (
            grounder.quote_backs_date(value, quote)
            and locate_quote(quote, passage, grounder.passages) is not None
        )

    start = scalar(
        draft.application_start_date,
        "Application start date",
    )

    end = scalar(
        draft.application_end_date,
        "Application end date",
    )

    late = scalar(
        draft.late_fee_end_date,
        "Late-fee application end date",
    )

    if start is None and tba_hint:
        g.issue(
            "info",
            "start-tba",
            (
                "The application start date is listed as "
                "'to be announced' in the document."
            ),
            "Application start date",
        )

    if late:
        g.issue(
            "info",
            "late-fee-deadline",
            (
                f"Extended (late-fee) application deadline: {late}. "
                "Only the regular deadline is stored."
            ),
            "Application end date",
        )

    if start and end and start > end:
        g.issue(
            "error",
            "date-order",
            "Application start date is after the application end date.",
            "Application end date",
        )

    ranges: list[ExamDateRange] = []
    seen: set[tuple[str, str]] = set()

    for item in draft.exam_dates:
        a = iso(item.start_date)
        b = iso(item.end_date)

        label = (
            f"Exam date ({item.label})"
            if item.label
            else "Exam date"
        )

        if a is None or b is None:
            g.issue(
                "warning",
                "date-unparsed",
                (
                    f"{label}: '{item.start_date} – "
                    f"{item.end_date}' is not a valid date range."
                ),
                label,
            )
            continue

        if a > b:
            a, b = b, a

            g.issue(
                "warning",
                "date-swapped",
                (
                    f"{label}: start and end were reversed in the "
                    "extraction and have been swapped."
                ),
                label,
            )

        # Both endpoints must exist in the document.
        missing = [
            d
            for d in (a, b)
            if not g.date_is_grounded(d)
        ]

        if missing:
            g.issue(
                "warning",
                "date-not-in-document",
                (
                    f"{label}: {', '.join(str(m) for m in missing)} "
                    "does not appear in the document; range dropped."
                ),
                label,
            )
            continue

        # The quoted evidence must support both endpoints.
        if not g.quote_backs_date(
            a,
            item.quote,
        ):
            g.issue(
                "warning",
                "date-quote-mismatch",
                (
                    f"{label}: start date {a} is not supported by "
                    "the quoted text; range dropped."
                ),
                label,
            )
            continue

        if not g.quote_backs_date(
            b,
            item.quote,
        ):
            g.issue(
                "warning",
                "date-quote-mismatch",
                (
                    f"{label}: end date {b} is not supported by "
                    "the quoted text; range dropped."
                ),
                label,
            )
            continue

        # The quote itself must exist in the source.
        supported = g.support(
            label,
            item.quote,
            item.passage,
        )

        if not supported:
            g.issue(
                "warning",
                "date-unverified",
                (
                    f"{label}: the supporting quote could not be "
                    "located in the document; range dropped."
                ),
                label,
            )
            continue

        key = (
            a.isoformat(),
            b.isoformat(),
        )

        if key in seen:
            continue

        seen.add(key)

        ranges.append(
            ExamDateRange(
                start_date=key[0],
                end_date=key[1],
            )
        )

    ranges.sort(
        key=lambda r: r.start_date
    )

    if end and ranges and ranges[0].start_date < end:
        g.issue(
            "warning",
            "exam-before-deadline",
            (
                "An exam date falls before the application end "
                "date; check the dates."
            ),
            "Exam dates",
        )

    return {
        "application_start_date": start,
        "application_end_date": end,
        "exam_dates": ranges,
    }


# ---------------------------------------------------------------------------
# Eligibility
# ---------------------------------------------------------------------------

def _is_general(limit: AgeLimit) -> bool:
    """
    True for the limit that applies to every candidate.

    A concession for a category ("up to five years for SC/ST") is not a
    competing value of the same limit, so it must not become a date-of-birth
    rule or a "conflict". The category is recognised from `applies_to`, and
    also from the quoted sentence, because models often leave `applies_to`
    empty for concessions.
    """

    applies = (limit.applies_to or "").strip()

    if applies:
        if _CATEGORY_WORDS.search(applies):
            return False

        if _GENERAL_WORDS.search(applies):
            return True

    quote = limit.quote or ""

    if _RELAXATION_WORDS.search(quote) and _CATEGORY_WORDS.search(quote):
        return False

    return True


def _expand_higher(
    levels: list[str],
    evidence_text: str,
) -> list[str]:
    """
    '...or a higher degree is also eligible'
    -> include all higher levels.
    """

    if not re.search(
        r"higher (degree|qualification)|degree higher|higher than",
        evidence_text,
        re.I,
    ):
        return levels

    known = [
        lvl
        for lvl in levels
        if lvl in _LEVEL_ORDER
    ]

    if not known:
        return levels

    lowest = min(
        _LEVEL_ORDER.index(lvl)
        for lvl in known
    )

    return [
        *levels,
        *[
            lvl
            for lvl in _LEVEL_ORDER[lowest:]
            if lvl not in levels
        ],
    ]


def _nationality_backs_quote(
    country: str,
    quote: str | None,
) -> bool:
    """
    Check whether a canonical country name is supported by nationality
    wording in the evidence.

    Handles both country names and common demonyms, for example:

        India  -> Indian
        Nepal  -> Nepali / Nepalese
        Bhutan -> Bhutanese

    IMPORTANT:
    Missing quote is NOT considered sufficient evidence.
    """

    if not country:
        return False

    if not quote:
        return False

    normalized_quote = quote.lower()

    demonyms = {
        "india": (
            "india",
            "indian",
        ),
        "nepal": (
            "nepal",
            "nepali",
            "nepalese",
        ),
        "bhutan": (
            "bhutan",
            "bhutanese",
        ),
        "bangladesh": (
            "bangladesh",
            "bangladeshi",
        ),
        "sri lanka": (
            "sri lanka",
            "sri lankan",
        ),
        "pakistan": (
            "pakistan",
            "pakistani",
        ),
        "united states": (
            "united states",
            "american",
        ),
        "united kingdom": (
            "united kingdom",
            "british",
        ),
    }

    accepted = demonyms.get(
        country.lower(),
        (country.lower(),),
    )

    return any(
        re.search(
            rf"\b{re.escape(term)}\b",
            normalized_quote,
        )
        for term in accepted
    )


def _age_limit_backs_quote(
    limit: AgeLimit,
    g: Grounder,
    quote: str | None = None,
) -> bool:
    """
    Verify that the age and, when present, the reference date are
    represented in the supporting quote.

    `quote` overrides limit.quote when a quote had to be recovered from the
    document text.
    """

    quote = limit.quote if quote is None else quote

    if not quote:
        return False

    # The age itself must be explicitly present ("32 years", "age of 32",
    # "18-32 years"), as a whole number, in a sentence about years or age.
    if not re.search(
        rf"(?<!\d){re.escape(str(limit.years))}(?!\d)",
        quote,
    ):
        return False

    if not re.search(
        r"\b(?:years?|yrs?|age)\b",
        quote,
        re.IGNORECASE,
    ):
        return False

    # If an "as on" date was extracted, the same quote must support it.
    if limit.as_on_date:
        reference_date = iso(
            limit.as_on_date
        )

        if reference_date is None:
            return False

        if not g.quote_backs_date(
            reference_date,
            quote,
        ):
            return False

    return True


# ---------------------------------------------------------------------------
# Quote helpers
# ---------------------------------------------------------------------------

def _passage_blocks(context_text: str) -> list[tuple[str, str]]:
    """Split the rendered context pack back into (passage id, text)."""

    tags = list(_PASSAGE_TAG.finditer(context_text))

    blocks = []

    for index, tag in enumerate(tags):
        end = (
            tags[index + 1].start()
            if index + 1 < len(tags)
            else len(context_text)
        )

        blocks.append((tag.group(1), context_text[tag.end():end]))

    return blocks


def _recover_sentence(
    context_text: str,
    predicate,
) -> tuple[str, str] | None:
    """
    First sentence of the retrieved document text that satisfies
    `predicate`, with the id of the passage it is in.

    The sentence is copied from the document itself, so it can always be
    located again by the grounder.
    """

    for passage_id, text in _passage_blocks(context_text):
        for part in re.split(r"(?<=[.;:])\s+|\n+", text):
            sentence = part.strip()

            if len(sentence) < 12:
                continue

            if predicate(sentence):
                return sentence[:400], passage_id

    return None


def _recover_date_quote(
    context_text: str,
    value: date,
    label: str,
) -> tuple[str, str] | None:
    """Recover literal date evidence from the relevant schedule row."""
    field = label.lower()
    if "late-fee" in field:
        required = re.compile(r"\b(?:late|extended|extension)\b", re.I)
        excluded = None
    elif "start" in field:
        required = re.compile(
            r"\b(?:open(?:ing)?|start(?:ing)?|commenc\w*|begin\w*|registration)\b",
            re.I,
        )
        excluded = re.compile(r"\b(?:late|extended|closing|last date)\b", re.I)
    else:
        required = re.compile(
            r"\b(?:clos(?:e|es|ed|ing)|last date|deadline|end date|registration)\b",
            re.I,
        )
        excluded = re.compile(r"\b(?:late|extended|with late fee)\b", re.I)

    candidates: list[tuple[int, str, str]] = []
    for passage_id, text in _passage_blocks(context_text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for index, line in enumerate(lines):
            if value not in {mention.value for mention in find_dates(line)}:
                continue

            for start in range(max(0, index - 2), index + 1):
                for end in range(index + 1, min(len(lines), start + 4) + 1):
                    snippet = " ".join(lines[start:end])
                    if value not in {mention.value for mention in find_dates(snippet)}:
                        continue
                    if not required.search(snippet):
                        continue
                    if excluded and excluded.search(snippet):
                        continue
                    candidates.append((len(snippet), snippet[:400], passage_id))

    if not candidates:
        return None
    _, quote, passage_id = min(candidates, key=lambda candidate: candidate[0])
    return quote, passage_id


def _recover_application_date(
    context_text: str,
    label: str,
) -> tuple[str, str, str] | None:
    """Find an application schedule date when the model omitted the field."""
    field = label.lower()
    if "late-fee" in field:
        required = re.compile(r"\b(?:late|extended|extension)\b", re.I)
        excluded = None
    elif "start" in field:
        required = re.compile(
            r"\b(?:open(?:ing)?|start(?:ing)?|commenc\w*|begin\w*|registration)\b",
            re.I,
        )
        excluded = re.compile(r"\b(?:late|extended|closing|last date)\b", re.I)
    else:
        required = re.compile(
            r"\b(?:clos(?:e|es|ed|ing)|last date|deadline|end date|registration)\b",
            re.I,
        )
        excluded = re.compile(r"\b(?:late|extended|with late fee)\b", re.I)

    candidates: list[tuple[int, date, str, str]] = []
    for passage_id, text in _passage_blocks(context_text):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for index in range(len(lines)):
            for start in range(max(0, index - 2), index + 1):
                for end in range(index + 1, min(len(lines), start + 4) + 1):
                    snippet = " ".join(lines[start:end])
                    if not required.search(snippet) or (excluded and excluded.search(snippet)):
                        continue
                    for mention in find_dates(snippet):
                        candidates.append((len(snippet), mention.value, snippet[:400], passage_id))

    if not candidates:
        return None
    _, value, quote, passage_id = min(candidates, key=lambda item: item[0])
    return value.isoformat(), quote, passage_id


def _recover_qualification_candidates(
    context_text: str,
) -> list[tuple[str, str, str]]:
    """Find explicit education requirements when the model omitted them.

    Each returned qualification is tied to a literal sentence in the
    retrieved eligibility passages, so the compiler can ground it normally.
    """
    candidates: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    eligibility_cue = re.compile(
        r"\b(?:eligib\w*|qualif\w*|must\s+(?:have|possess|hold)|"
        r"shall\s+(?:have|possess|hold)|should\s+(?:have|possess|hold)|"
        r"required\s+to|currently\s+(?:studying|pursuing)|"
        r"completed|degree\s+of)\b",
        re.I,
    )

    for passage_id, text in _passage_blocks(context_text):
        for part in re.split(r"(?<=[.;:])\s+|\n+", text):
            sentence = part.strip()
            if len(sentence) < 18 or not eligibility_cue.search(sentence):
                continue
            levels = [
                level for level in _LEVEL_ORDER
                if _level_backs_quote(level, sentence)
            ]
            for level in levels:
                key = (level, sentence)
                if key not in seen:
                    candidates.append((level, sentence[:400], passage_id))
                    seen.add(key)
    return candidates


def _resolve_quote(
    g: Grounder,
    quote: str | None,
    passage: str | None,
    context_text: str,
    predicate,
) -> tuple[str | None, str | None, bool]:
    """
    Keep the model's quote when it can be found in the document.

    Small models often return no quote, or one that is not verbatim. In that
    case the sentence of the retrieved text that matches the claim is used
    instead, and the reviewer is told. Returns (quote, passage, recovered).
    """

    if quote and locate_quote(quote, passage, g.passages) is not None:
        return quote, passage, False

    found = _recover_sentence(context_text, predicate)

    if found is None:
        return quote, passage, False

    return found[0], found[1], True


def _origin_only_countries(
    quote: str | None,
    countries: list[str],
) -> tuple[set[str], str | None]:
    """
    Countries that appear only in the "persons of Indian origin who migrated
    from ..." part of the nationality sentence, with that part of the
    sentence. India itself is never excluded.
    """

    if not quote:
        return set(), None

    match = _ORIGIN_START.search(quote)

    if match is None:
        return set(), None

    before = quote[: match.start()].lower()
    after = quote[match.start():].lower()

    excluded = {
        country
        for country in countries
        if country != "India"
        and country.lower() in after
        and country.lower() not in before
    }

    if not excluded:
        return set(), None

    return excluded, " ".join(quote[match.start():].split())[:240]


def _mentions_age(sentence: str, years: int) -> bool:
    if _RELAXATION_WORDS.search(sentence) and _CATEGORY_WORDS.search(sentence):
        return False

    return bool(
        re.search(rf"(?<!\d){years}(?!\d)", sentence)
        and re.search(r"\b(?:years?|yrs?|age)\b", sentence, re.IGNORECASE)
    )


def _level_backs_quote(level: str, quote: str | None) -> bool:
    """True when the quote talks about this educational level."""

    if not quote:
        return False

    pattern = _LEVEL_PATTERNS.get(level)

    if pattern is None or not pattern.search(quote):
        return False

    # "degree" alone also appears in "Master's degree"; for Bachelor's it
    # only counts when no higher level is mentioned.
    if (
        level == "Bachelor's"
        and not _BACHELOR_SPECIFIC.search(quote)
        and _HIGHER_WORDS.search(quote)
    ):
        return False

    return True


def _digits(text: str | None) -> set[str]:
    tokens = {
        str(int(number))
        for number in re.findall(r"\d+", text or "")
    }

    for word, digit in _NUMBER_WORDS.items():
        if re.search(rf"\b{word}\b", (text or "").lower()):
            tokens.add(digit)

    return tokens


def _numbers_supported(text: str | None, quote: str | None) -> bool:
    """
    Every number in an informational statement must occur in its quote.

    A summary ("born not earlier than 02.08.1996") is worded differently
    from the notice, so word overlap is a poor test for it; the numbers are
    what must not be invented.
    """

    return _digits(text) <= _digits(quote)


def _short(text: str, width: int = 50) -> str:
    if len(text) <= width:
        return text

    cut = text[:width].rsplit(" ", 1)[0] or text[:width]

    return cut + "…"


def compile_eligibility(
    draft: EligibilityDraft,
    g: Grounder,
    context_text: str,
) -> tuple[
    EligibilityInformation,
    EligibilityRulesData,
]:
    rules: list[EligibilityRuleData] = []
    children: list[EligibilityRuleGroupData] = []
    other: list[str] = []

    # ---- age -> date of birth ------------------------------------------

    min_age = None
    max_age = None

    general: dict[str, list[AgeLimit]] = {
        "minimum": [],
        "maximum": [],
    }

    for limit in draft.age_limits:
        if limit.years <= 0 or limit.years > 120:
            g.issue(
                "warning",
                "age-invalid",
                (
                    f"Ignored implausible age limit: "
                    f"{limit.years} years."
                ),
                "Age limit",
            )
            continue

        if _is_general(limit):
            general[limit.kind].append(limit)
        else:
            who = (
                (limit.applies_to or "").strip()
                or _short((limit.quote or "").strip(), 70)
                or "a category of candidates"
            )

            text = (
                f"Age {limit.kind} {limit.years} years for {who}"
                + (
                    f" (as on {limit.as_on_date})"
                    if limit.as_on_date
                    else ""
                )
            )

            if text not in other:
                other.append(text)

            g.support(
                f"Age limit ({who})",
                limit.quote,
                limit.passage,
                required=False,
            )

    dob_rules: list[EligibilityRuleData] = []

    # One "as on" date for the whole notice, used when the model did not
    # report one for a limit.
    default_reference = find_age_reference_date(context_text)

    for kind, limits in general.items():
        if not limits:
            continue

        distinct = {
            (
                l.years,
                l.as_on_date,
            )
            for l in limits
        }

        resolved = []

        for limit in limits:
            quote, passage, recovered = _resolve_quote(
                g,
                limit.quote,
                limit.passage,
                context_text,
                lambda sentence, years=limit.years: _mentions_age(
                    sentence, years
                ),
            )

            resolved.append((limit, quote, passage, recovered))

        # Prefer an age limit whose value and reference date are
        # actually supported by its quoted evidence.
        supported_limits = [
            item
            for item in resolved
            if _age_limit_backs_quote(
                item[0],
                g,
                item[1],
            )
        ]

        if not supported_limits:
            g.issue(
                "warning",
                "age-value-quote-mismatch",
                (
                    f"Age limit ({kind}): none of the extracted "
                    "age/reference-date values are fully supported "
                    "by their quoted text; no date-of-birth rule "
                    "was created."
                ),
                f"Age limit ({kind})",
            )
            continue

        chosen, quote, passage, recovered = supported_limits[0]

        if len(distinct) > 1:
            g.conflict(
                f"Age limit ({kind})",
                [
                    ConflictOption(
                        value=(
                            f"{l.years} years"
                            + (
                                f" as on {l.as_on_date}"
                                if l.as_on_date
                                else ""
                            )
                        ),
                        source=(l.quote or "")[:160],
                        pages=(
                            g.passages[l.passage].pages
                            if l.passage in g.passages
                            else []
                        ),
                    )
                    for l in limits
                ],
                f"{chosen.years} years",
                (
                    "Provisionally using the first general limit "
                    "found; verify against the document."
                ),
            )

        label = f"Age limit ({kind})"

        # "must not have attained 32" means the last eligible age is 31.
        exclusive = is_exclusive(kind, quote)

        shown = chosen.years

        if exclusive:
            shown = chosen.years - 1 if kind == "maximum" else chosen.years + 1

        if kind == "minimum":
            min_age = shown
        else:
            max_age = shown

        # The supporting quote must actually be located before
        # considering the age fact authoritative.
        supported = g.support(
            label,
            quote,
            passage,
        )

        if not supported:
            g.issue(
                "warning",
                "age-unverified",
                (
                    f"{label}: the supporting quote could not be "
                    "located in the document; no date-of-birth "
                    "rule was created."
                ),
                label,
            )
            continue

        if recovered:
            g.issue(
                "info",
                "quote-recovered",
                (
                    f"{label}: the model gave no usable quote, so the "
                    "matching sentence from the document was used."
                ),
                label,
            )

        if exclusive:
            g.issue(
                "info",
                "age-exclusive",
                (
                    f"{label}: the notice says candidates must not have "
                    f"attained {chosen.years} years, so the last eligible "
                    f"age is {shown}."
                    if kind == "maximum"
                    else (
                        f"{label}: the notice says candidates must be "
                        f"older than {chosen.years}, so the first eligible "
                        f"age is {shown}."
                    )
                ),
                label,
            )

        ref = iso(
            chosen.as_on_date
        )

        if ref is None and default_reference is not None:
            ref = default_reference

            g.issue(
                "info",
                "age-reference-from-notice",
                (
                    f"{label}: the 'as on' date {ref} was taken from "
                    "the notification text."
                ),
                label,
            )

        if ref is None:
            g.issue(
                "warning",
                "age-no-reference-date",
                (
                    f"The {kind} age of {chosen.years} years has "
                    "no 'as on' date in the document, so no "
                    "date-of-birth rule was created."
                ),
                label,
            )
            continue

        if not g.date_is_grounded(ref):
            g.issue(
                "warning",
                "date-not-in-document",
                (
                    f"{label}: reference date {ref} is not in "
                    "the document."
                ),
                label,
            )
            continue

        operator, boundary = dob_boundary(
            kind,
            chosen.years,
            ref,
            exclusive=exclusive,
        )

        dob_rules.append(
            EligibilityRuleData(
                attribute="Date of Birth",
                operator=operator,
                value=boundary.isoformat(),
            )
        )

    # ---- birth dates written out in the notice -----------------------
    #
    # "born not earlier than 2nd August 1993 and not later than
    # 1st August 2004" is authoritative; when present it replaces the
    # boundary calculated from the age.

    explicit = parse_explicit_dob_limits(
        context_text,
        exclude=_CATEGORY_WORDS,
    )

    for key, operator, words in (
        ("earliest", ">=", "not earlier than"),
        ("latest", "<=", "not later than"),
    ):
        found = explicit[key]

        if found is None:
            continue

        found_date, snippet = found

        if not g.date_is_grounded(found_date):
            continue

        if not g.support(
            f"Date of birth ({words})",
            snippet,
            None,
            required=False,
        ):
            continue

        replaced = [r for r in dob_rules if r.operator == operator]

        dob_rules = [r for r in dob_rules if r.operator != operator]

        if replaced and replaced[0].value != found_date.isoformat():
            g.issue(
                "warning",
                "dob-from-notice",
                (
                    f"The notice states the date of birth limit "
                    f"({words} {found_date}) outright; it was used "
                    f"instead of the value calculated from the age "
                    f"limit ({replaced[0].value})."
                ),
                "Date of birth",
            )

        dob_rules.append(
            EligibilityRuleData(
                attribute="Date of Birth",
                operator=operator,
                value=found_date.isoformat(),
            )
        )

    if explicit.get("varies") and (explicit["earliest"] or explicit["latest"]):
        g.issue(
            "warning",
            "dob-varies-by-post",
            (
                "The notice gives different birth-date limits for "
                "different posts. The most generous limit was used for "
                "the exam-level rule; check the post-wise limits."
            ),
            "Date of birth",
        )

    rules.extend(dob_rules)

    if draft.has_no_age_limit and not draft.age_limits:
        other.append("No age limit")

    # ---- qualifications: OR of accepted levels -----------------------

    levels: list[str] = []
    fields: list[str] = []
    quals_text = ""

    for q in draft.qualifications:
        label = f"Qualification: {q.level}"

        # Use the model's quote when it is in the document; otherwise the
        # sentence of the document that talks about this level.
        quote, passage, recovered = _resolve_quote(
            g,
            q.quote,
            q.passage,
            context_text,
            lambda sentence, level=q.level: _level_backs_quote(
                level, sentence
            ),
        )

        # The quote must exist in the source document.
        quote_found = g.support(
            label,
            quote,
            passage,
            required=False,
        )

        # The extracted qualification must also agree with its evidence.
        # "Bachelor's" is backed by "a degree of a recognised university",
        # so the level is checked by meaning as well as by wording.
        value_supported = g.value_backs_quote(
            q.level,
            quote,
        ) or _level_backs_quote(q.level, quote)

        if not value_supported:
            g.issue(
                "warning",
                "value-quote-mismatch",
                (
                    f"{label}: the extracted qualification is "
                    "not supported by the quoted text; it was ignored."
                ),
                label,
            )
            continue

        if not quote_found:
            g.issue(
                "warning",
                "qualification-unverified",
                (
                    f"{label}: the supporting quote could not be "
                    "located in the document; it was ignored."
                ),
                label,
            )
            continue

        if recovered:
            g.issue(
                "info",
                "quote-recovered",
                (
                    f"{label}: the model gave no usable quote, so the "
                    "matching sentence from the document was used."
                ),
                label,
            )

        if q.level not in levels:
            levels.append(q.level)

        if q.field and q.field not in fields:
            fields.append(q.field)

        quals_text += " " + (
            quote or ""
        )

    # A model may omit all qualifications even though the retrieved
    # eligibility text states them explicitly. Recover only a literal
    # qualification sentence from those passages and still ground it.
    recovered_qualification = False
    if not levels:
        for level, quote, passage in _recover_qualification_candidates(context_text):
            if level in levels or not _level_backs_quote(level, quote):
                continue
            if not g.support(
                f"Qualification: {level}",
                quote,
                passage,
                required=False,
            ):
                continue
            levels.append(level)
            quals_text += " " + quote
            recovered_qualification = True

    if recovered_qualification:
        g.issue(
            "info",
            "qualification-recovered",
            (
                "No usable qualification was returned by the model, so "
                "an explicit education requirement from the notification "
                "was used."
            ),
            "Educational Qualification",
        )

    levels = _expand_higher(
        levels,
        quals_text + " " + context_text,
    )

    if levels:
        children.append(
            EligibilityRuleGroupData(
                logical_operator="OR",
                rules=[
                    EligibilityRuleData(
                        attribute="Educational Qualification",
                        operator="=",
                        value=level,
                    )
                    for level in levels
                ],
            )
        )

    # ---- scores --------------------------------------------------------

    score_rule_created = False

    if draft.minimum_percentage is not None:
        percentage_value = _num(
            draft.minimum_percentage
        )

        score_supported = g.support(
            "Minimum percentage",
            draft.score_quote,
            draft.score_passage,
        )

        if (
            score_supported
            and g.value_backs_quote(
                percentage_value,
                draft.score_quote,
            )
        ):
            rules.append(
                EligibilityRuleData(
                    attribute="Percentage",
                    operator=">=",
                    value=percentage_value,
                )
            )

            score_rule_created = True
        elif score_supported:
            g.issue(
                "warning",
                "value-quote-mismatch",
                (
                    f"Minimum percentage '{percentage_value}' "
                    "is not supported by the quoted text; "
                    "it was ignored."
                ),
                "Minimum percentage",
            )

    if draft.minimum_cgpa is not None:
        cgpa_value = _num(
            draft.minimum_cgpa
        )

        score_supported = g.support(
            "Minimum CGPA",
            draft.score_quote,
            draft.score_passage,
        )

        if (
            score_supported
            and g.value_backs_quote(
                cgpa_value,
                draft.score_quote,
            )
        ):
            rules.append(
                EligibilityRuleData(
                    attribute="CGPA",
                    operator=">=",
                    value=cgpa_value,
                )
            )

            score_rule_created = True
        elif score_supported:
            g.issue(
                "warning",
                "value-quote-mismatch",
                (
                    f"Minimum CGPA '{cgpa_value}' is not "
                    "supported by the quoted text; it was ignored."
                ),
                "Minimum CGPA",
            )

    # ---- nationality: OR of countries -------------------------------

    countries: list[str] = []

    # Nationality is executable eligibility data, so the supporting
    # quote must actually exist in the source document. Nothing is
    # checked (or reported) when the notice names no nationality.
    if draft.nationalities:
        nat_quote, nat_passage, nat_recovered = _resolve_quote(
            g,
            draft.nationality_quote,
            draft.nationality_passage,
            context_text,
            _NATIONALITY_SENTENCE.search,
        )

        nationality_supported = g.support(
            "Nationality",
            nat_quote,
            nat_passage,
        )

        if nationality_supported and nat_recovered:
            g.issue(
                "info",
                "quote-recovered",
                (
                    "Nationality: the model gave no usable quote, so "
                    "the matching sentence from the document was used."
                ),
                "Nationality",
            )

        if nationality_supported:
            canonical = [
                canonical_country(name) for name in draft.nationalities
            ]

            origin_only, origin_text = _origin_only_countries(
                nat_quote,
                [c for c in canonical if c],
            )

            if origin_text:
                note = f"Nationality: {origin_text}"

                if note not in other:
                    other.append(note)

            for name in draft.nationalities:
                country = canonical_country(name)

                if not country:
                    continue

                if country in origin_only:
                    continue

                # "Persons of Indian origin who migrated from ..." is a
                # condition, not a country. It cannot be compared with a
                # student's nationality, so it is shown to the reviewer
                # instead of becoming a rule that can never match.
                if len(country) > 40 or _FREE_TEXT_COUNTRY.search(country):
                    note = f"Nationality: {name.strip()}"

                    if note not in other:
                        other.append(note)

                    continue

                if not _nationality_backs_quote(
                    country,
                    nat_quote,
                ):
                    g.issue(
                        "warning",
                        "value-quote-mismatch",
                        (
                            f"Nationality '{country}' is not supported "
                            "by the quoted text; it was ignored."
                        ),
                        "Nationality",
                    )
                    continue

                if country not in countries:
                    countries.append(country)

            if countries:
                children.append(
                    EligibilityRuleGroupData(
                        logical_operator="OR",
                        rules=[
                            EligibilityRuleData(
                                attribute="Nationality",
                                operator="=",
                                value=country,
                            )
                            for country in countries
                        ],
                    )
                )

    # ---- work experience is informational ----------------------------

    #
    # The current eligibility evaluator only supports text equality
    # for Work Experience, so numeric experience requirements are not
    # converted into executable rules yet.

    work = draft.work_experience.value

    if work:
        work_label = "Work experience"

        quote_found = g.support(
            work_label,
            draft.work_experience.quote,
            draft.work_experience.passage,
            required=False,
        )

        # The statement is a summary, so its numbers (not its wording)
        # must be present in the quote.
        value_supported = _numbers_supported(
            work,
            draft.work_experience.quote,
        )

        if quote_found and value_supported:
            # Keep this informational until the evaluator supports
            # numeric work-experience comparisons.
            pass
        else:
            g.issue(
                "warning",
                (
                    "value-quote-mismatch"
                    if not value_supported
                    else "work-experience-unverified"
                ),
                (
                    f"{work_label}: the extracted value is not "
                    "supported by the quoted text; it was ignored."
                ),
                work_label,
            )
            work = None

    # ---- other requirements -------------------------------------------

    for item in draft.other_requirements:
        text = item.text.strip()

        if not text:
            continue

        label = f"Requirement: {_short(text)}"

        quote_found = g.support(
            label,
            item.quote,
            item.passage,
            required=False,
        )

        # Informational statements are summaries: they are kept when the
        # quote is in the document and every number in them is in the quote.
        value_supported = _numbers_supported(
            text,
            item.quote,
        )

        if not quote_found or not value_supported:
            g.issue(
                "warning",
                (
                    "value-quote-mismatch"
                    if not value_supported
                    else "requirement-unverified"
                ),
                (
                    f"{label}: the extracted requirement is not "
                    "sufficiently supported by its quoted text; "
                    "it was ignored."
                ),
                label,
            )
            continue

        if text not in other:
            other.append(text)

    info = EligibilityInformation(
        minimum_age=min_age,
        maximum_age=max_age,
        educational_qualification=(
            ", ".join(levels)
            + (
                f" ({'; '.join(fields)})"
                if fields
                else ""
            )
            if levels
            else None
        ),
        nationality=", ".join(countries) or None,
        work_experience=work,
        other_requirements=other,
    )

    groups = []

    if rules or children:
        groups.append(
            EligibilityRuleGroupData(
                logical_operator="AND",
                rules=rules,
                child_groups=children,
            )
        )

    return (
        info,
        EligibilityRulesData(
            rule_groups=groups
        ),
    )


def _num(x: float) -> str:
    return (
        str(int(x))
        if float(x).is_integer()
        else str(x)
    )
