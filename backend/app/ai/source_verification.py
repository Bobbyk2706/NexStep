from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    Groq,
    RateLimitError,
)
from pydantic import BaseModel, ValidationError


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


class SourceVerificationResult(BaseModel):
    selected_url: str
    source_type: str
    relevant: bool


def _build_prompt(
    exam_name: str,
    sources: list[dict],
) -> str:

    source_information = []

    for source in sources:
        source_information.append(
            {
                "url": source.get("url"),
                "text": source.get("text", "")[:3000],
            }
        )

    return f"""
You are verifying official sources for an examination.

Exam name:
{exam_name}

Candidate sources:
{json.dumps(source_information, ensure_ascii=False)}

Select the single source that is most relevant to the
specified examination.

Rules:

1. Prefer an official source belonging to the conducting
   authority.

2. Prefer an official examination notification, notice,
   advertisement, or information document.

3. Do not select unrelated pages or documents.

4. Do not invent URLs.

5. selected_url MUST exactly match one of the candidate
   source URLs.

6. If no relevant source exists, return:

   selected_url = ""

   source_type = "NONE"

   relevant = false

7. Return JSON only.

"""


def _verify_once(
    exam_name: str,
    sources: list[dict],
) -> SourceVerificationResult:

    prompt = _build_prompt(
        exam_name=exam_name,
        sources=sources,
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict source verification "
                    "system. You may only select URLs that "
                    "appear in the supplied candidate list."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=512,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "source_verification",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "selected_url": {
                            "type": "string",
                        },
                        "source_type": {
                            "type": "string",
                        },
                        "relevant": {
                            "type": "boolean",
                        },
                    },
                    "required": [
                        "selected_url",
                        "source_type",
                        "relevant",
                    ],
                    "additionalProperties": False,
                },
            },
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError(
            "Groq returned an empty source-verification response."
        )

    try:
        return SourceVerificationResult.model_validate(
            json.loads(content)
        )
    except (
        json.JSONDecodeError,
        ValidationError,
    ) as exc:
        raise RuntimeError(
            "Groq returned source-verification data that "
            "failed validation."
        ) from exc


def verify_exam_source(
    exam_name: str,
    sources: list[dict],
) -> SourceVerificationResult:

    if not sources:
        return SourceVerificationResult(
            selected_url="",
            source_type="NONE",
            relevant=False,
        )

    try:
        result = _verify_once(
            exam_name=exam_name,
            sources=sources,
        )

    except RateLimitError:
        raise

    except (
        APIConnectionError,
        APITimeoutError,
    ):
        raise

    except APIStatusError:
        raise

    candidate_urls = {
        source.get("url")
        for source in sources
        if source.get("url")
    }

    if result.selected_url:
        if result.selected_url not in candidate_urls:
            raise RuntimeError(
                "Source verification returned a URL that was "
                "not present in the candidate source list."
            )

    else:
        result = SourceVerificationResult(
            selected_url="",
            source_type="NONE",
            relevant=False,
        )

    return result