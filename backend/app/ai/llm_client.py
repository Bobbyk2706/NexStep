import os

from dotenv import load_dotenv
from google import genai

from app.ai.schemas import ExamInformation

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_exam_information(
    text: str,
    feedback: str | None = None
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

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ExamInformation,
        },
    )

    return ExamInformation.model_validate_json(
        response.text
    )