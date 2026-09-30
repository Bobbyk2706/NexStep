from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from app.ai.providers.base import (
    AIProvider,
    AIProviderError,
    AIProviderRateLimitError,
)
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.local_provider import LocalProvider
from app.ai.providers.openrouter_provider import (
    OpenRouterProvider,
)
from app.ai.token_budget import (
    BudgetExceededError,
    estimate_request_cost,
    get_limiter,
    last_resort_wait_seconds,
    max_wait_seconds,
)


T = TypeVar("T")

logger = logging.getLogger("ai_provider")


@dataclass
class ProviderAttempt:
    """Outcome of one provider attempt (useful for debugging/tests)."""

    provider: str
    success: bool
    error: str | None = None
    tokens: int = 0          # estimated request cost reserved
    waited: float = 0.0      # seconds spent waiting for token budget


class AllAIProvidersFailedError(RuntimeError):
    """Raised only after every configured provider has failed."""

    def __init__(self, attempts: list[ProviderAttempt]) -> None:
        self.attempts = attempts

        details = "; ".join(
            f"{attempt.provider}: {attempt.error or 'unknown error'}"
            for attempt in attempts
        )

        super().__init__(f"All AI providers failed. Attempts: {details}")

    @property
    def validation_failed(self) -> bool:
        """True when at least one provider answered but its output was
        rejected by the caller's validator (worth retrying with feedback)."""
        return any(
            (attempt.error or "").startswith("Validation failed")
            for attempt in self.attempts
        )

    @property
    def validation_errors(self) -> list[str]:
        return [
            attempt.error or ""
            for attempt in self.attempts
            if (attempt.error or "").startswith("Validation failed")
        ]


class AIProviderManager(Generic[T]):
    """
    Central AI fallback manager: Groq -> OpenRouter -> Local.

    A provider counts as successful only when it returns non-empty
    content AND the optional validator accepts it.

    Token budgeting: before a provider is called, the request's cost
    (input + requested output tokens) is reserved in that provider's
    token bucket. If the bucket would make the request wait too long,
    the request is routed to the next provider instead of provoking a
    429. If nothing else worked, providers that were skipped only
    because of a wait are tried again, this time willing to wait.
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

        self.providers = [p for p in providers if p is not None]

        if not self.providers:
            raise ValueError(
                "AIProviderManager requires at least one provider."
            )

        self.last_provider: str | None = None
        self.last_attempts: list[ProviderAttempt] = []

    def request_capacity(self) -> int | None:
        """
        Largest single request (input + output tokens) the first
        rate-limited provider in the chain accepts, or None if no
        provider is limited. Used to size context packs.
        """
        from app.ai.token_budget import request_capacity

        for provider in self.providers:
            capacity = request_capacity(provider.name)
            if capacity:
                return capacity
        return None

    @staticmethod
    def _safe_create(provider_class: type[AIProvider]) -> AIProvider | None:
        try:
            return provider_class()
        except AIProviderError:
            return None

    # ------------------------------------------------------------------

    def _try(
        self,
        provider: AIProvider,
        *,
        messages: list[dict[str, Any]],
        response_schema: dict[str, Any] | None,
        validator: Callable[[str], T] | None,
        temperature: float,
        max_tokens: int | None,
        attempts: list[ProviderAttempt],
    ) -> tuple[bool, Any]:
        try:
            content = provider.generate(
                messages=messages,
                response_schema=response_schema,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except AIProviderError as exc:
            if isinstance(exc, AIProviderRateLimitError) and exc.retry_after > 0:
                # Our estimate was too optimistic (or another process
                # shares the limit): make following requests wait.
                limiter = get_limiter(provider.name)
                if limiter is not None:
                    limiter.penalize(exc.retry_after)

            # Provider errors can contain very long failed generations;
            # keep the log line readable.
            message = str(exc)
            if len(message) > 600:
                message = message[:600] + "... [truncated]"

            logger.warning(
                "FAILED provider=%s error=%s", provider.name, message
            )
            attempts.append(ProviderAttempt(provider.name, False, str(exc)))
            return False, None

        if not content or not content.strip():
            logger.warning(
                "FAILED provider=%s error=empty content", provider.name
            )
            attempts.append(
                ProviderAttempt(provider.name, False, "Provider returned empty content.")
            )
            return False, None

        if validator is None:
            attempts.append(ProviderAttempt(provider.name, True))
            return True, content

        try:
            validated = validator(content)
        except Exception as exc:
            logger.warning(
                "VALIDATION FAILED provider=%s error=%s", provider.name, exc
            )
            attempts.append(
                ProviderAttempt(provider.name, False, f"Validation failed: {exc}")
            )
            return False, None

        attempts.append(ProviderAttempt(provider.name, True))
        return True, validated

    def generate(
        self,
        *,
        messages: list[dict[str, Any]],
        response_schema: dict[str, Any] | None = None,
        validator: Callable[[str], T] | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> T | str:
        attempts: list[ProviderAttempt] = []
        deferred: list[tuple[AIProvider, float]] = []
        waited: dict[str, float] = {}

        cost = estimate_request_cost(messages, response_schema, max_tokens)

        def finish() -> None:
            for attempt in attempts:
                attempt.tokens = cost
                attempt.waited = waited.get(attempt.provider, 0.0)
            self.last_attempts = attempts

        common = dict(
            messages=messages,
            response_schema=response_schema,
            validator=validator,
            temperature=temperature,
            max_tokens=max_tokens,
            attempts=attempts,
        )

        for provider in self.providers:
            limiter = get_limiter(provider.name)

            if limiter is not None:
                try:
                    waited[provider.name] = limiter.acquire(
                        cost, max_wait=max_wait_seconds()
                    )
                except BudgetExceededError as exc:
                    logger.info(
                        "SKIPPED provider=%s reason=token budget (%s)",
                        provider.name,
                        exc,
                    )
                    attempts.append(
                        ProviderAttempt(provider.name, False, f"Token budget: {exc}")
                    )
                    if exc.wait_seconds is not None:
                        deferred.append((provider, exc.wait_seconds))
                    continue

            logger.info(
                "START provider=%s est_tokens=%s", provider.name, cost
            )
            ok, result = self._try(provider, **common)
            if ok:
                self.last_provider = provider.name
                finish()
                return result

        # Nothing worked. Providers skipped only because of a wait are
        # now worth waiting for, shortest wait first.
        for provider, wait in sorted(deferred, key=lambda item: item[1]):
            limiter = get_limiter(provider.name)
            try:
                if limiter is not None:
                    waited[provider.name] = limiter.acquire(
                        cost, max_wait=last_resort_wait_seconds()
                    )
            except BudgetExceededError as exc:
                attempts.append(
                    ProviderAttempt(provider.name, False, f"Token budget (last resort): {exc}")
                )
                continue

            logger.info("LAST-RESORT provider=%s", provider.name)
            ok, result = self._try(provider, **common)
            if ok:
                self.last_provider = provider.name
                finish()
                return result

        finish()
        logger.error("ALL PROVIDERS FAILED est_tokens=%s", cost)
        raise AllAIProvidersFailedError(attempts=attempts)