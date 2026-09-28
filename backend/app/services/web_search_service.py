from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import requests
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


DEFAULT_MAX_RESULTS = 10
MAX_ALLOWED_RESULTS = 20
SEARCH_TIMEOUT_SECONDS = 20


class WebSearchError(RuntimeError):
    """Base error for web-search failures."""


class WebSearchConfigurationError(WebSearchError):
    """Raised when a search provider is not configured."""


class WebSearchUnavailableError(WebSearchError):
    """Raised when a search provider cannot perform a search."""


class WebSearchResponseError(WebSearchError):
    """Raised when a provider returns unusable data."""


@dataclass(frozen=True)
class SearchResult:
    """
    Provider-independent search result.

    The rest of NexStep should use this model instead of depending
    directly on Tavily or Serper response formats.
    """

    url: str
    title: str
    content: str
    score: float | None
    provider: str
    result_id: str | None = None


class WebSearchProvider(ABC):
    """Interface implemented by every web-search provider."""

    name: str

    @abstractmethod
    def search(
        self,
        query: str,
        *,
        max_results: int,
    ) -> list[SearchResult]:
        """Search the web and return normalized results."""


class TavilySearchProvider(WebSearchProvider):
    """
    Tavily implementation.

    Tavily is the primary provider when TAVILY_API_KEY is configured.
    """

    name = "tavily"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        client: TavilyClient | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

        if client is not None:
            self.client = client
            return

        if not self.api_key:
            raise WebSearchConfigurationError(
                "TAVILY_API_KEY is not configured."
            )

        self.client = TavilyClient(api_key=self.api_key)

    def search(
        self,
        query: str,
        *,
        max_results: int,
    ) -> list[SearchResult]:
        try:
            response = self.client.search(
                query,
                search_depth="basic",
                max_results=max_results,
                include_raw_content=False,
            )
        except Exception as exc:
            raise WebSearchUnavailableError(
                "Tavily search failed."
            ) from exc

        if not isinstance(response, dict):
            raise WebSearchResponseError(
                "Tavily returned an invalid response."
            )

        raw_results = response.get("results")

        if raw_results is None:
            raise WebSearchResponseError(
                "Tavily response did not contain search results."
            )

        if not isinstance(raw_results, list):
            raise WebSearchResponseError(
                "Tavily returned an invalid results collection."
            )

        return self._normalize_results(raw_results)

    @classmethod
    def _normalize_results(
        cls,
        raw_results: list[Any],
    ) -> list[SearchResult]:
        results: list[SearchResult] = []

        for raw_result in raw_results:
            if not isinstance(raw_result, dict):
                continue

            url = raw_result.get("url")

            if not isinstance(url, str) or not url.strip():
                continue

            title = raw_result.get("title")
            content = raw_result.get("content")
            score = raw_result.get("score")
            result_id = raw_result.get("id")

            if not isinstance(title, str):
                title = ""

            if not isinstance(content, str):
                content = ""

            if score is not None:
                try:
                    score = float(score)
                except (TypeError, ValueError):
                    score = None

            if result_id is not None and not isinstance(
                result_id,
                str,
            ):
                result_id = str(result_id)

            results.append(
                SearchResult(
                    url=url.strip(),
                    title=title.strip(),
                    content=content.strip(),
                    score=score,
                    provider=cls.name,
                    result_id=result_id,
                )
            )

        return results


