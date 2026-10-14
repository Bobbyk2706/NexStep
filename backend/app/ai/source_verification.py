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

    for index, source in enumerate(sources, start=1):
        source_information.append(
            {
                "source_id": f"S{index}",
                "url": source.get("url"),
                "text": source.get("text", "")[:1000],
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

5. Return selected_source_id using the source_id field of one
   candidate (for example, "S1"). Do not copy or invent a URL.

6. If no relevant source exists, return selected_source_id = "".
   source_type = "NONE" and relevant = false.

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
            "selected_source_id": {
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
            "selected_source_id",
            "source_type",
            "relevant",
        ],
        "additionalProperties": False,
    }

    # ========================================================
    # VALIDATOR
    # ========================================================

    source_by_id = {
        f"S{index}": source
        for index, source in enumerate(sources, start=1)
        if source.get("url")
    }

    def validate_response(
        content: str,
    ) -> SourceVerificationResult:
        """Validate the selected candidate ID and map it to its original URL."""
        try:
            payload = json.loads(content)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Source verification did not return valid JSON.") from exc

        if not isinstance(payload, dict):
            raise ValueError("Source verification response must be a JSON object.")

        source_id = str(payload.get("selected_source_id") or "").strip()
        if not source_id:
            return SourceVerificationResult(
                selected_url="",
                source_type="NONE",
                relevant=False,
            )

        source = source_by_id.get(source_id)
        if source is None:
            raise ValueError(
                "Source verification selected an ID that was not in the candidate list."
            )

        return SourceVerificationResult(
            selected_url=source["url"],
            source_type=str(payload.get("source_type") or "OFFICIAL"),
            relevant=bool(payload.get("relevant", False)),
        )

    # ========================================================
    # PROVIDER CHAIN
    # ========================================================

    try:
        result = _provider_manager.generate(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict source verification system. "
                        "Select only a source_id present in the supplied candidate list. "
                        "Never invent a source ID or URL."
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
            max_tokens=1024,
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
