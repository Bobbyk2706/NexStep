import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class SourceVerificationResult(BaseModel):
    selected_url: str
    source_type: str
    relevant: bool


def verify_exam_source(
    exam_name: str,
    sources: list[dict]
) -> SourceVerificationResult:

    source_information = []

    for source in sources:
        source_information.append({
            "url": source.get("url"),
            "text": source.get("text", "")[:3000]
        })

    prompt = f"""
You are verifying official sources for an examination.

Exam name:
{exam_name}

Candidate sources:
{source_information}

Select the single source that is most relevant to the specified examination.

Rules:
- Prefer an official source belonging to the conducting authority.
- Prefer an official examination notification, notice, advertisement, or information document.
- Do not select unrelated pages or documents.
- Do not invent URLs.
- selected_url must exactly match one of the candidate source URLs.
- If no relevant source exists, return selected_url as an empty string.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": SourceVerificationResult,
        },
    )

    return SourceVerificationResult.model_validate_json(
        response.text
    )