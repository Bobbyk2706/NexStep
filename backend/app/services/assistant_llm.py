"""
Dedicated LLM client for the student assistant ("Ask NexStep").

It talks to any OpenAI-compatible chat API, and is deliberately separate
from the extraction pipeline's provider chain (Groq -> OpenRouter ->
Ollama), so student chat never uses up the token budget that exam
extraction needs.

Configure it in backend/.env (and in Render's Environment page):

    ASSISTANT_API_KEY=your_openrouter_key
    ASSISTANT_BASE_URL=https://openrouter.ai/api/v1
    ASSISTANT_MODEL=openrouter/free
    ASSISTANT_REASONING_EFFORT=        # optional: low | medium | high | none

Examples of other OpenAI-compatible endpoints:
    https://api.groq.com/openai/v1          (use a model Groq lists)
    https://openrouter.ai/api/v1            (use a model OpenRouter lists)

The key is never logged.
"""

from __future__ import annotations

import logging
import os

from openai import OpenAI

logger = logging.getLogger("app.assistant")


class AssistantLLMError(RuntimeError):
    """The dedicated assistant model could not produce an answer."""


def is_configured() -> bool:
    return bool(
        (os.getenv("ASSISTANT_API_KEY") or "").strip()
        and (os.getenv("ASSISTANT_MODEL") or "").strip()
    )


def generate(
    messages: list[dict],
    *,
    temperature: float = 0.2,
    max_tokens: int = 700,
) -> str:
    """Return the model's answer text, or raise AssistantLLMError."""

    if not is_configured():
        raise AssistantLLMError("The assistant model is not configured.")

    api_key = os.getenv("ASSISTANT_API_KEY", "").strip()
    base_url = (os.getenv("ASSISTANT_BASE_URL") or "").strip() or None
    model = os.getenv("ASSISTANT_MODEL", "").strip()
    reasoning = (os.getenv("ASSISTANT_REASONING_EFFORT") or "").strip()

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if reasoning:
        kwargs["reasoning_effort"] = reasoning

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=25.0,
            max_retries=1,
        )
        # Some free-model routes can return an empty content field even when
        # the request succeeds. Retry once before allowing the configured
        # shared-provider fallback to run.
        for attempt in range(2):
            response = client.chat.completions.create(**kwargs)
            answer = ""

            if response.choices:
                message = response.choices[0].message
                content = message.content
                if isinstance(content, str):
                    answer = content.strip()
                elif isinstance(content, list):
                    # Accommodate providers that return text content blocks.
                    answer = "\n".join(
                        str(part.get("text", ""))
                        for part in content
                        if isinstance(part, dict) and part.get("text")
                    ).strip()

            if answer:
                return answer
            if attempt == 0:
                logger.warning(
                    "Assistant provider returned empty content; retrying once."
                )

    except Exception as exc:
        raise AssistantLLMError(
            f"{type(exc).__name__}: {str(exc)[:200]}"
        ) from exc

    raise AssistantLLMError(
        "The assistant model returned an empty answer after one retry."
    )
