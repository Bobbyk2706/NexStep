from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from app.ai.providers.base import (
    AIProvider,
    AIProviderConfigurationError,
    AIProviderResponseError,
    AIProviderUnavailableError,
)


load_dotenv()


DEFAULT_MODEL = os.getenv(
    "LOCAL_AI_MODEL",
    "qwen3:1.7b",
)

DEFAULT_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434",
)

DEFAULT_TIMEOUT = float(
    os.getenv(
        "NEXSTEP_LOCAL_AI_TIMEOUT_SECONDS",
        "90",
    )
)


class LocalProvider(AIProvider):
    """
    Local Ollama provider.

    Ollama is imported lazily so NexStep can still run when
    Ollama is not installed or not running.
    """

    name = "local"

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        host: str = DEFAULT_HOST,
        timeout: float = DEFAULT_TIMEOUT,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self.host = host
        self.timeout = timeout
        self.client = client

        if self.timeout <= 0:
            raise AIProviderConfigurationError(
                "NEXSTEP_AI_TIMEOUT_SECONDS must be greater than zero."
            )

    def _get_client(self) -> Any:
        if self.client is not None:
            return self.client

        try:
            from ollama import Client
        except ImportError as exc:
            raise AIProviderConfigurationError(
                "The 'ollama' package is not installed."
            ) from exc

        try:
            self.client = Client(
                host=self.host,
                timeout=self.timeout,
            )
        except Exception as exc:
            raise AIProviderUnavailableError(
                "Could not initialize the local Ollama client."
            ) from exc

        return self.client

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

        client = self._get_client()

        request_kwargs: dict[str, Any] = {
            "model": selected_model,
            "messages": messages,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens is not None:
            request_kwargs["options"]["num_predict"] = max_tokens

        if response_schema is not None:
            request_kwargs["format"] = response_schema

        try:
            response = client.chat(
                **request_kwargs
            )
        except Exception as exc:
            raise AIProviderUnavailableError(
                f"Local Ollama provider failed to generate a response: {exc!r}"
            ) from exc

        message = getattr(
            response,
            "message",
            None,
        )

        content = getattr(
            message,
            "content",
            None,
        )

        if not content or not content.strip():
            raise AIProviderResponseError(
                "Local Ollama provider returned an empty response."
            )

        return content