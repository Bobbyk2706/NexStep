from __future__ import annotations

import copy
import os
import time
from typing import Any

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    Groq,
    RateLimitError,
)

import re

from app.ai.providers.base import (
    AIProvider,
    AIProviderConfigurationError,
    AIProviderRateLimitError,
    AIProviderResponseError,
    AIProviderUnavailableError,
)
from app.ai.token_budget import get_limiter


load_dotenv()


DEFAULT_MODEL = "openai/gpt-oss-120b"

MAX_RETRIES = 2

DEFAULT_TIMEOUT = float(
    os.getenv(
        "NEXSTEP_AI_TIMEOUT_SECONDS",
        "30",
    )
)

RETRYABLE_STATUS_CODES = {
    408,
    409,
    429,
    500,
    502,
    503,
    504,
}


def _retry_after_seconds(exc: Exception) -> float:
    """
    Seconds Groq asked us to wait: the Retry-After header, or the
    "try again in 6.5s" sentence in the error message.
    """

    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)

    if headers is not None:
        try:
            value = headers.get("retry-after")
            if value:
                return float(value)
        except (TypeError, ValueError):
            pass

    match = re.search(
        r"try again in\s+(?:(\d+)m)?\s*([\d.]+)s",
        str(exc),
        re.IGNORECASE,
    )

    if match:
        minutes = float(match.group(1) or 0)
        return minutes * 60 + float(match.group(2))

    return 0.0


def _make_groq_compatible_schema(
    schema: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert a JSON schema into the form required by Groq
    strict structured outputs.

    The caller's schema is copied before modification so the
    original schema is never mutated.
    """

    schema = copy.deepcopy(schema)

    def transform(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object":
                properties = node.get("properties", {})

                node["additionalProperties"] = False

                if properties:
                    node["required"] = list(properties.keys())

                for property_schema in properties.values():
                    transform(property_schema)

            if node.get("type") == "array":
                items = node.get("items")

                if items is not None:
                    transform(items)

            for key in ("anyOf", "oneOf", "allOf"):
                variants = node.get(key)

                if isinstance(variants, list):
                    for variant in variants:
                        transform(variant)

            defs = node.get("$defs")

            if isinstance(defs, dict):
                for definition in defs.values():
                    transform(definition)

            return

        if isinstance(node, list):
            for item in node:
                transform(item)

    transform(schema)

    return schema


class GroqProvider(AIProvider):
    """
    Groq AI provider.

    This provider is responsible only for communication with Groq.
    Provider fallback decisions are handled by AIProviderManager.
    """

    name = "groq"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        max_retries: int = MAX_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        client: Groq | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout

        if self.timeout <= 0:
            raise AIProviderConfigurationError(
                "NEXSTEP_AI_TIMEOUT_SECONDS must be greater than zero."
            )

        if client is not None:
            self.client = client
            return

        if not self.api_key:
            raise AIProviderConfigurationError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=self.api_key,
            timeout=self.timeout,
        )

    def generate(
        self,
        *,
        messages: list[dict[str, Any]],
        response_schema: dict[str, Any] | None = None,
        model: str | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> str:
        """
        Generate a response using Groq.

        If a structured response schema is supplied, the schema is
        converted into Groq-compatible strict JSON-schema format.
        """

        selected_model = model or self.model

        request_kwargs: dict[str, Any] = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens is not None:
            request_kwargs["max_tokens"] = max_tokens

        # gpt-oss models spend output tokens on hidden reasoning; low
        # effort keeps structured extraction fast and inside the budget.
        if "gpt-oss" in selected_model:
            request_kwargs["reasoning_effort"] = os.getenv(
                "NEXSTEP_GROQ_REASONING_EFFORT",
                "low",
            )

        if response_schema is not None:
            groq_schema = _make_groq_compatible_schema(
                response_schema
            )

            request_kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "nexstep_response",
                    "strict": True,
                    "schema": groq_schema,
                },
            }

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    **request_kwargs
                )

                if not response.choices:
                    raise AIProviderResponseError(
                        "Groq returned no choices."
                    )

                content = response.choices[0].message.content

                if not content or not content.strip():
                    raise AIProviderResponseError(
                        "Groq returned an empty response."
                    )

                return content

            except RateLimitError as exc:
                last_error = exc
                retry_after = _retry_after_seconds(exc) or 10.0

                # Tell the shared bucket, so every other request waits
                # instead of also being rejected.
                limiter = get_limiter(self.name)
                if limiter is not None:
                    limiter.penalize(retry_after)

                if attempt >= self.max_retries or retry_after > 45:
                    raise AIProviderRateLimitError(
                        f"Groq rate limit: retry after {retry_after:.1f}s",
                        retry_after=retry_after,
                    ) from exc

                time.sleep(retry_after + 0.5)

            except APITimeoutError as exc:
                last_error = exc

                if attempt >= self.max_retries:
                    break

                time.sleep(2**attempt)

            except APIConnectionError as exc:
                last_error = exc

                if attempt >= self.max_retries:
                    break

                time.sleep(2**attempt)

            except APIStatusError as exc:
                last_error = exc

                status_code = getattr(
                    exc,
                    "status_code",
                    None,
                )

                if (
                    status_code in RETRYABLE_STATUS_CODES
                    and attempt < self.max_retries
                ):
                    time.sleep(2 * (attempt + 1))
                    continue

                break

            except AIProviderResponseError:
                raise

            except Exception as exc:
                last_error = exc
                break

        raise AIProviderUnavailableError(
                f"Groq failed to generate a response: {last_error!r}"
            ) from last_error