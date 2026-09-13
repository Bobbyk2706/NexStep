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

Return the requirements as a structured logical rule tree.

Rules:

1. Extract only eligibility requirements that are explicitly
   supported by the document.

2. Do not invent or assume requirements.

3. Use these attribute names when applicable:
   CGPA
   Percentage
   Specialization
   Date of Birth
   Nationality
   State
   Educational Qualification
   Work Experience

4. Use only these operators:
   =
   !=
   >
   >=
   <
   <=

5. Do NOT use the IN operator.

6. If the document says that an attribute can have multiple
   acceptable values, represent those alternatives using an
   OR child group.

   Example:

   Nationality can be India, Nepal, or Bhutan

   becomes:

   OR
   ├── Nationality = India
   ├── Nationality = Nepal
   └── Nationality = Bhutan

7. If multiple requirements must all be satisfied, use an
   AND group.

   Example:

   Education = Graduate
   AND
   CGPA >= 7.0

8. Use child_groups whenever nested logical conditions are
   required.

   Example:

   Education = Graduate
   AND
   (
       Nationality = India
       OR
       Nationality = Nepal
   )

   should be represented as:

   Root group: AND
       Rule: Education = Graduate
       Child group: OR
           Rule: Nationality = India
           Rule: Nationality = Nepal

9. Preserve the logical meaning of the official document.

10. Extract every explicitly stated eligibility requirement.

11. Do not include:
    - application instructions
    - exam dates
    - syllabus
    - fees
    - document submission instructions
    - unrelated information

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