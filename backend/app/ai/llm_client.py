import os

from dotenv import load_dotenv
from google import genai

from app.ai.schemas import ExamInformation

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_exam_information(text: str) -> ExamInformation:
    prompt = f"""
Extract exam information from the following official exam document.

Rules:
- Extract only information explicitly present in the document.
- Do not invent or assume missing information.
- If a field is not available, return null.
- Return the dates in YYYY-MM-DD format when possible.

Document:
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

    return ExamInformation.model_validate_json(response.text)