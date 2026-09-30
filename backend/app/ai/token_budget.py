from __future__ import annotations

import json
import math
import os
import threading
import time
from typing import Any


# ============================================================
# TOKEN BUDGETING
# ============================================================
#
# Providers such as Groq enforce a tokens-per-minute (TPM) limit
# and count the tokens you REQUEST (input + max output), not only
# the tokens you use. Sending requests blindly and letting the
# provider answer 429 wastes calls and pushes work onto weaker
# fallback models.
#
# This module lets NexStep spend a provider's budget on purpose:
#
#   estimate_tokens()  -> how big is this request?
#   TokenBucket        -> may we send it now, or must we wait?
#   get_limiter()      -> the shared bucket for a provider name
#
# It is provider-independent and has no third-party dependencies.
# ============================================================


class BudgetExceededError(RuntimeError):
    """
    Raised when a request cannot be sent within the allowed wait,
    or can never fit into the provider's bucket at all.
    """

    def __init__(
        self,
        message: str,
        *,
        wait_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        self.wait_seconds = wait_seconds


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)

    if raw is None or not raw.strip():
        return default

    try:
        return float(raw)
    except ValueError:
        return default


# ------------------------------------------------------------
# Token estimation
# ------------------------------------------------------------

_encoder: Any = None
_encoder_checked = False
_encoder_lock = threading.Lock()


def _get_encoder() -> Any:
    """
    Load a tiktoken encoder if it is installed AND usable.

    tiktoken downloads its vocabulary on first use, which fails
    offline. Any failure falls back to a character-based estimate.
    """

    global _encoder, _encoder_checked

    if _encoder_checked:
        return _encoder

    # NEXSTEP_TOKENIZER=chars forces the dependency-free estimate.
    if os.getenv("NEXSTEP_TOKENIZER", "").strip().lower() == "chars":
        _encoder_checked = True
        return None

    with _encoder_lock:
        if _encoder_checked:
            return _encoder

        try:
            import tiktoken

            _encoder = tiktoken.get_encoding("o200k_base")
        except Exception:
            _encoder = None

        _encoder_checked = True

    return _encoder


def estimate_text_tokens(text: str) -> int:
    """
    Conservative token estimate for one string.

    Deliberately errs on the high side: over-estimating only makes
    us slightly slower, under-estimating gets us rate limited.
    """

    if not text:
        return 0

    encoder = _get_encoder()

    if encoder is not None:
        try:
            count = len(
                encoder.encode(
                    text,
                    disallowed_special=(),
                )
            )
            return math.ceil(count * 1.10)
        except Exception:
            pass

    # PDF text (numbers, tables, abbreviations) tokenizes worse
    # than prose, so assume roughly 3 characters per token.
    return math.ceil(len(text) / 3.0)


def estimate_tokens(
    messages: list[dict[str, Any]],
    response_schema: dict[str, Any] | None = None,
) -> int:
    """
    Estimate the INPUT tokens of a chat request.

    A strict JSON schema is sent to the provider and counts as
    input, so it is included.
    """

    total = 0

    for message in messages:
        content = message.get("content")

        if isinstance(content, str):
            total += estimate_text_tokens(content)

        elif isinstance(content, list):
            # Multi-part content: [{"type": "text", "text": "..."}, ...]
            for part in content:
                if isinstance(part, str):
                    total += estimate_text_tokens(part)
                elif isinstance(part, dict):
                    text = part.get("text")
                    if isinstance(text, str):
                        total += estimate_text_tokens(text)

        # Tool calls, if any, are sent to the provider as JSON.
        tool_calls = message.get("tool_calls")

        if tool_calls:
            total += estimate_text_tokens(json.dumps(tool_calls))

        # Per-message framing overhead.
        total += 8

    if response_schema is not None:
        total += estimate_text_tokens(
            json.dumps(response_schema)
        )

    return total


# Used when the caller did not set max_tokens: providers then reserve
# their own default output allowance, so assume a modest one.
DEFAULT_MAX_OUTPUT_TOKENS = 1024


def estimate_request_cost(
    messages: list[dict[str, Any]],
    response_schema: dict[str, Any] | None = None,
    max_output_tokens: int | None = None,
) -> int:
    """
    Tokens a provider such as Groq will count against the
    per-minute budget for this request:

        input tokens + the max output tokens that were REQUESTED.
    """

    output = (
        max_output_tokens
        if max_output_tokens is not None and max_output_tokens > 0
        else DEFAULT_MAX_OUTPUT_TOKENS
    )

    return estimate_tokens(messages, response_schema) + output


# ------------------------------------------------------------
# Token bucket
# ------------------------------------------------------------


