from __future__ import annotations

import json
import os
from copy import deepcopy

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    Groq,
    RateLimitError,
)
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

# Groq currently has a very small TPM allowance for this model.
# Keep the request comfortably below the limit because token
# consumption depends on the actual text density.
CHUNK_SIZE = 16000

MAX_RETRIES = 2


def _chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
) -> list[str]:
    """
    Split a large document into deterministic chunks.

    Prefer paragraph boundaries so that requirements are less
    likely to be split in the middle of a sentence.
    """

    if not text or not text.strip():
        return []

    text = text.strip()

    if len(text) <= chunk_size:
        return [text]

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[str] = []
    current: list[str] = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)

        if paragraph_length > chunk_size:
            if current:
                chunks.append("\n\n".join(current))
                current = []
                current_length = 0

            start = 0

            while start < paragraph_length:
                end = min(
                    start + chunk_size,
                    paragraph_length,
                )

                chunks.append(paragraph[start:end])
                start = end

            continue

        separator_length = 2 if current else 0

        if (
            current
            and current_length
            + separator_length
            + paragraph_length
            > chunk_size
        ):
            chunks.append("\n\n".join(current))
            current = []
            current_length = 0

            separator_length = 0

        current.append(paragraph)

        current_length += (
            separator_length + paragraph_length
        )

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _make_prompt(text: str) -> str:
    return f"""
Extract the eligibility requirements from the following
official examination document chunk.

Return the requirements as a structured logical rule tree.

Rules:

1. Extract only eligibility requirements explicitly supported
   by the supplied text.

2. Do not use outside knowledge.

3. Do not invent or assume requirements.

4. Use these attribute names when applicable:

   CGPA
   Percentage
   Specialization
   Date of Birth
   Nationality
   State
   Educational Qualification
   Work Experience

5. Use only these operators:

   =
   !=
   >
   >=
   <
   <=

6. Do NOT use the IN operator.

7. If an attribute can have multiple acceptable values,
   represent those alternatives using an OR child group.

8. If multiple requirements must all be satisfied,
   use an AND group.

9. Use child_groups whenever nested logical conditions
   are required.

10. Preserve the logical meaning explicitly stated in
    this document chunk.

11. Extract every explicitly stated eligibility requirement
    present in this chunk.

12. Do not include:

    - application instructions
    - exam dates
    - syllabus
    - fees
    - document submission instructions
    - unrelated information

13. A chunk may contain no eligibility requirements.
    In that case return an empty rule tree.

IMPORTANT:

This is only one chunk of a larger official document.
Do not infer requirements from information that is not
present in this chunk.

OFFICIAL DOCUMENT CHUNK:

{text}
"""


def _extract_single_chunk(
    text: str,
) -> EligibilityRulesData:

    prompt = _make_prompt(text)

    last_error: Exception | None = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict eligibility-rule "
                            "extraction system. Extract only "
                            "requirements explicitly supported "
                            "by the supplied document text. "
                            "Never invent information."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
                max_tokens=4096,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "eligibility_rules",
                        "strict": False,
                        "schema": (
                            EligibilityRulesData
                            .model_json_schema()
                        ),
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
            except (
                json.JSONDecodeError,
                ValidationError,
            ) as exc:
                raise RuntimeError(
                    "Groq returned eligibility rules that "
                    "failed validation."
                ) from exc

        except RateLimitError as exc:
            last_error = exc

        except (
            APIConnectionError,
            APITimeoutError,
        ) as exc:
            last_error = exc

        except APIStatusError as exc:
            if exc.status_code == 413:
                raise RuntimeError(
                    "Eligibility-rule extraction chunk is "
                    "too large for the configured Groq TPM "
                    "limit. Reduce CHUNK_SIZE."
                ) from exc

            raise

    raise RuntimeError(
        "Groq eligibility-rule extraction failed after "
        f"{MAX_RETRIES + 1} attempts."
    ) from last_error


def _merge_results(
    results: list[EligibilityRulesData],
) -> EligibilityRulesData:
    """
    Merge independently extracted rule trees.

    Rule groups from different chunks are preserved rather
    than attempting to reconstruct logical relationships
    across arbitrary chunk boundaries.
    """

    if not results:
        return EligibilityRulesData(
            rule_groups=[]
        )

    merged = deepcopy(results[0])

    for result in results[1:]:
        existing_groups = getattr(
            merged,
            "rule_groups",
            [],
        )

        new_groups = getattr(
            result,
            "rule_groups",
            [],
        )

        existing_serialized = {
            group.model_dump_json()
            for group in existing_groups
        }

        for group in new_groups:
            serialized = group.model_dump_json()

            if serialized not in existing_serialized:
                existing_groups.append(group)
                existing_serialized.add(serialized)

        merged.rule_groups = existing_groups

    return merged


def extract_eligibility_rules(
    text: str,
) -> EligibilityRulesData:
    """
    Extract eligibility rules from a document of arbitrary size.

    Large documents are split into bounded chunks so that a
    single request cannot exceed the Groq TPM limit.
    """

    chunks = _chunk_text(text)

    if not chunks:
        return EligibilityRulesData(
            rule_groups=[]
        )

    results: list[EligibilityRulesData] = []

    for index, chunk in enumerate(chunks, start=1):
        try:
            result = _extract_single_chunk(chunk)
        except Exception as exc:
            raise RuntimeError(
                "Eligibility-rule extraction failed for "
                f"chunk {index}/{len(chunks)}."
            ) from exc

        results.append(result)

    return _merge_results(results)