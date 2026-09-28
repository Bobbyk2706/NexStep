from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from app.ai.providers.base import (
    AIProvider,
    AIProviderError,
)
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.local_provider import LocalProvider
from app.ai.providers.openrouter_provider import (
    OpenRouterProvider,
)
from click import prompt


T = TypeVar("T")


@dataclass(frozen=True)
class ProviderAttempt:
    """
    Records the outcome of one provider attempt.

    This is useful for debugging and testing without exposing
    provider internals to the rest of NexStep.
    """

    provider: str
    success: bool
    error: str | None = None


class AllAIProvidersFailedError(RuntimeError):
    """
    Raised only after every configured provider has failed.
    """

    def __init__(
        self,
        attempts: list[ProviderAttempt],
    ) -> None:
        self.attempts = attempts

        details = "; ".join(
            (
                f"{attempt.provider}: "
                f"{attempt.error or 'unknown error'}"
            )
            for attempt in attempts
        )

        super().__init__(
            "All AI providers failed. "
            f"Attempts: {details}"
        )


class AIProviderManager(Generic[T]):
    """
    Central AI fallback manager.

    Provider order is intentionally fixed:

        1. Groq
        2. OpenRouter
        3. Local

    A provider is considered successful only when:

        - it returns a non-empty response, AND
        - the optional validator accepts the response.

    If either condition fails, the next provider is attempted.
    """

    def __init__(
        self,
        *,
        providers: list[AIProvider] | None = None,
    ) -> None:
        if providers is None:
            providers = [
                self._safe_create(GroqProvider),
                self._safe_create(OpenRouterProvider),
                self._safe_create(LocalProvider),
            ]

        self.providers = [
            provider
            for provider in providers
            if provider is not None
        ]

        if not self.providers:
            raise ValueError(
                "AIProviderManager requires at least one provider."
            )

    @staticmethod
    def _safe_create(
        provider_class: type[AIProvider],
    ) -> AIProvider | None:
        """
        Create a provider without allowing missing optional
        provider configuration to crash application startup.

        A missing API key/configuration means that provider is
        unavailable and the manager continues to the next provider.
        """

        try:
            return provider_class()

        except AIProviderError:
            return None

    def generate(
        self,
        *,
        messages: list[dict[str, Any]],
        response_schema: dict[str, Any] | None = None,
        validator: Callable[[str], T] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> T | str:
        """
        Try providers in their configured order.

        Provider-specific model configuration is intentionally left
        to each provider. This prevents a Groq model name from being
        accidentally sent to OpenRouter or Ollama.
        """

        attempts: list[ProviderAttempt] = []

        for provider in self.providers:
                try:
                    print(
                        f"[AI PROVIDER] START provider={provider.name}",
                        flush=True,
                    )

                    
                    content = provider.generate(
                                                messages=messages,
                                                response_schema=response_schema,
                                                temperature=temperature,
                                                max_tokens=max_tokens,
                                            )

                    print(
                        f"[AI PROVIDER] RESPONSE provider={provider.name}",
                        flush=True,
                    )

                    if not content or not content.strip():
                        attempts.append(
                            ProviderAttempt(
                                provider=provider.name,
                                success=False,
                                error="Provider returned empty content.",
                            )
                        )
                        continue

                    if validator is None:
                        attempts.append(
                            ProviderAttempt(
                                provider=provider.name,
                                success=True,
                            )
                        )
                        return content

                    try:
                        validated = validator(content)
                    except Exception as exc:
                        attempts.append(
                            ProviderAttempt(
                                provider=provider.name,
                                success=False,
                                error=f"Validation failed: {exc}",
                            )
                        )
                        continue

                    attempts.append(
                        ProviderAttempt(
                            provider=provider.name,
                            success=True,
                        )
                    )
                    return validated

                except AIProviderError as exc:
                    print(
                        f"[AI PROVIDER] FAILED "
                        f"provider={provider.name} "
                        f"error={exc}",
                        flush=True,
                    )

                    attempts.append(
                        ProviderAttempt(
                            provider=provider.name,
                            success=False,
                            error=str(exc),
                        )
                    )
                    continue

        raise AllAIProvidersFailedError(
            attempts=attempts
        )