class TokenBucket:
    """
    Thread-safe token bucket for a tokens-per-minute budget.

    Callers reserve tokens BEFORE sending a request. If the bucket
    is short, acquire() blocks for the exact time needed, but never
    longer than `max_wait`; beyond that it raises so the caller can
    route the request to another provider instead.

    Waiting callers are served in the order they arrive: a reservation
    is taken immediately (the balance may go negative) and the caller
    sleeps until its share has been refilled.
    """

    def __init__(
        self,
        tokens_per_minute: int,
        *,
        safety: float = 0.9,
        name: str = "bucket",
    ) -> None:
        if tokens_per_minute <= 0:
            raise ValueError(
                "tokens_per_minute must be greater than zero."
            )

        if not 0 < safety <= 1:
            raise ValueError(
                "safety must be in the range (0, 1]."
            )

        self.name = name
        self.capacity = tokens_per_minute * safety
        self.rate = self.capacity / 60.0

        self._tokens = self.capacity
        self._updated = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self, now: float) -> None:
        elapsed = now - self._updated

        if elapsed > 0:
            self._tokens = min(
                self.capacity,
                self._tokens + elapsed * self.rate,
            )
            self._updated = now

    def acquire(
        self,
        cost: int,
        *,
        max_wait: float,
    ) -> float:
        """
        Reserve `cost` tokens. Returns the seconds slept.

        Raises BudgetExceededError if the request can never fit,
        or would have to wait longer than `max_wait`.
        """

        if cost > self.capacity:
            raise BudgetExceededError(
                f"{self.name}: request needs about {cost} tokens "
                f"but the per-minute budget is only "
                f"{int(self.capacity)}. Use a smaller chunk or a "
                "lower max output token setting.",
            )

        with self._lock:
            self._refill(time.monotonic())

            deficit = cost - self._tokens

            wait = (
                deficit / self.rate
                if deficit > 0
                else 0.0
            )

            if wait > max_wait:
                raise BudgetExceededError(
                    f"{self.name}: would need to wait "
                    f"{wait:.1f}s for {cost} tokens "
                    f"(limit {max_wait:.1f}s).",
                    wait_seconds=wait,
                )

            # Reserve now so concurrent callers queue behind us.
            self._tokens -= cost

        if wait > 0:
            time.sleep(wait)

        return wait

    def penalize(self, seconds: float) -> None:
        """
        Called after the provider itself answered 429.

        Our estimate was too optimistic (or another process shares
        the same organization limit), so drain the bucket by the
        amount of time the provider asked us to back off.
        """

        if seconds <= 0:
            return

        with self._lock:
            self._refill(time.monotonic())

            self._tokens = min(
                self._tokens,
                -self.rate * seconds,
            )


# ------------------------------------------------------------
# Shared limiters
# ------------------------------------------------------------

# Provider name -> (env variable, default tokens per minute).
# 0 means "no limit enforced by NexStep".
_PROVIDER_TPM: dict[str, tuple[str, int]] = {
    "groq": ("NEXSTEP_GROQ_TPM", 8000),
    "openrouter": ("NEXSTEP_OPENROUTER_TPM", 0),
    "local": ("NEXSTEP_LOCAL_TPM", 0),
}

_limiters: dict[str, TokenBucket | None] = {}
_limiters_lock = threading.Lock()


def get_limiter(provider_name: str) -> TokenBucket | None:
    """
    Return the shared bucket for a provider, or None if that
    provider has no NexStep-side limit.
    """

    with _limiters_lock:
        if provider_name in _limiters:
            return _limiters[provider_name]

        env_name, default = _PROVIDER_TPM.get(
            provider_name,
            ("", 0),
        )

        tpm = int(
            _env_float(env_name, default)
            if env_name
            else default
        )

        limiter = (
            TokenBucket(
                tpm,
                safety=_env_float(
                    "NEXSTEP_TPM_SAFETY",
                    0.9,
                ),
                name=provider_name,
            )
            if tpm > 0
            else None
        )

        _limiters[provider_name] = limiter

        return limiter


def request_capacity(provider_name: str) -> int | None:
    """
    Largest single request (input + max output) the shared bucket of a
    provider can ever accept, or None when the provider is not limited.

    Callers use this to size their context so that a request can never
    be rejected as "too large for the budget".
    """

    limiter = get_limiter(provider_name)

    if limiter is None:
        return None

    return int(limiter.capacity)


def max_wait_seconds() -> float:
    """
    Longest a request may wait for budget on one provider before
    it is routed to the next provider instead.
    """

    return _env_float(
        "NEXSTEP_AI_MAX_WAIT_SECONDS",
        25.0,
    )


def last_resort_wait_seconds() -> float:
    """
    Longest a request may wait when there is NO other provider left
    to route it to. Waiting is then better than failing.
    """

    return _env_float(
        "NEXSTEP_AI_LAST_RESORT_WAIT_SECONDS",
        120.0,
    )


def reset_limiters_for_tests() -> None:
    with _limiters_lock:
        _limiters.clear()
