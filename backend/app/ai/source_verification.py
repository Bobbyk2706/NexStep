from __future__ import annotations

import json

from pydantic import BaseModel

from app.ai.provider_manager import (
    AIProviderManager,
    AllAIProvidersFailedError,
)


# ============================================================
# RESULT MODEL
# ============================================================


class SourceVerificationResult(BaseModel):
    selected_url: str
    source_type: str
    relevant: bool


# ============================================================
# PROVIDER MANAGER
# ============================================================

_provider_manager = AIProviderManager()


# ============================================================
# PROMPT
# ============================================================


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


# ============================================================
# SOURCE VERIFICATION
# ============================================================


def verify_exam_source(
    exam_name: str,
    sources: list[dict],
) -> SourceVerificationResult:
    """
    Select the most relevant official source for an exam.

    The provider chain is:

        Groq → OpenRouter → Local Ollama

    A provider response is accepted only if:

        1. It is valid SourceVerificationResult JSON.
        2. selected_url is empty OR exactly matches one of the
           supplied candidate URLs.

    If a provider violates the URL constraint, the next provider
    is attempted.
    """

    # ========================================================
    # EMPTY SOURCE LIST
    # ========================================================

    if not sources:
        return SourceVerificationResult(
            selected_url="",
            source_type="NONE",
            relevant=False,
        )

    # ========================================================
    # CANDIDATE URL SET
    # ========================================================

    candidate_urls = {
        source.get("url")
        for source in sources
        if source.get("url")
    }

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = _build_prompt(
        exam_name=exam_name,
        sources=sources,
    )

    # ========================================================
    # RESPONSE SCHEMA
    # ========================================================

    response_schema = {
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
    }

    # ========================================================
    # VALIDATOR
    # ========================================================

    def validate_response(
        content: str,
    ) -> SourceVerificationResult:
        """
        Validate both the JSON structure and the critical
        candidate-URL safety invariant.
        """

        result = SourceVerificationResult.model_validate_json(
            content
        )

        # ----------------------------------------------------
        # NO SOURCE SELECTED
        # ----------------------------------------------------

        if not result.selected_url:
            return SourceVerificationResult(
                selected_url="",
                source_type="NONE",
                relevant=False,
            )

        # ----------------------------------------------------
        # URL MUST COME FROM CANDIDATE LIST
        # ----------------------------------------------------

        if result.selected_url not in candidate_urls:
            raise ValueError(
                "Source verification returned a URL that was "
                "not present in the candidate source list."
            )

        return result

    # ========================================================
    # PROVIDER CHAIN
    # ========================================================

    try:
        result = _provider_manager.generate(
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
            response_schema=response_schema,
            validator=validate_response,
            temperature=0.0,
            max_tokens=512,
        )

    except AllAIProvidersFailedError as exc:
        raise RuntimeError(
            "Source verification failed because all configured "
            "AI providers failed or returned invalid source "
            "verification data."
        ) from exc

    # ========================================================
    # SAFETY CHECK
    # ========================================================

    if not isinstance(
        result,
        SourceVerificationResult,
    ):
        raise RuntimeError(
            "Source verification returned an unexpected "
            "result type."
        )

    return result