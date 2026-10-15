from __future__ import annotations

"""
What the LLM is asked to return.

The schemas are deliberately flat and simple (a small model must be able
to fill them in). The model reports FACTS, each with the passage id and a
verbatim quote it came from. Turning facts into eligibility rules, and
age limits into date-of-birth boundaries, is done in Python (compiler.py),
because that logic is deterministic and models are unreliable at it.

Important grounding rule:

Every extracted examination date MUST include:
    - the passage id where the date was found
    - a short verbatim quote from that passage

This is enforced by the schema instead of relying only on the prompt.
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
    quote: str | None = None
    passage: str | None = None


class IdentityDraft(BaseModel):
    exam_name: Fact
    conducting_body: Fact
    release_date: Fact


class DateRangeFact(BaseModel):
    """
    One examination date/range.

    Unlike generic Fact objects, quote and passage are REQUIRED here.

    If the model cannot provide source evidence for an examination date,
    it should NOT create a DateRangeFact for that date.
    """

    label: str | None = None

    start_date: str
    end_date: str

    quote: str = Field(
        min_length=1,
        description=(
            "Short verbatim quote copied from the supplied passage. "
            "The quote must contain the examination date or date range."
        ),
    )

    passage: str = Field(
        min_length=1,
        description=(
            "ID of the supplied passage containing the quoted examination date."
        ),
    )


class DatesDraft(BaseModel):
    application_start_date: Fact
    application_end_date: Fact
    late_fee_end_date: Fact
    exam_dates: list[DateRangeFact] = Field(default_factory=list)


class AgeLimit(BaseModel):
    kind: Literal["minimum", "maximum"]
    years: int
    applies_to: str | None = None
    as_on_date: str | None = None
    quote: str | None = None
    passage: str | None = None


class QualificationFact(BaseModel):
    level: QualLevel
    field: str | None = None
    quote: str | None = None
    passage: str | None = None


class TextItem(BaseModel):
    text: str
    quote: str | None = None
    passage: str | None = None


class EligibilityDraft(BaseModel):
    has_no_age_limit: bool = False

    age_limits: list[AgeLimit] = Field(
        default_factory=list
    )

    qualifications: list[QualificationFact] = Field(
        default_factory=list
    )

    minimum_percentage: float | None = None
    minimum_cgpa: float | None = None

    score_quote: str | None = None
    score_passage: str | None = None

    nationalities: list[str] = Field(
        default_factory=list
    )

    nationality_quote: str | None = None
    nationality_passage: str | None = None

    work_experience: Fact

    other_requirements: list[TextItem] = Field(
        default_factory=list
    )


# ---------------------------------------------------------------------------
# JSON schema helpers
# ---------------------------------------------------------------------------

def inline_schema(model: type[BaseModel]) -> dict[str, Any]:
    """
    JSON schema with every $ref inlined.

    Providers differ in how well they support $defs/$ref in structured
    output. A self-contained schema works more reliably across providers.
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
    "Every extracted fact must be traceable to the supplied passages. "
    "Every fact that has a value must include the passage id and a short "
    "VERBATIM quote copied from that passage. "
    "For examination dates this requirement is mandatory: never return an "
    "exam_dates item without both passage and quote. If you cannot provide "
    "a source quote for an examination date, do not return that date as an "
    "exam_dates item. "
    "Return one JSON object and nothing else."
)


_COMMON_RULES = """\
General rules:
- Dates: YYYY-MM-DD.
- If the passage says a date is 'to be announced' or gives no date, use null.
- Ignore values marked as superseded, cancelled or replaced.
- Do not copy a date unless it is written in a supplied passage.
- Never invent a passage id.
- Never invent a quotation.
"""


IDENTITY_TASK = """\
Task: identify the examination.

- exam_name: the official name of the examination including the year/edition
  (e.g. 'GATE 2027').
- conducting_body: the organisation that conducts or organises it.
- release_date: the date this notification/brochure was issued or last revised,
  if stated.
""" + _COMMON_RULES