class SerperSearchProvider(WebSearchProvider):
    """
    Serper implementation.

    Serper is an optional fallback provider.

    It is activated only when SERPER_API_KEY exists.
    """

    name = "serper"

    SEARCH_URL = "https://google.serper.dev/search"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("SERPER_API_KEY")

        if not self.api_key:
            raise WebSearchConfigurationError(
                "SERPER_API_KEY is not configured."
            )

        self.session = session or requests.Session()

    def search(
        self,
        query: str,
        *,
        max_results: int,
    ) -> list[SearchResult]:
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "q": query,
            "num": max_results,
        }

        try:
            response = self.session.post(
                self.SEARCH_URL,
                headers=headers,
                json=payload,
                timeout=SEARCH_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise WebSearchUnavailableError(
                "Serper search failed."
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise WebSearchResponseError(
                "Serper returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise WebSearchResponseError(
                "Serper returned an invalid response."
            )

        organic_results = data.get("organic", [])

        if not isinstance(organic_results, list):
            raise WebSearchResponseError(
                "Serper returned an invalid organic results collection."
            )

        results: list[SearchResult] = []

        for raw_result in organic_results:
            if not isinstance(raw_result, dict):
                continue

            url = raw_result.get("link")

            if not isinstance(url, str) or not url.strip():
                continue

            title = raw_result.get("title")
            snippet = raw_result.get("snippet")
            position = raw_result.get("position")
            result_id = raw_result.get("link")

            if not isinstance(title, str):
                title = ""

            if not isinstance(snippet, str):
                snippet = ""

            score: float | None = None

            if position is not None:
                try:
                    position_value = float(position)

                    # Convert ranking position into a simple
                    # descending relevance score.
                    score = 1.0 / position_value
                except (TypeError, ValueError, ZeroDivisionError):
                    score = None

            results.append(
                SearchResult(
                    url=url.strip(),
                    title=title.strip(),
                    content=snippet.strip(),
                    score=score,
                    provider=self.name,
                    result_id=result_id,
                )
            )

        return results


class WebSearchService:
    """
    Provider-fallback manager.

    Default order:

        1. Tavily
        2. Serper

    Providers without credentials are skipped.

    A successful provider stops the fallback chain.

    A provider failure causes the next configured provider to be
    attempted.

    If every configured provider fails, WebSearchUnavailableError
    is raised with the complete provider failure information.
    """

    DEFAULT_PROVIDER_ORDER = (
        "tavily",
        "serper",
    )

    def __init__(
        self,
        *,
        providers: list[WebSearchProvider] | None = None,
    ) -> None:
        if providers is None:
            providers = self._create_configured_providers()

        self.providers = providers

        if not self.providers:
            raise WebSearchConfigurationError(
                "No web-search providers are configured. "
                "Configure TAVILY_API_KEY or SERPER_API_KEY."
            )

    @classmethod
    def _create_configured_providers(
        cls,
    ) -> list[WebSearchProvider]:
        configured: list[WebSearchProvider] = []

        provider_classes: dict[
            str,
            type[WebSearchProvider],
        ] = {
            "tavily": TavilySearchProvider,
            "serper": SerperSearchProvider,
        }

        configured_order = os.getenv(
            "SEARCH_PROVIDER_ORDER",
            "tavily,serper",
        )

        provider_names = [
            name.strip().lower()
            for name in configured_order.split(",")
            if name.strip()
        ]

        for provider_name in provider_names:
            provider_class = provider_classes.get(provider_name)

            if provider_class is None:
                continue

            try:
                configured.append(provider_class())
            except WebSearchConfigurationError:
                # An optional provider with no credentials is simply
                # unavailable and should not prevent another provider
                # from being used.
                continue

        return configured

    def search(
        self,
        query: str,
        *,
        max_results: int = DEFAULT_MAX_RESULTS,
    ) -> list[SearchResult]:
        normalized_query = query.strip()

        if not normalized_query:
            raise ValueError(
                "Search query cannot be empty."
            )

        if not 1 <= max_results <= MAX_ALLOWED_RESULTS:
            raise ValueError(
                f"max_results must be between "
                f"1 and {MAX_ALLOWED_RESULTS}."
            )

        failures: list[str] = []

        for provider in self.providers:
            try:
                results = provider.search(
                    normalized_query,
                    max_results=max_results,
                )

                # A successful API call that returned zero results
                # is still a successful search. There is no reason
                # to interpret "no results" as a provider failure.
                return results

            except WebSearchError as exc:
                failures.append(
                    f"{provider.name}: {exc}"
                )

        details = "; ".join(failures)

        raise WebSearchUnavailableError(
            "All configured web-search providers failed. "
            f"Attempts: {details}"
        )


_default_search_service: WebSearchService | None = None


def get_web_search_service() -> WebSearchService:
    """
    Lazily create the application-level search service.
    """

    global _default_search_service

    if _default_search_service is None:
        _default_search_service = WebSearchService()

    return _default_search_service


def search_web(
    query: str,
    *,
    max_results: int = DEFAULT_MAX_RESULTS,
) -> list[SearchResult]:
    """
    Public search tool used by the future discovery agent.
    """

    return get_web_search_service().search(
        query,
        max_results=max_results,
    )