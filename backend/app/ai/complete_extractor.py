import os

from dotenv import load_dotenv
from google import genai

from app.ai.exam_schemas import ExamInformation
from app.ai.schemas import EligibilityRulesData
from app.ai.extraction_schemas import CompleteExtractionData


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_complete_information(
    text: str,
    feedback: str | None = None
) -> CompleteExtractionData:

    feedback_instruction = ""

    if feedback:
        feedback_instruction = f"""
ADMINISTRATOR FEEDBACK FROM PREVIOUS REVIEW:

{feedback}

Use this feedback to carefully correct the extraction.

Re-examine the ORIGINAL document and make corrections
only when supported by the document.

Do not blindly follow the feedback if it contradicts
the official document.
"""

    prompt = f"""
You are extracting structured information from an official
examination document.

The output must contain:

1. Exam information
2. Eligibility rules

==================================================
GENERAL RULES
==================================================

- Extract only information explicitly supported by the
  official document.
- Do not invent or assume information.
- If information is unavailable, return null or an empty list.
- Preserve the meaning of the official document.
- Do not use outside knowledge.
- Do not infer requirements that are not explicitly stated.

{feedback_instruction}

==================================================
EXAM INFORMATION
==================================================

Extract:

- examination name
- conducting body
- notification/release date
- application start date
- application end date
- every examination date or date range
- eligibility information where explicitly stated

DATE RULES:

- Return dates in YYYY-MM-DD format.
- A single-day examination must use the same date for
  start_date and end_date.
- Consecutive examination dates should be represented
  as one date range.
- Separate examination periods must be represented as
  separate date ranges.
- Do not combine separate examination periods into one
  date range.

release_date means the date on which the official
notification/document was issued or released.

==================================================
ELIGIBILITY RULES
==================================================

Extract every explicitly stated eligibility requirement.

Use these attributes whenever applicable:

- CGPA
- Percentage
- Specialization
- Date of Birth
- Nationality
- State
- Educational Qualification
- Work Experience

Use ONLY these operators:

=
!=
>
>=
<
<=

NEVER use:

IN
==
approximately
unknown symbols
or any other operator.

If a requirement means equality, use:

=

Examples:

Educational Qualification = Graduate

Nationality = India

If a requirement says "at least", "minimum", or
"greater than or equal to", use:

>=

If a requirement says "at most", "maximum", or
"less than or equal to", use:

<=

==================================================
ALTERNATIVE VALUES
==================================================

If multiple values are acceptable for the SAME requirement,
represent them using an OR child group.

Example:

Nationality can be India, Nepal, or Bhutan.

Represent it as:

OR
    Nationality = India
    Nationality = Nepal
    Nationality = Bhutan

Do NOT use:

Nationality IN India, Nepal, Bhutan

==================================================
AND CONDITIONS
==================================================

If multiple requirements must ALL be satisfied,
place them in the same AND group.

Example:

Educational Qualification = Graduate
AND
CGPA >= 7.0

Represent it as:

AND
    Rule: Educational Qualification = Graduate
    Rule: CGPA >= 7.0

==================================================
NESTED LOGICAL CONDITIONS
==================================================

Represent eligibility as a logical tree.

A group may contain:

- rules
- child_groups

IMPORTANT:

If an OR condition is part of a larger AND condition,
the OR group MUST be a child_group of that AND group.

Example:

A candidate must:

- have a graduate degree
- AND be either an Indian, Nepali, or Bhutanese citizen

Correct representation:

Root Group: AND

    Rule:
        Educational Qualification = Graduate

    Child Group: OR

        Rule:
            Nationality = India

        Rule:
            Nationality = Nepal

        Rule:
            Nationality = Bhutan

DO NOT represent it as:

Group 1: AND
    Educational Qualification = Graduate

Group 2: OR
    Nationality = India
    Nationality = Nepal
    Nationality = Bhutan

The second representation is incorrect because it loses
the relationship between the AND and OR conditions.

==================================================
MORE COMPLEX EXAMPLE
==================================================

If the document requires:

Graduate degree

AND

(
    Indian citizen
    OR
    Nepali citizen
)

AND

(
    CGPA >= 7
    OR
    Percentage >= 70
)

represent it as:

AND
    Rule: Educational Qualification = Graduate

    Child Group: OR
        Rule: Nationality = India
        Rule: Nationality = Nepal

    Child Group: OR
        Rule: CGPA >= 7
        Rule: Percentage >= 70

Preserve the exact logical meaning of the document.

==================================================
DO NOT EXTRACT
==================================================

Do not include:

- application instructions
- application procedure
- fees
- syllabus
- examination instructions
- document submission instructions
- unrelated information

unless they are explicitly part of an eligibility requirement.

==================================================
OFFICIAL EXAMINATION DOCUMENT
==================================================

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CompleteExtractionData,
        },
    )

    return CompleteExtractionData.model_validate_json(
        response.text
    )