DATES_TASK = """\
Task: extract the schedule.

- application_start_date: when online registration/applications open
  (regular period).
- application_end_date: last date to apply in the REGULAR period.
- late_fee_end_date: last date to apply in the extended / late-fee period,
  if any.

Read schedule tables and labelled lines together: a date may appear on a
separate line from "opening", "closing", "regular period", or "late fee".
Copy the date and quote the shortest supplied text that connects it to the
correct application event. If the notice explicitly says the start date is
"to be announced", leave application_start_date null; do not substitute a
superseded date.

- exam_dates: every actual examination date stated in the supplied passages.

For exam_dates:

1. A consecutive multi-day examination must be represented as one range.
2. A single examination day must use the same date for start_date and end_date.
3. Separate sessions, papers, stages, weeks, or non-consecutive examination
   periods should be represented as separate items when the notification
   distinguishes them.
4. Do NOT include dates of results, answer keys, admit cards, application
   periods, interviews, counselling, or other non-examination events.
5. Every exam_dates item MUST contain:
   - start_date
   - end_date
   - passage
   - quote
6. The quote MUST be copied VERBATIM from the supplied passage.
7. The quote MUST contain the examination date or date range supporting the
   extracted start_date/end_date.
8. The passage MUST be the exact passage id containing that quote.
9. Never create an exam_dates item with quote=null, quote="", passage=null,
   or passage="".
10. If an examination date is visible but you cannot provide both a valid
    passage id and a verbatim supporting quote, OMIT that exam_dates item
    instead of guessing.

Example of the required structure:

{
  "label": "Civil Services Preliminary Examination",
  "start_date": "2025-05-25",
  "end_date": "2025-05-25",
  "quote": "The Civil Services (Preliminary) Examination, 2025 will be held on 25.05.2025.",
  "passage": "P12"
}

The quote above is only an example of the format. Do not copy the example
as evidence. Use only quotes from the supplied passages.
""" + _COMMON_RULES


ELIGIBILITY_TASK = """\
Task: extract who may apply.

Every item below needs "passage" (the id of the passage it came from) and
"quote" (a short sentence copied word for word from that passage). An item
without a quote cannot be used, so leave it out instead of guessing.

- age_limits: one item per age limit.
  kind is 'minimum' or 'maximum'.
  years is the number exactly as written in the notice. Copy it; do not
  add or subtract anything. ("must not have attained the age of 32 years"
  -> years = 32.)
  as_on_date: the date age is counted on, only if the passage states it.
  applies_to: leave null ONLY for the limit that applies to every
  candidate. Any limit or concession that applies to a particular group
  (SC, ST, OBC, EWS, persons with disabilities, ex-servicemen, defence
  personnel, government servants, women, ...) must name that group in
  applies_to. If a concession is written as "up to five years in the case
  of ...", report the resulting age for that group (general limit plus the
  concession) with applies_to set to the group.

- qualifications: each accepted educational level (alternatives).
  level must be one of the allowed values.
  Put the subject area in field.
  quote: the sentence that names the qualification.
  Inspect eligibility prose, tables, and continuation passages. If the
  notice states who is eligible by education or current year of study,
  include that qualification even when it appears in a table or is phrased
  as a degree-equivalence rule. Do not leave qualifications empty when an
  explicit educational requirement is present in the supplied passages.

- minimum_percentage / minimum_cgpa:
  only if a minimum score is required.
  score_quote / score_passage: the sentence stating it.

- nationalities:
  names of countries only, one per entry (e.g. ['India', 'Nepal',
  'Bhutan']). Do not put conditions or descriptions here: "persons of
  Indian origin who migrated from ...", refugee conditions and similar
  wording belong in other_requirements. Empty if not restricted.
  nationality_quote / nationality_passage: the sentence that lists who
  may apply.

- work_experience:
  required work experience, if any.

- other_requirements:
  other conditions worth showing an administrator
  (attempt limits, year of study, category conditions, dates of birth
  written out in the notice, etc.). Keep each item short, and keep every
  number exactly as the notice writes it.
""" + _COMMON_RULES


def build_messages(
    task: str,
    context: str,
    feedback: str | None,
) -> list[dict[str, str]]:
    parts = [task]

    if feedback:
        parts.append(
            "Administrator feedback about a previous attempt "
            "(guidance only, NOT evidence; verify everything against "
            "the passages):\n"
            + feedback.strip()
        )

    parts.append(
        "PASSAGES:\n" + context
    )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "\n\n".join(parts),
        },
    ]
