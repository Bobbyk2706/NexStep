import os

from dotenv import load_dotenv
from google import genai

from app.ai.eligibility_schemas import EligibilityRulesData


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_eligibility_rules(
    text: str
) -> EligibilityRulesData:

    prompt = f"""
Extract the eligibility requirements from the following
official examination document.

Return only eligibility requirements that are explicitly
supported by the document.

Rules:
- Do not invent or assume requirements.
- Convert each requirement into a structured rule.
- Use these attribute names when applicable:
  CGPA
  Percentage
  Specialization
  Date of Birth
  Nationality
  State
  Educational Qualification
  Work Experience
- Use clear operators such as:
  =
  !=
  >
  >=
  <
  <=
  IN
- Keep the value as a string.
- If multiple rules must ALL be satisfied, put them in
  the same group with logical_operator = "AND".
- If alternatives exist, use separate groups where
  appropriate.
- Extract every explicitly stated eligibility requirement.
- Do not include application instructions, exam dates,
  syllabus, fees, or unrelated information.

Official examination document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": EligibilityRulesData,
        },
    )

    return EligibilityRulesData.model_validate_json(
        response.text
    )