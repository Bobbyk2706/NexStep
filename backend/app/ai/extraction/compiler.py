from __future__ import annotations

"""
Facts -> the structures NexStep stores.

Everything here is deterministic: age limits become date-of-birth
boundaries, accepted qualifications become an OR group, and so on.
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
from app.ai.extraction.facts import AgeLimit, DatesDraft, EligibilityDraft, Fact
from app.ai.extraction.grounding import Grounder

_LEVEL_ORDER = ["10th", "12th / Senior Secondary", "Diploma", "Bachelor's", "Master's", "PhD"]

_CATEGORY_WORDS = re.compile(
    r"\b(obc|sc|st|ews|pwd|pwbd|ph|women|female|male|reserved|category|ex-?servicem[ae]n|"
    r"relaxation|domicile|defence|handicapped|disab\w*)\b",
    re.IGNORECASE,
)

_DEMONYMS = {
    "indian": "India", "nepali": "Nepal", "nepalese": "Nepal", "bhutanese": "Bhutan",
    "bangladeshi": "Bangladesh", "sri lankan": "Sri Lanka", "pakistani": "Pakistan",
    "american": "United States", "british": "United Kingdom",
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def iso(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(normalize_any_date(value.strip()))
    except Exception:
        return None


def subtract_years(d: date, years: int) -> date:
    try:
        return d.replace(year=d.year - years)
    except ValueError:                     # 29 February
        return d.replace(year=d.year - years, day=28)


def canonical_country(name: str) -> str:
    cleaned = name.strip().strip(".")
    return _DEMONYMS.get(cleaned.lower(), cleaned)


# ---------------------------------------------------------------------------
# Exam dates
# ---------------------------------------------------------------------------

def compile_dates(draft: DatesDraft, g: Grounder, tba_hint: bool) -> dict:
    """Validate and ground every date. Returns ExamInformation date fields."""

    def scalar(fact: Fact, label: str) -> str | None:
        if not fact.value:
            return None
        parsed = iso(fact.value)
        if parsed is None:
            g.issue("warning", "date-unparsed", f"{label}: '{fact.value}' is not a valid date.", label)
            return None
        if not g.date_is_grounded(parsed):
            g.issue(
                "warning",
                "date-not-in-document",
                f"{label}: {parsed} does not appear anywhere in the document, so it was left empty.",
                label,
            )
            return None
        if not g.quote_backs_date(parsed, fact.quote):
            g.issue(
                "warning",
                "date-quote-mismatch",
                f"{label}: {parsed} is not the date written in the quoted text.",
                label,
            )
        g.support(label, fact.quote, fact.passage)
        return parsed.isoformat()

    start = scalar(draft.application_start_date, "Application start date")
    end = scalar(draft.application_end_date, "Application end date")
    late = scalar(draft.late_fee_end_date, "Late-fee application end date")

    if start is None and tba_hint:
        g.issue(
            "info",
            "start-tba",
            "The application start date is listed as 'to be announced' in the document.",
            "Application start date",
        )
    if late:
        g.issue(
            "info",
            "late-fee-deadline",
            f"Extended (late-fee) application deadline: {late}. Only the regular deadline is stored.",
            "Application end date",
        )
    if start and end and start > end:
        g.issue("error", "date-order", "Application start date is after the application end date.", "Application end date")

    ranges: list[ExamDateRange] = []
    seen: set[tuple[str, str]] = set()

    for item in draft.exam_dates:
        a, b = iso(item.start_date), iso(item.end_date)
        label = f"Exam date{f' ({item.label})' if item.label else ''}"

        if a is None or b is None:
            g.issue("warning", "date-unparsed", f"{label}: '{item.start_date} – {item.end_date}' is not a valid date range.", label)
            continue
        if a > b:
            a, b = b, a
            g.issue("warning", "date-swapped", f"{label}: start and end were reversed in the extraction and have been swapped.", label)

        missing = [d for d in (a, b) if not g.date_is_grounded(d)]
        if missing:
            g.issue(
                "warning",
                "date-not-in-document",
                f"{label}: {', '.join(str(m) for m in missing)} does not appear in the document; range dropped.",
                label,
            )
            continue

        key = (a.isoformat(), b.isoformat())
        if key in seen:
            continue
        seen.add(key)
        g.support(label, item.quote, item.passage)
        ranges.append(ExamDateRange(start_date=key[0], end_date=key[1]))

    ranges.sort(key=lambda r: r.start_date)

    if end and ranges and ranges[0].start_date < end:
        g.issue(
            "warning",
            "exam-before-deadline",
            "An exam date falls before the application end date; check the dates.",
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
    return not (limit.applies_to and _CATEGORY_WORDS.search(limit.applies_to))


def _expand_higher(levels: list[str], evidence_text: str) -> list[str]:
    """'…or a higher degree is also eligible' -> include all higher levels."""

    if not re.search(r"higher (degree|qualification)|degree higher|higher than", evidence_text, re.I):
        return levels
    known = [lvl for lvl in levels if lvl in _LEVEL_ORDER]
    if not known:
        return levels
    lowest = min(_LEVEL_ORDER.index(lvl) for lvl in known)
    return [*levels, *[lvl for lvl in _LEVEL_ORDER[lowest:] if lvl not in levels]]


def compile_eligibility(
    draft: EligibilityDraft,
    g: Grounder,
    context_text: str,
) -> tuple[EligibilityInformation, EligibilityRulesData]:
    rules: list[EligibilityRuleData] = []
    children: list[EligibilityRuleGroupData] = []
    other: list[str] = []

    # ---- age -> date of birth ------------------------------------------
    min_age = max_age = None
    general: dict[str, list[AgeLimit]] = {"minimum": [], "maximum": []}

    for limit in draft.age_limits:
        if limit.years <= 0 or limit.years > 120:
            g.issue("warning", "age-invalid", f"Ignored implausible age limit: {limit.years} years.", "Age limit")
            continue
        if _is_general(limit):
            general[limit.kind].append(limit)
        else:
            other.append(
                f"Age {limit.kind} {limit.years} years for {limit.applies_to}"
                + (f" (as on {limit.as_on_date})" if limit.as_on_date else "")
            )
            g.support(f"Age limit ({limit.applies_to})", limit.quote, limit.passage, required=False)

    for kind, limits in general.items():
        if not limits:
            continue

        distinct = {(l.years, l.as_on_date) for l in limits}
        chosen = limits[0]

        if len(distinct) > 1:
            g.conflict(
                f"Age limit ({kind})",
                [
                    ConflictOption(
                        value=f"{l.years} years" + (f" as on {l.as_on_date}" if l.as_on_date else ""),
                        source=(l.quote or "")[:160],
                        pages=g.passages[l.passage].pages if l.passage in g.passages else [],
                    )
                    for l in limits
                ],
                f"{chosen.years} years",
                "Provisionally using the first general limit found; verify against the document.",
            )

        ref = iso(chosen.as_on_date)
        label = f"Age limit ({kind})"

        if kind == "minimum":
            min_age = chosen.years
        else:
            max_age = chosen.years

        g.support(label, chosen.quote, chosen.passage)

        if ref is None:
            g.issue(
                "warning",
                "age-no-reference-date",
                f"The {kind} age of {chosen.years} years has no 'as on' date in the document, "
                "so no date-of-birth rule was created.",
                label,
            )
            continue
        if not g.date_is_grounded(ref):
            g.issue("warning", "date-not-in-document", f"{label}: reference date {ref} is not in the document.", label)
            continue

        if kind == "maximum":
            # age <= N on `ref`  <=>  born on or after (ref - (N+1) years) + 1 day
            boundary = subtract_years(ref, chosen.years + 1) + timedelta(days=1)
            rules.append(EligibilityRuleData(attribute="Date of Birth", operator=">=", value=boundary.isoformat()))
        else:
            boundary = subtract_years(ref, chosen.years)
            rules.append(EligibilityRuleData(attribute="Date of Birth", operator="<=", value=boundary.isoformat()))

    if draft.has_no_age_limit and not draft.age_limits:
        other.append("No age limit")

    # ---- qualifications: OR of accepted levels ---------------------------
    levels: list[str] = []
    fields: list[str] = []
    quals_text = ""

    for q in draft.qualifications:
        if q.level not in levels:
            levels.append(q.level)
        if q.field and q.field not in fields:
            fields.append(q.field)
        quals_text += " " + (q.quote or "")
        g.support(f"Qualification: {q.level}", q.quote, q.passage, required=False)

    levels = _expand_higher(levels, quals_text + " " + context_text)

    if levels:
        children.append(
            EligibilityRuleGroupData(
                logical_operator="OR",
                rules=[
                    EligibilityRuleData(attribute="Educational Qualification", operator="=", value=lvl)
                    for lvl in levels
                ],
            )
        )

    # ---- scores ----------------------------------------------------------
    if draft.minimum_percentage is not None:
        rules.append(EligibilityRuleData(attribute="Percentage", operator=">=", value=_num(draft.minimum_percentage)))
    if draft.minimum_cgpa is not None:
        rules.append(EligibilityRuleData(attribute="CGPA", operator=">=", value=_num(draft.minimum_cgpa)))
    if draft.minimum_percentage is not None or draft.minimum_cgpa is not None:
        g.support("Minimum score", draft.score_quote, draft.score_passage)

    # ---- nationality: OR of countries -------------------------------------
    countries = []
    for name in draft.nationalities:
        country = canonical_country(name)
        if country and country not in countries:
            countries.append(country)

    if countries:
        g.support("Nationality", draft.nationality_quote, draft.nationality_passage, required=False)
        children.append(
            EligibilityRuleGroupData(
                logical_operator="OR",
                rules=[EligibilityRuleData(attribute="Nationality", operator="=", value=c) for c in countries],
            )
        )

    # ---- work experience is informational: the evaluator only supports
    # text equality on it, so a numeric rule could never be evaluated.
    work = draft.work_experience.value
    if work:
        g.support("Work experience", draft.work_experience.quote, draft.work_experience.passage, required=False)

    for item in draft.other_requirements:
        text = item.text.strip()
        if text and text not in other:
            other.append(text)
            g.support(f"Requirement: {text[:40]}", item.quote, item.passage, required=False)

    info = EligibilityInformation(
        minimum_age=min_age,
        maximum_age=max_age,
        educational_qualification=(
            ", ".join(levels) + (f" ({'; '.join(fields)})" if fields else "") if levels else None
        ),
        nationality=", ".join(countries) or None,
        work_experience=work,
        other_requirements=other,
    )

    groups = []
    if rules or children:
        groups.append(
            EligibilityRuleGroupData(logical_operator="AND", rules=rules, child_groups=children)
        )

    return info, EligibilityRulesData(rule_groups=groups)


def _num(x: float) -> str:
    return str(int(x)) if float(x).is_integer() else str(x)
