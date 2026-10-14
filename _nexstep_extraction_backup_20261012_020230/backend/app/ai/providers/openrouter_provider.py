from __future__ import annotations

import os
import time
from typing import Any

from dotenv import load_dotenv

from app.ai.providers.base import (
    AIProvider,
    AIProviderConfigurationError,
    AIProviderResponseError,
    AIProviderUnavailableError,
)


load_dotenv()


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_MODEL = (
    os.getenv("OPENROUTER_MODEL", "").strip()
    or "openrouter/free"
)

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


class OpenRouterProvider(AIProvider):
    """
    OpenRouter AI provider.

    OpenRouter exposes an OpenAI-compatible API, so the OpenAI
    Python client is used as the transport layer.
    """

    name = "openrouter"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        max_retries: int = MAX_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        client: Any | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv(
            "OPENROUTER_API_KEY"
        )
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
                "OPENROUTER_API_KEY is not configured."
            )

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AIProviderConfigurationError(
                "The 'openai' package is required for "
                "OpenRouterProvider."
            ) from exc

        self.client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
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

        selected_model = model or self.model

        request_kwargs: dict[str, Any] = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens is not None:
            request_kwargs["max_tokens"] = max_tokens

        if response_schema is not None:
            request_kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "nexstep_response",
                    "strict": True,
                    "schema": response_schema,
                },
            }

        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            try:
                response = (
                    self.client.chat.completions.create(
                        **request_kwargs
                    )
                )

                if not response.choices:
                    raise AIProviderResponseError(
                        "OpenRouter returned no choices."
                    )

                content = response.choices[0].message.content

                if not content or not content.strip():
                    raise AIProviderResponseError(
                        "OpenRouter returned an empty response."
                    )

                return content

            except AIProviderResponseError:
                raise

            except Exception as exc:
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

        if last_error is not None:
            raise AIProviderUnavailableError(
                f"OpenRouter failed to generate a response: {last_error!r}"
            ) from last_error
        raise AIProviderUnavailableError(
            "OpenRouter failed to generate a response."
        )