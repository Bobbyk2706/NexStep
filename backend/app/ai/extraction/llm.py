from __future__ import annotations

"""
Structured LLM calls: lenient JSON parsing, provider fallback (through
AIProviderManager, which also enforces the token budget) and one
corrective retry that shows the model what was wrong with its output.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any, TypeVar

from pydantic import BaseModel

from app.ai.extraction.facts import build_messages, inline_schema
from app.ai.provider_manager import (
    AIProviderManager,
    AllAIProvidersFailedError,
    ProviderAttempt,
)

M = TypeVar("M", bound=BaseModel)

_THINK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def parse_model_json(text: str, model_cls: type[M]) -> M:
    """
    Validate model output, tolerating the usual small-model habits:
    reasoning blocks, markdown fences and prose around the JSON.
    """

    cleaned = _FENCE.sub("", _THINK.sub("", text).strip()).strip()

    try:
        return model_cls.model_validate_json(cleaned)
    except Exception as first:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start != -1 and end > start:
            try:
                return model_cls.model_validate(json.loads(cleaned[start : end + 1]))
            except Exception:
                pass
        raise first


@dataclass
class CallRecord:
    facet: str
    provider: str | None = None
    attempts: list[dict[str, Any]] = field(default_factory=list)
    est_tokens: int = 0
    corrective_retry: bool = False


def call_structured(
    manager: AIProviderManager,
    *,
    facet: str,
    task: str,
    context: str,
    model_cls: type[M],
    feedback: str | None = None,
    max_tokens: int = 1200,
) -> tuple[M, CallRecord]:
    """Run one extraction call; raises AllAIProvidersFailedError."""

    schema = inline_schema(model_cls)
    messages = build_messages(task, context, feedback)
    record = CallRecord(facet=facet)

    def validator(text: str) -> M:
        return parse_model_json(text, model_cls)

    def remember(attempts: list[ProviderAttempt]) -> None:
        record.attempts.extend(
            {
                "provider": a.provider,
                "ok": a.success,
                "error": (a.error or "")[:300] or None,
                "waited_s": round(a.waited, 1),
            }
            for a in attempts
        )
        record.est_tokens += max((a.tokens for a in attempts), default=0)
        ok = [a for a in attempts if a.success]
        if ok:
            record.provider = ok[-1].provider

    try:
        result = manager.generate(
            messages=messages,
            response_schema=schema,
            validator=validator,
            temperature=0.0,
            max_tokens=max_tokens,
        )
        remember(manager.last_attempts)
        return result, record

    except AllAIProvidersFailedError as first_error:
        remember(first_error.attempts)

        if not first_error.validation_failed:
            raise

        # Corrective retry: show the model its own invalid answer's error.
        reason = next(
            (a.error for a in first_error.attempts if (a.error or "").startswith("Validation failed")),
            "the output did not match the schema",
        )
        retry_messages = messages + [
            {
                "role": "user",
                "content": (
                    "Your previous answer was rejected: "
                    f"{str(reason)[:400]}\nReturn ONLY corrected JSON that matches the schema."
                ),
            }
        ]

        record.corrective_retry = True

        result = manager.generate(
            messages=retry_messages,
            response_schema=schema,
            validator=validator,
            temperature=0.0,
            max_tokens=max_tokens,
        )
        remember(manager.last_attempts)
        return result, record
