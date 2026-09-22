from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from app.ai.eligibility_schemas import EligibilityRulesData


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


def extract_eligibility_rules(
    text: str,
) -> EligibilityRulesData:

    prompt = f"""
Extract the eligibility requirements from the following
official examination document.

Return the requirements as a structured logical rule tree.

Rules:

1. Extract only eligibility requirements explicitly supported
   by the document.

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

6. If an attribute can have multiple acceptable values,
   represent those alternatives using an OR child group.

7. If multiple requirements must all be satisfied,
   use an AND group.

8. Use child_groups whenever nested logical conditions
   are required.

9. Preserve the logical meaning of the official document.

10. Extract every explicitly stated eligibility requirement.

11. Do not include:

    - application instructions
    - exam dates
    - syllabus
    - fees
    - document submission instructions
    - unrelated information

OFFICIAL EXAMINATION DOCUMENT:

{text}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict eligibility-rule extraction "
                    "system. Extract only requirements explicitly "
                    "supported by the supplied official document."
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
                "name": "eligibility_rules",
                "strict": False,
                "schema": EligibilityRulesData.model_json_schema(),
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty response."
        )

    try:
        return EligibilityRulesData.model_validate(
            json.loads(content)
        )
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError(
            "Groq returned eligibility rules that failed validation."
        ) from exc