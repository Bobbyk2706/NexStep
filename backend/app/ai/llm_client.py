from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from app.ai.exam_schemas import ExamInformation


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured."
    )


client = Groq(
    api_key=GROQ_API_KEY,
)


MODEL_NAME = "openai/gpt-oss-120b"


def extract_exam_information(
    text: str,
    feedback: str | None = None,
) -> ExamInformation:

    feedback_instruction = ""

    if feedback:
        feedback_instruction = f"""
Administrator feedback from the previous review:

{feedback}

Use this feedback to carefully correct the extraction.
Re-examine the original document and make corrections
only when supported by the document.
"""

    prompt = f"""
Extract exam information from the following official
exam document.

Rules:

- Extract only information explicitly present in the document.
- Do not invent or assume missing information.
- If a field is not available, return null.
- Return dates in YYYY-MM-DD format when possible.
- release_date means the date the official notification/document
  was issued or released.
- exam_dates must contain every examination date or date range
  explicitly stated in the document.
- For a single-day examination, use the same date for start_date
  and end_date.
- For an examination spanning multiple consecutive days, use one
  date range.
- If the examination occurs on separate groups of dates, return
  multiple date ranges.
- Do not combine multiple dates into a text string.

{feedback_instruction}

ORIGINAL OFFICIAL DOCUMENT:

{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict information extraction system. "
                    "Extract only information explicitly supported "
                    "by the supplied official document."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "exam_information",
                "strict": False,
                "schema": ExamInformation.model_json_schema(),
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    try:
        return ExamInformation.model_validate(
            json.loads(content)
        )
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(
            "Groq returned exam data that failed validation."
        ) from exc