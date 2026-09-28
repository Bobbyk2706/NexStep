from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIProviderError(RuntimeError):
    """
    Base exception for all AI provider failures.

    The provider manager catches this exception and moves to
    the next provider in the fallback chain.
    """


class AIProviderConfigurationError(AIProviderError):
    """
    Raised when a provider cannot be used because its
    configuration is missing or invalid.

    Example:
        Missing GROQ_API_KEY
        Missing OPENROUTER_API_KEY
    """


class AIProviderUnavailableError(AIProviderError):
    """
    Raised when the provider cannot currently be reached.
    """


class AIProviderResponseError(AIProviderError):
    """
    Raised when the provider returns an unusable response.

    Examples:
        Empty response
        Malformed response
        Unsupported response
    """


class AIProvider(ABC):
    """
    Common interface implemented by every AI provider.

    Providers return the raw response content as a string.

    Task-specific modules remain responsible for validating
    that content against their own Pydantic schema.
    """

    name: str

    @abstractmethod
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
        Generate a response from the provider.

        Args:
            messages:
                OpenAI-compatible chat messages.

            response_schema:
                JSON schema describing the expected structured
                response. None means ordinary text generation.

            model:
                Provider-specific model identifier.

            temperature:
                Sampling temperature.

            max_tokens:
                Maximum output tokens.

        Returns:
            Raw response content.

        Raises:
            AIProviderError:
                If the provider cannot produce a usable response.
        """
        raise NotImplementedError