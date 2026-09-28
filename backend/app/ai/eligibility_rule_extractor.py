from __future__ import annotations

from copy import deepcopy

from app.ai.eligibility_schemas import EligibilityRulesData
from app.ai.provider_manager import (
    AIProviderManager,
    AllAIProvidersFailedError,
)


# ============================================================
# CONFIGURATION
# ============================================================

# Groq currently has a very small TPM allowance for this model.
# Keep the request comfortably below the limit because token
# consumption depends on the actual text density.
CHUNK_SIZE = 16000

# Number of task-level attempts.
#
# Each attempt itself goes through the complete provider chain:
#
#     Groq → OpenRouter → Local
#
# The provider classes handle their own infrastructure retries.
MAX_ATTEMPTS = 2


# ============================================================
# PROVIDER MANAGER
# ============================================================

_provider_manager = AIProviderManager()


# ============================================================
# TEXT CHUNKING
# ============================================================


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


# ============================================================
# PROMPT
# ============================================================


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


# ============================================================
# STRICT RETRY PROMPT
# ============================================================


def _make_retry_prompt(text: str) -> str:
    return f"""
The previous eligibility-rule extraction response was invalid
or could not be validated against the required schema.

Retry the extraction for the SAME official document chunk.

Return ONLY valid JSON matching the supplied response schema.

IMPORTANT:

1. Extract only eligibility requirements explicitly supported
   by the supplied text.

2. Do not use outside knowledge.

3. Do not invent or assume requirements.

4. Use only these attributes:

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

6. Do NOT use IN.

7. Multiple acceptable values must be represented with an
   OR child group.

8. Requirements that must all be satisfied must be represented
   with an AND group.

9. Preserve explicitly stated nested logical relationships.

10. Do not include application instructions, exam dates,
    syllabus, fees, document submission instructions,
    or unrelated information.

11. If this chunk contains no eligibility requirements,
    return an empty rule tree.

12. Do not infer requirements from information that is not
    present in this chunk.

13. Return ONLY the structured JSON response.

OFFICIAL DOCUMENT CHUNK:

{text}
"""


# ============================================================
# SINGLE-CHUNK EXTRACTION
# ============================================================


def _extract_single_chunk(
    text: str,
) -> EligibilityRulesData:
    """
    Extract eligibility rules from one bounded document chunk.

    Each task-level attempt uses the complete provider chain:

        Groq → OpenRouter → Local

    Provider-specific API retries are handled by the provider
    implementations.

    Pydantic validation happens here so the provider manager can
    reject malformed structured output and move to the next
    provider.
    """

    response_schema = (
        EligibilityRulesData.model_json_schema()
    )

    def validate_response(
        content: str,
    ) -> EligibilityRulesData:
        """
        Validate the raw provider response against the
        application's authoritative Pydantic model.
        """

        return EligibilityRulesData.model_validate_json(
            content
        )

    prompt = _make_prompt(text)

    last_error: Exception | None = None

    for attempt in range(MAX_ATTEMPTS):
        current_prompt = (
            prompt
            if attempt == 0
            else _make_retry_prompt(text)
        )

        try:
            result = _provider_manager.generate(
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
                        "content": current_prompt,
                    },
                ],
                response_schema=response_schema,
                validator=validate_response,
                temperature=0.0,
                max_tokens=4096,
            )

            if not isinstance(
                result,
                EligibilityRulesData,
            ):
                raise RuntimeError(
                    "AI provider manager returned an unexpected "
                    "eligibility-rule extraction result."
                )

            return result

        except AllAIProvidersFailedError as exc:
            last_error = exc

            # If this was the final task-level attempt,
            # preserve the failure context.
            if attempt == MAX_ATTEMPTS - 1:
                break

    raise RuntimeError(
        "Eligibility-rule extraction failed after "
        f"{MAX_ATTEMPTS} provider-chain attempts."
    ) from last_error


# ============================================================
# RESULT MERGING
# ============================================================


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


# ============================================================
# PUBLIC EXTRACTION FUNCTION
# ============================================================


def extract_eligibility_rules(
    text: str,
) -> EligibilityRulesData:
    """
    Extract eligibility rules from a document of arbitrary size.

    Large documents are split into bounded chunks so that a
    single request cannot exceed the configured chunk size.

    Each chunk is processed independently through the AI
    provider fallback chain.
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