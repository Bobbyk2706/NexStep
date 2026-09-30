from __future__ import annotations

"""
What the LLM is asked to return.

The schemas are deliberately flat and simple (a small model must be able
to fill them in). The model reports FACTS, each with the passage id and a
verbatim quote it came from. Turning facts into eligibility rules, and
age limits into date-of-birth boundaries, is done in Python (compiler.py),
because that logic is deterministic and models are unreliable at it.
"""

from typing import Any, Literal

from pydantic import BaseModel, Field

QualLevel = Literal[
    "10th",
    "12th / Senior Secondary",
    "Diploma",
    "Bachelor's",
    "Master's",
    "PhD",
    "Other",
]


class Fact(BaseModel):
    value: str | None = None
    quote: str | None = None        # verbatim text from the passage
    passage: str | None = None      # passage id, e.g. "P12"


class IdentityDraft(BaseModel):
    exam_name: Fact
    conducting_body: Fact
    release_date: Fact


class DateRangeFact(BaseModel):
    label: str | None = None        # e.g. "Week 1", "Paper A"
    start_date: str
    end_date: str
    quote: str | None = None
    passage: str | None = None


class DatesDraft(BaseModel):
    application_start_date: Fact
    application_end_date: Fact
    late_fee_end_date: Fact
    exam_dates: list[DateRangeFact] = Field(default_factory=list)


class AgeLimit(BaseModel):
    kind: Literal["minimum", "maximum"]
    years: int
    applies_to: str | None = None   # "all candidates", "OBC", ...
    as_on_date: str | None = None   # reference date, YYYY-MM-DD
    quote: str | None = None
    passage: str | None = None


class QualificationFact(BaseModel):
    level: QualLevel
    field: str | None = None        # e.g. "Engineering/Technology"
    quote: str | None = None
    passage: str | None = None


class TextItem(BaseModel):
    text: str
    quote: str | None = None
    passage: str | None = None


class EligibilityDraft(BaseModel):
    has_no_age_limit: bool = False
    age_limits: list[AgeLimit] = Field(default_factory=list)
    qualifications: list[QualificationFact] = Field(default_factory=list)
    minimum_percentage: float | None = None
    minimum_cgpa: float | None = None
    score_quote: str | None = None
    score_passage: str | None = None
    nationalities: list[str] = Field(default_factory=list)
    nationality_quote: str | None = None
    nationality_passage: str | None = None
    work_experience: Fact
    other_requirements: list[TextItem] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# JSON schema helpers
# ---------------------------------------------------------------------------

def inline_schema(model: type[BaseModel]) -> dict[str, Any]:
    """
    JSON schema with every $ref inlined. Providers differ in how well
    they support $defs/$ref in structured output; a self-contained
    schema works everywhere.
    """

    schema = model.model_json_schema()
    defs = schema.pop("$defs", {})

    def resolve(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node:
                name = node["$ref"].rsplit("/", 1)[-1]
                return resolve(dict(defs[name]))
            return {
                key: resolve(value)
                for key, value in node.items()
                if key not in {"title", "default"}
            }
        if isinstance(node, list):
            return [resolve(item) for item in node]
        return node

    return resolve(schema)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You extract facts from an official examination notification. "
    "Use ONLY the supplied passages. Never use outside knowledge and never "
    "guess. If a fact is not stated, use null (or an empty list). "
    "Every fact must include the passage id and a short VERBATIM quote "
    "(at most 25 words) copied from that passage. "
    "Return one JSON object and nothing else."
)

_COMMON_RULES = """\
General rules:
- Dates: YYYY-MM-DD. If the passage says a date is 'to be announced' or gives no date, use null.
- Ignore values marked as superseded, cancelled or replaced.
- Do not copy a date unless it is written in a passage."""

IDENTITY_TASK = """\
Task: identify the examination.
- exam_name: the official name of the examination including the year/edition (e.g. 'GATE 2027').
- conducting_body: the organisation that conducts or organises it.
- release_date: the date this notification/brochure was issued or last revised, if stated.
""" + _COMMON_RULES

DATES_TASK = """\
Task: extract the schedule.
- application_start_date: when online registration/applications open (regular period).
- application_end_date: last date to apply in the REGULAR period.
- late_fee_end_date: last date to apply in the extended / late-fee period, if any.
- exam_dates: every examination date. A range (start_date to end_date) for consecutive days;
  for a single day use the same date for both. Separate sessions/weeks are separate items.
  Do not include dates of results, admit cards, or application periods here.
""" + _COMMON_RULES

ELIGIBILITY_TASK = """\
Task: extract who may apply.
- age_limits: one item per age limit. kind is 'minimum' or 'maximum'. Give as_on_date (the date age is
  counted on) only if the passage states it. Include limits for special categories with applies_to.
  If the notification says there is no age limit, set has_no_age_limit true.
- qualifications: each accepted educational level (alternatives). level must be one of the allowed
  values; put the subject area in field.
- minimum_percentage / minimum_cgpa: only if a minimum score is required.
- nationalities: countries whose citizens may apply (e.g. ['India']); empty if not restricted.
- work_experience: required work experience, if any.
- other_requirements: other conditions worth showing an administrator (attempt limits, year of study,
  category conditions...). Keep each item short.
""" + _COMMON_RULES


def build_messages(task: str, context: str, feedback: str | None) -> list[dict[str, str]]:
    parts = [task]

    if feedback:
        parts.append(
            "Administrator feedback about a previous attempt (guidance only, NOT evidence; "
            "verify everything against the passages):\n" + feedback.strip()
        )

    parts.append("PASSAGES:\n" + context)

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "\n\n".join(parts)},
    ]
