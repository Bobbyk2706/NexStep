from __future__ import annotations

from app.ai.exam_schemas import ExamInformation
from app.ai.provider_manager import (
    AIProviderManager,
    AllAIProvidersFailedError,
)


# ============================================================
# PROVIDER MANAGER
# ============================================================

_provider_manager = AIProviderManager()


# ============================================================
# EXAM INFORMATION EXTRACTION
# ============================================================


def extract_exam_information(
    text: str,
    feedback: str | None = None,
) -> ExamInformation:
    """
    Extract structured exam information from an official
    examination document.

    The AI provider chain is:

        Groq → OpenRouter → Local Ollama

    Provider-specific failures are handled by the provider
    manager.

    The application's Pydantic model remains the authoritative
    validation layer.
    """

    # ========================================================
    # ADMIN FEEDBACK
    # ========================================================

    feedback_instruction = ""

    if feedback:
        feedback_instruction = f"""
Administrator feedback from the previous review:

{feedback}

Use this feedback to carefully correct the extraction.
Re-examine the original document and make corrections
only when supported by the document.
"""

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
Extract exam information from the following official
exam document.

Rules:

- Extract only information explicitly present in the document.
- Do not invent or assume missing information.
- If a field is not available, return null.
- Return dates in YYYY-MM-DD format when possible.
- release_date means the date the official notification/document
  was issued or released.
- exam_dates must contain every examination date or date range
  explicitly stated in the document.
- For a single-day examination, use the same date for start_date
  and end_date.
- For an examination spanning multiple consecutive days, use one
  date range.
- If the examination occurs on separate groups of dates, return
  multiple date ranges.
- Do not combine multiple dates into a text string.

{feedback_instruction}

ORIGINAL OFFICIAL DOCUMENT:

{text}
"""

    # ========================================================
    # RESPONSE SCHEMA
    # ========================================================

    response_schema = ExamInformation.model_json_schema()

    # ========================================================
    # VALIDATOR
    # ========================================================

    def validate_response(
        content: str,
    ) -> ExamInformation:
        """
        Validate the provider response against the application's
        authoritative ExamInformation Pydantic model.
        """

        return ExamInformation.model_validate_json(
            content
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
                        "You are a strict information extraction "
                        "system. Extract only information explicitly "
                        "supported by the supplied official document."
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
            max_tokens=4096,
        )

    except AllAIProvidersFailedError as exc:
        raise RuntimeError(
            "Exam-information extraction failed because all "
            "configured AI providers failed or returned invalid "
            "structured data."
        ) from exc

    # ========================================================
    # SAFETY CHECK
    # ========================================================

    if not isinstance(result, ExamInformation):
        raise RuntimeError(
            "Exam-information extraction returned an unexpected "
            "result type."
        )

    return result