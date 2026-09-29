from __future__ import annotations

from collections import deque
from datetime import datetime,date
import hashlib
import os
import re
from pathlib import Path
import threading
from urllib.parse import unquote, urljoin, urlparse

import requests

import pymupdf
from bs4 import BeautifulSoup
from sqlalchemy import select

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.document_models import (
    DocumentPage,
    ParsedDocument,
)
from app.ai.chunk_aggregator import (
    aggregate_chunk_extractions,
)
from app.ai.chunk_extractor import (
    extract_chunk_information,
)
from app.ai.parallel_chunk_extraction import (
    extract_chunks_in_parallel,
)
from app.ai.complete_extraction_normalizer import (
    normalize_complete_extraction,
)
from app.ai.complete_extraction_validation import (
    validate_complete_extraction,
)
from app.ai.extraction_serialization import (
    serialize_aggregated_extraction,
)
from app.ai.source_verification import (
    SourceVerificationResult,
    verify_exam_source,
)
from app.database.session import SessionLocal
from app.models.conducting_body import ConductingBody
from app.models.exam import Exam
from app.models.exam_date import ExamDate
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification
from app.services.document_chunker import (
    chunk_document_pages,
)
from app.services.exam_discovery_service import (
    download_pdf,
    fetch_website,
    is_pdf,
)
from app.services.web_search_service import (
    SearchResult,
    search_web,
)


class ExamDiscoveryError(RuntimeError):
    """Raised when the AI exam-discovery pipeline cannot complete safely."""


# ============================================================
# DEBUG LOGGING
# ============================================================


def _log(message: str) -> None:
    """
    Flush discovery-stage logs immediately so long-running
    frontend requests can be diagnosed from the backend terminal.
    """

    print(
        f"[AI DISCOVERY] {message}",
        flush=True,
    )


# ============================================================
# SEARCH QUERY GENERATION
# ============================================================


def _build_search_queries(
    exam_name: str,
) -> list[str]:
    """
    Build deterministic search queries from the administrator's
    exam name.

    Search is used only for discovery. It does not establish
    that a source is official.
    """

    exam_name = exam_name.strip()

    return [
        f"{exam_name} official notification",
        f"{exam_name} official website",
        f"{exam_name} notification PDF",
        f"{exam_name} recruitment notification",
    ]


# ============================================================
# WEB SOURCE DISCOVERY
# ============================================================


def _search_exam_sources(
    exam_name: str,
) -> list[dict]:
    """
    Search the web for candidate sources.

    Results are deduplicated by URL.

    Search results are candidates only. They must pass the
    separate source-verification step before being treated
    as official.
    """

    queries = _build_search_queries(
        exam_name
    )

    candidates: list[dict] = []
    seen_urls: set[str] = set()

    for query in queries:

        _log(
            f"SEARCH START: {query}"
        )

        try:
            results = search_web(
                query=query,
                max_results=10,
            )

        except Exception as error:
            _log(
                f"SEARCH FAILED: {query}"
            )

            raise ExamDiscoveryError(
                f"Web search failed for query: {query}"
            ) from error

        _log(
            f"SEARCH COMPLETE: {query} -> "
            f"{len(results)} results"
        )

        for result in results:

            if isinstance(
                result,
                SearchResult,
            ):
                url = result.url
                title = result.title
                content = result.content
                score = result.score
                provider = result.provider
                result_id = result.result_id

            elif isinstance(
                result,
                dict,
            ):
                url = result.get(
                    "url"
                )
                title = result.get(
                    "title"
                )
                content = result.get(
                    "content",
                    "",
                )
                score = result.get(
                    "score"
                )
                provider = result.get(
                    "provider"
                )
                result_id = result.get(
                    "result_id"
                )

            else:
                continue

            if not url:
                continue

            if url in seen_urls:
                continue

            seen_urls.add(
                url
            )

            candidates.append(
                {
                    "url": url,
                    "title": title or "",
                    "text": content or "",
                    "score": score,
                    "provider": provider,
                    "result_id": result_id,
                }
            )

    if not candidates:
        raise ExamDiscoveryError(
            "No candidate sources were found for the specified exam."
        )

    _log(
        f"SEARCH PIPELINE COMPLETE: "
        f"{len(candidates)} unique candidates"
    )

    return candidates


# ============================================================
# SOURCE VERIFICATION
# ============================================================


# ============================================================
# BLOCKED SOURCE HOSTS
# ============================================================
#
# Social/general-audience platforms are never a conducting
# authority's own official notification host, but they get
# indexed heavily (official accounts posting announcements,
# unofficial reposts, coaching-institute promo posts, etc.) and
# can otherwise crowd out or get mistaken for the real official
# site by the AI verifier. This is a hard, deterministic
# exclusion - it never reaches the LLM prompt or the scored
# fallback, so a misjudgment here can't happen regardless of
# what any individual provider decides.

_BLOCKED_SOURCE_HOSTS = (
    "instagram.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "youtube.com",
    "youtu.be",
    "linkedin.com",
    "reddit.com",
    "pinterest.com",
    "tiktok.com",
    "t.me",
    "telegram.org",
    "whatsapp.com",
    "quora.com",
    "medium.com",
    "threads.net",
)


def _is_blocked_source_host(hostname: str) -> bool:
    if not hostname:
        return False

    return any(
        hostname == host or hostname.endswith(f".{host}")
        for host in _BLOCKED_SOURCE_HOSTS
    )


def _verify_source(
    exam_name: str,
    candidates: list[dict],
) -> SourceVerificationResult:
    """
    Use the existing source-verification AI layer to select
    one candidate source.

    The verifier is constrained to URLs returned by search.
    """

    _log(
        "SOURCE VERIFICATION START"
    )

    candidates = [
        candidate
        for candidate in candidates
        if not _is_blocked_source_host(
            _get_hostname(candidate.get("url") or "")
        )
    ]

    if not candidates:
        _log(
            "SOURCE VERIFICATION: ALL CANDIDATES WERE ON "
            "BLOCKED (SOCIAL MEDIA / NON-INSTITUTIONAL) HOSTS"
        )
        raise ExamDiscoveryError(
            "No relevant official source was identified - every "
            "search result was on a social media or other "
            "non-institutional platform."
        )

    # Keep the verification prompt bounded to high-signal search results.
    # The complete candidate list remains available to PDF discovery.
    def candidate_score(candidate: dict) -> tuple[int, float]:
        url = (candidate.get("url") or "").lower()
        title = (candidate.get("title") or "").lower()
        text = (candidate.get("text") or "").lower()
        hostname = _get_hostname(url)
        score = 0
        if "official" in title or "official" in text:
            score += 12
        if "notification" in title or "notification" in text:
            score += 10
        if "information brochure" in title or "information brochure" in text:
            score += 9
        if "examination" in title or "examination" in text:
            score += 5
        if "application" in title or "admission" in title:
            score += 3
        if ".gov.in" in hostname or ".nic.in" in hostname:
            score += 8
        if ".gov." in hostname:
            score += 8
        if ".ac.in" in hostname or ".edu.in" in hostname:
            score += 6
        if ".ac." in hostname or ".edu." in hostname:
            score += 4
        try:
            numeric_score = float(candidate.get("score") or 0)
        except (TypeError, ValueError):
            numeric_score = 0.0
        return score, numeric_score

    verification_candidates = sorted(
        candidates,
        key=candidate_score,
        reverse=True,
    )[:12]

    _log(
        "SOURCE VERIFICATION CANDIDATES: "
        f"{len(verification_candidates)} of {len(candidates)}"
    )

    try:
        result = verify_exam_source(
            exam_name=exam_name,
            sources=verification_candidates,
        )
    except Exception as error:
        _log(
            f"SOURCE VERIFICATION FAILED: "
            f"{type(error).__name__}: {error}"
        )
        raise ExamDiscoveryError(
            "Official source verification failed."
        ) from error

    _log(
        "SOURCE VERIFICATION COMPLETE: "
        f"{result.selected_url or '<none>'}"
    )

    candidate_urls = {
        candidate["url"]
        for candidate in verification_candidates
        if candidate.get("url")
    }

    if result.relevant and result.selected_url:
        if result.selected_url not in candidate_urls:
            raise ExamDiscoveryError(
                "Source verification returned a URL that was not "
                "present in the verification candidate list."
            )
        return result

    # Safe deterministic recovery. The fallback can only select a URL
    # already returned by the search provider and requires strong
    # institutional/official evidence. It never invents a URL.
    fallback_candidates: list[tuple[int, float, dict]] = []

    for candidate in verification_candidates:
        url = candidate.get("url")
        if not url:
            continue
        parsed = urlparse(url)
        hostname = _get_hostname(url)
        title = (candidate.get("title") or "").lower()
        text = (candidate.get("text") or "").lower()
        score = 0
        if ".gov.in" in hostname or ".nic.in" in hostname:
            score += 30
        elif ".gov." in hostname:
            score += 28
        elif ".ac.in" in hostname or ".edu.in" in hostname:
            score += 24
        elif ".ac." in hostname or ".edu." in hostname:
            score += 18
        if "official" in title or "official" in text:
            score += 18
        if "notification" in title or "notification" in text:
            score += 15
        if "information brochure" in title or "information brochure" in text:
            score += 12
        if "examination" in title or "examination" in text:
            score += 6
        if parsed.scheme != "https":
            score -= 10
        try:
            search_score = float(candidate.get("score") or 0)
        except (TypeError, ValueError):
            search_score = 0.0
        fallback_candidates.append((score, search_score, candidate))

    fallback_candidates.sort(
        key=lambda item: (item[0], item[1], item[2].get("url") or ""),
        reverse=True,
    )

    if fallback_candidates:
        fallback_score, _, fallback = fallback_candidates[0]
        if fallback_score >= 24:
            fallback_url = fallback["url"]
            _log(
                "SOURCE VERIFICATION AI RETURNED NO SOURCE; "
                f"USING VERIFIED SEARCH FALLBACK: {fallback_url}"
            )
            return SourceVerificationResult(
                selected_url=fallback_url,
                source_type="OFFICIAL_SEARCH_FALLBACK",
                relevant=True,
            )

    raise ExamDiscoveryError(
        "No relevant official source was identified."
    )


# ============================================================
# PDF CANDIDATE SCORING
# ============================================================


_STOPWORDS_FOR_EXAM_TOKENS = {
    "and",
    "exam",
    "examination",
    "for",
    "in",
    "notification",
    "of",
    "official",
    "pdf",
    "test",
    "the",
}

_NEGATIVE_PDF_KEYWORDS = (
    "history",
    "about us",
    "about-us",
    "gallery",
    "photo gallery",
    "annual report",
    "rti",
    "right to information",
    "press release",
    "press-release",
    "newsletter",
    "magazine",
    "tender",
    "profile",
    "vision and mission",
    "org chart",
    "organogram",
    "citizen charter",
    "grievance",
    "faq",
    "media coverage",
    "achievements",
    "success stor",
    "alumni",
    "convocation",
    "sports",
    "cultural",
)

_STRONG_POSITIVE_PDF_KEYWORDS = (
    "information brochure",
    "info brochure",
    "notification",
    "advertisement",
    "advt",
    "brochure",
)


def _extract_exam_tokens(exam_name: str) -> list[str]:
    """
    Break the administrator-supplied exam name into meaningful
    lowercase tokens used to check relevance of a candidate link
    or document. Generic words and bare "exam"/"examination" are
    excluded so scoring focuses on what actually identifies this
    exam (e.g. "GATE", "NEET", "2027").
    """

    tokens = re.findall(r"[a-z0-9]+", exam_name.lower())
    return [
        token
        for token in tokens
        if token not in _STOPWORDS_FOR_EXAM_TOKENS and len(token) > 1
    ]


def _extract_year_tokens(text: str) -> list[str]:
    return re.findall(
        r"(?<!\d)(20\d{2})(?!\d)",
        text,
    )


def _score_pdf_link(
    url: str,
    text: str,
    exam_name: str = "",
) -> int:
    """
    Deterministically score a PDF candidate for the requested exam.

    Known non-notification documents are hard rejected.
    """

    value = f"{url} {text}".lower()

    # ------------------------------------------------------------
    # HARD NEGATIVES
    # ------------------------------------------------------------

    hard_negative_terms = (
        "history",
        "history of gate",
        "history_of_gate",
        "gallery",
        "annual report",
        "annual-report",
        "annual_report",
        "newsletter",
        "magazine",
        "tender",
        "convocation",
        "sports",
        "cultural",
        "syllabus",
        "answer key",
        "answerkey",
        "answer_key",
        "question paper",
        "questionpaper",
        "question-paper",
        "test paper",
        "testpaper",
        "test-paper",
        "sample paper",
        "samplepaper",
        "sample-paper",
        "previous year",
        "old paper",
    )

    if any(
        term in value
        for term in hard_negative_terms
    ):
        return -100

    # ------------------------------------------------------------
    # BASE SCORE
    # ------------------------------------------------------------

    score = 0

    if ".pdf" in value:
        score += 5

    keywords = (
        "notification",
        "advertisement",
        "notice",
        "examination",
        "exam",
        "recruitment",
        "application",
        "brochure",
        "information",
        "circular",
        "download",
    )

    for keyword in keywords:
        if keyword in value:
            score += 1

    for keyword in _STRONG_POSITIVE_PDF_KEYWORDS:
        if keyword in value:
            score += 6

    # ------------------------------------------------------------
    # EXAM IDENTITY
    # ------------------------------------------------------------

    exam_tokens = _extract_exam_tokens(
        exam_name
    )

    if exam_tokens:
        matched = sum(
            1
            for token in exam_tokens
            if token in value
        )

        if matched == 0:
            score -= 6
        else:
            score += matched * 4

    # ------------------------------------------------------------
    # YEAR
    # ------------------------------------------------------------

    exam_years = set(
        _extract_year_tokens(exam_name)
    )

    if exam_years:
        parsed_url = urlparse(url)

        url_years = set(
            _extract_year_tokens(parsed_url.path)
        )

        text_years = set(
            _extract_year_tokens(text)
        )

        # An explicit year in the document URL must match
        # the requested exam year.
        if url_years and not (url_years & exam_years):
            return -100

        if url_years:
            score += 5

        elif text_years:
            if text_years & exam_years:
                score += 5
            else:
                score -= 8
    # ------------------------------------------------------------
    # GENERIC NEGATIVES
    # ------------------------------------------------------------

    for keyword in _NEGATIVE_PDF_KEYWORDS:
        if keyword in value:
            score -= 15

    return score

def _get_hostname(
    url: str,
) -> str:
    """
    Return a normalized hostname.
    """

    return (
        urlparse(url)
        .netloc
        .lower()
        .split(":")[0]
    )


def _is_same_official_host(
    url: str,
    official_host: str,
) -> bool:
    """
    Accept URLs on the exact verified hostname or on a
    subdomain of the same official domain.
    """

    try:
        hostname = _get_hostname(url).lower().rstrip(".")
        official_hostname = official_host.lower().rstrip(".")

        if hostname == official_hostname:
            return True

        # The verified host itself may be a subdomain.
        official_parts = official_hostname.split(".")

        if len(official_parts) < 3:
            return False

        official_domain = ".".join(official_parts[-3:])

        return (
            hostname.endswith("." + official_domain)
            or hostname == official_domain
        )

    except Exception:
        return False

def _add_pdf_candidate(
    pdf_candidates: dict[str, tuple[int, dict]],
    url: str,
    text: str,
    exam_name: str = "",
) -> None:
    """
    Add or update a PDF candidate using deterministic scoring.

    Candidates that score at or below zero (no exam-identifying
    token present, or matching a known non-notification page type
    such as "history"/"gallery"/"annual report") are never added.
    This is what stops an unrelated official PDF from ever being
    picked as a fallback simply because it was the only one found.
    """

    if not url:
        return

    score = _score_pdf_link(
        url,
        text,
        exam_name=exam_name,
    )

    if score <= 0:
        return

    existing = pdf_candidates.get(
        url
    )

    candidate = {
        "url": url,
        "text": text,
    }

    if (
        existing is None
        or score > existing[0]
    ):
        pdf_candidates[url] = (
            score,
            candidate,
        )


def _get_result_fields(
    result,
) -> tuple[str | None, str, str]:
    """
    Normalize SearchResult/dict results.
    """

    if isinstance(
        result,
        SearchResult,
    ):
        return (
            result.url,
            result.title or "",
            result.content or "",
        )

    if isinstance(
        result,
        dict,
    ):
        return (
            result.get("url"),
            result.get("title") or "",
            result.get("content") or "",
        )

    return (
        None,
        "",
        "",
    )


# ============================================================
# PDF DOWNLOAD
# ============================================================


_PDF_STORAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "storage"
    / "notifications"
)
_PDF_STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "application/pdf,application/octet-stream;q=0.9,"
        "text/html;q=0.8,*/*;q=0.7"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


def _pdf_filename(url: str) -> str:
    """Build a safe local filename from a PDF URL."""

    filename = os.path.basename(
        unquote(urlparse(url).path)
    )

    if not filename:
        filename = "document.pdf"

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    return filename


def _download_pdf_with_session(
    url: str,
    referer: str | None = None,
) -> dict:
    """
    Download a PDF using a browser-like session.

    The existing download_pdf() helper is intentionally strict,
    but some official sites reject a bare requests client and return
    an HTML page for a perfectly valid PDF URL. This helper keeps the
    same PDF-signature safety rule while establishing a normal session
    and sending a Referer/User-Agent.
    """

    headers = dict(_BROWSER_HEADERS)

    if referer:
        headers["Referer"] = referer

    with requests.Session() as session:
        session.headers.update(headers)

        # Establish the official-site session first so any cookies
        # required by the document endpoint are available.
        if referer:
            try:
                session.get(
                    referer,
                    timeout=20,
                    allow_redirects=True,
                )
            except requests.RequestException:
                # The actual PDF request below remains authoritative.
                pass

        response = session.get(
            url,
            timeout=30,
            allow_redirects=True,
        )
        response.raise_for_status()

        content = response.content

    if not content:
        raise ValueError(
            "Downloaded document is empty."
        )

    if not content.startswith(b"%PDF-"):
        content_type = response.headers.get(
            "Content-Type",
            "",
        )
        raise ValueError(
            "Downloaded content is not a valid PDF "
            f"(content_type={content_type})."
        )

    document_hash = hashlib.sha256(
        content
    ).hexdigest()

    filename = _pdf_filename(url)
    file_path = _PDF_STORAGE_DIR / filename

    file_path.write_bytes(content)

    return {
        "content": content,
        "url": url,
        "document_hash": document_hash,
        "content_type": response.headers.get(
            "Content-Type",
            "application/pdf",
        ),
        "path": str(file_path),
    }


def _download_best_pdf_candidate(
    pdf_candidates: dict[str, tuple[int, dict]],
    exam_name: str = "",
) -> dict | None:

    ordered_candidates = sorted(
        pdf_candidates.values(),
        key=lambda item: (
            item[0],
            item[1]["url"],
        ),
        reverse=True,
    )

    for score, candidate in ordered_candidates:

        candidate_url = candidate["url"]

        # Never download obviously irrelevant candidates.
        if score < 20:
            _log(
                f"SKIPPING PDF: score={score} "
                f"url={candidate_url}"
            )
            continue

        _log(
            f"TRYING PDF: score={score} "
            f"url={candidate_url}"
        )

        try:
            pdf = download_pdf(
                candidate_url
            )

            relevant, reason = (
                _pdf_content_looks_relevant(
                    pdf["content"],
                    exam_name,
                )
            )

            if not relevant:

                _log(
                    f"PDF CONTENT REJECTED: "
                    f"{candidate_url} -> {reason}"
                )

                try:
                    Path(
                        pdf["path"]
                    ).unlink(
                        missing_ok=True
                    )
                except Exception:
                    pass

                continue

            _log(
                f"PDF ACCEPTED: {candidate_url}"
            )

            return pdf

        except Exception as error:

            _log(
                f"PDF CANDIDATE FAILED: "
                f"{candidate_url} -> {error}"
            )

    return None

def _pdf_content_looks_relevant(
    content: bytes,
    exam_name: str,
) -> tuple[bool, str]:
    """
    Sanity-check a downloaded PDF's actual *content* against the
    exam it is supposed to be the notification for.

    `_score_pdf_link()` only ever looks at the URL and the
    surrounding link text on the page it was found on - it never
    sees what the PDF itself actually says. That is enough to
    reject an obviously unrelated document, but it can still be
    fooled by a same-domain PDF with a generic/undescriptive link
    (e.g. a "History of GATE" retrospective linked with plain text
    like "About" or "Download") that happens to pick up enough
    domain-substring/keyword points to pass the URL-level score.
    This is a second, independent check against the real text of
    the document before it is accepted as the official notification.

    Deliberately conservative: this only rejects a document when it
    is fairly confident something is wrong (a known non-notification
    page type is named right at the top, or none of the exam's own
    identifying tokens appear anywhere in the document at all). If
    the PDF can't be parsed here, that is left for the main
    extraction step to report - this function just returns "looks
    fine" rather than blocking on a parsing problem.
    """

    try:
        document = pymupdf.open(
            stream=content,
            filetype="pdf",
        )

        try:
            first_pages_text = " ".join(
                page.get_text()
                for page in list(document)[:2]
            ).lower()
        finally:
            document.close()

    except Exception:
        return True, ""

    if not first_pages_text.strip():
        return True, ""

    # A known non-notification page type named right at the start
    # of the document (its title/heading) is a strong signal this
    # is the wrong document, regardless of how it was linked to.
    heading_text = first_pages_text[:300]

    for keyword in _NEGATIVE_PDF_KEYWORDS:
        if keyword in heading_text:
            return False, (
                f"document heading matches non-notification "
                f"page type ('{keyword}')"
            )

    exam_tokens = _extract_exam_tokens(exam_name)

    if exam_tokens:
        matched = any(
            token in first_pages_text
            for token in exam_tokens
        )

        if not matched:
            return False, (
                "none of the exam's identifying terms "
                f"({', '.join(exam_tokens)}) appear anywhere in "
                "the document text"
            )

    return True, ""


def _download_best_pdf_candidate(
    pdf_candidates: dict[str, tuple[int, dict]],
    exam_name: str = "",
) -> dict | None:
    """
    Try PDF candidates in deterministic relevance order.

    download_pdf() performs actual PDF signature validation.
    _pdf_content_looks_relevant() additionally checks the
    downloaded document's own text against the exam it is
    supposed to be for, since URL/link-text scoring alone can be
    fooled by a same-domain document with generic link text.
    """

    ordered_candidates = sorted(
        pdf_candidates.values(),
        key=lambda item: (
            item[0],
            item[1]["url"],
        ),
        reverse=True,
    )

    for score, candidate in ordered_candidates:

        candidate_url = candidate["url"]

        _log(
            f"TRYING PDF: score={score} "
            f"url={candidate_url}"
        )

        try:
            pdf = download_pdf(
                candidate_url
            )

        except Exception as error:
            _log(
                f"PDF DOWNLOAD FAILED: {candidate_url} "
                f"-> {error}"
            )
            continue

        relevant, reason = _pdf_content_looks_relevant(
            pdf["content"],
            exam_name,
        )

        if not relevant:
            _log(
                f"PDF CONTENT REJECTED: {candidate_url} -> {reason}"
            )
            try:
                Path(pdf["path"]).unlink(missing_ok=True)
            except Exception:
                pass
            continue

        _log(
            f"PDF DOWNLOAD SUCCESS: {candidate_url}"
        )

        return pdf

    return None


# ============================================================
# TARGETED OFFICIAL PDF SEARCH
# ============================================================


def _search_official_pdf_candidates(
    exam_name: str,
    official_host: str,
) -> dict[str, tuple[int, dict]]:
    """
    Search specifically for PDFs on the verified official
    hostname.

    This is preferred over broad website crawling.
    """

    pdf_candidates: dict[
        str,
        tuple[int, dict],
    ] = {}

    queries = [
        (
            f'site:{official_host} '
            f'"{exam_name}" filetype:pdf'
        ),
        (
            f'site:{official_host} '
            f'{exam_name} notification pdf'
        ),
        (
            f'site:{official_host} '
            f'{exam_name} information brochure'
        ),
    ]

    for query in queries:

        _log(
            f"TARGETED PDF SEARCH START: {query}"
        )

        try:
            results = search_web(
                query=query,
                max_results=10,
            )

        except Exception as error:
            _log(
                f"TARGETED PDF SEARCH FAILED: {error}"
            )

            continue

        _log(
            f"TARGETED PDF SEARCH COMPLETE: "
            f"{len(results)} results"
        )

        for result in results:

            url, title, content = (
                _get_result_fields(
                    result
                )
            )

            if not url:
                continue

            if not _is_same_official_host(
                url,
                official_host,
            ):
                continue

            text = (
                f"{title} {content}"
            ).strip()

            if ".pdf" not in url.lower():
                continue

            _add_pdf_candidate(
                pdf_candidates,
                url,
                text,
                exam_name=exam_name,
            )

    _log(
        f"TARGETED PDF SEARCH TOTAL: "
        f"{len(pdf_candidates)} PDF candidates"
    )

    return pdf_candidates


# ============================================================
# OFFICIAL PAGE / HIDDEN PDF URL DISCOVERY
# ============================================================


def _extract_document_urls_from_html(
    html: str,
    base_url: str,
    official_host: str,
) -> list[tuple[str, str]]:
    """
    Extract document-like URLs from both normal links and
    JavaScript/data attributes used by modern official sites.

    Some official sites expose download controls as buttons or
    JavaScript handlers instead of normal <a href="..."> links.
    A crawler that only inspects <a> tags can therefore miss the
    actual brochure/notification PDF.
    """

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    found: dict[str, str] = {}

    # Normal anchors, buttons, and elements carrying common URL
    # attributes are all inspected.
    for element in soup.find_all(True):
        text = element.get_text(
            " ",
            strip=True,
        )

        attribute_values: list[str] = []

        for attribute_name in (
            "href",
            "src",
            "data-href",
            "data-url",
            "data-file",
            "data-download",
            "data-document",
            "onclick",
            "value",
        ):
            value = element.get(attribute_name)
            if isinstance(value, str) and value.strip():
                attribute_values.append(value)

        for raw_value in attribute_values:
            # Only treat the raw attribute value itself as a URL/path
            # candidate when it actually looks like one. Attributes
            # such as `onclick` frequently hold arbitrary JavaScript
            # (e.g. toggleSub('exam-sub', 'mob-exam')) rather than a
            # URL - blindly urljoin()-ing that text produces a bogus
            # "URL" that only ever 404s and wastes crawl budget that
            # should go to real pages.
            stripped_value = raw_value.strip()

            candidates = (
                [stripped_value]
                if re.match(
                    r"^(https?://|/|\./|\.\./)[^\s()'\"]*$",
                    stripped_value,
                    flags=re.IGNORECASE,
                )
                else []
            )

            # Then extract URL/path-looking strings embedded in
            # JavaScript such as window.open('/static/file.pdf').
            candidates.extend(
                re.findall(
                    r"(?:https?://[^\"'\s)]+|/[^\"'\s)]+\\?\.pdf(?:\?[^\"'\s)]*)?)",
                    raw_value,
                    flags=re.IGNORECASE,
                )
            )

            for candidate in candidates:
                candidate = candidate.strip().strip("'\"")

                if not candidate:
                    continue

                if candidate.startswith((
                    "javascript:",
                    "#",
                    "mailto:",
                    "tel:",
                )):
                    continue

                absolute_url = urljoin(
                    base_url,
                    candidate,
                )

                if not absolute_url.startswith(
                    "https://"
                ):
                    continue

                if not _is_same_official_host(
                    absolute_url,
                    official_host,
                ):
                    continue

                # Keep the text around the URL because it improves
                # deterministic scoring of brochure/notification links.
                context = f"{text} {raw_value}".strip()

                if absolute_url not in found:
                    found[absolute_url] = context
                elif len(context) > len(found[absolute_url]):
                    found[absolute_url] = context

    return list(found.items())


def _official_navigation_urls(
    official_url: str,
    official_host: str,
) -> list[str]:
    """
    Return high-value official pages that commonly contain the
    current notification/brochure.

    These are discovery hints, not hardcoded exam documents.
    """

    parsed = urlparse(official_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"

    paths = (
        parsed.path,
        "/download",
        "/downloads",
        "/notification",
        "/notifications",
        "/notices",
        "/announcements",
    )

    result: list[str] = []
    seen: set[str] = set()

    for path in paths:
        if not path:
            continue

        url = urljoin(
            origin,
            path,
        )

        if not _is_same_official_host(
            url,
            official_host,
        ):
            continue

        if url in seen:
            continue

        seen.add(url)
        result.append(url)

    return result


# ============================================================
# BOUNDED OFFICIAL-SITE PDF DISCOVERY
# ============================================================


def _bounded_official_pdf_discovery(
    official_url: str,
    official_host: str,
    exam_name: str = "",
) -> dict[str, tuple[int, dict]]:
    """
    Perform a bounded crawl focused on official download and
    notification pages.

    The crawl deliberately checks common official document pages
    before following ordinary navigation links. It also inspects
    JavaScript/data attributes because modern sites frequently put
    PDF download URLs behind buttons rather than <a href> elements.
    """

    MAX_PAGES = 10
    MAX_DEPTH = 1
    MAX_FOLLOW_LINKS_PER_PAGE = 6

    queue = deque()

    for url in _official_navigation_urls(
        official_url,
        official_host,
    ):
        queue.append(
            (
                url,
                0,
            )
        )

    visited: set[str] = set()

    pdf_candidates: dict[
        str,
        tuple[int, dict],
    ] = {}

    pages_checked = 0

    while (
        queue
        and pages_checked < MAX_PAGES
    ):

        current_url, depth = queue.popleft()

        if current_url in visited:
            continue

        if depth > MAX_DEPTH:
            continue

        visited.add(current_url)
        pages_checked += 1

        _log(
            f"BOUNDED DISCOVERY PAGE "
            f"{pages_checked}/{MAX_PAGES}: "
            f"{current_url}"
        )

        try:
            response, content_type = fetch_website(
                current_url
            )

        except Exception as error:
            _log(
                f"BOUNDED PAGE FAILED: "
                f"{current_url} -> {error}"
            )
            continue

        if is_pdf(
            content_type,
            current_url,
        ):
            _add_pdf_candidate(
                pdf_candidates,
                current_url,
                current_url,
                exam_name=exam_name,
            )
            continue

        if "text/html" not in content_type.lower():
            continue

        # Inspect every relevant URL-bearing HTML attribute.
        document_urls = _extract_document_urls_from_html(
            response.text,
            current_url,
            official_host,
        )

        relevant_links: list[
            tuple[int, str, str]
        ] = []

        for absolute_url, link_text in document_urls:
            score = _score_pdf_link(
                absolute_url,
                link_text,
                exam_name=exam_name,
            )

            if ".pdf" in absolute_url.lower():
                _add_pdf_candidate(
                    pdf_candidates,
                    absolute_url,
                    link_text,
                    exam_name=exam_name,
                )
                continue

            relevance_text = (
                f"{absolute_url} "
                f"{link_text}"
            ).lower()

            relevant_keywords = (
                "notification",
                "advertisement",
                "notice",
                "examination",
                "exam",
                "recruitment",
                "application",
                "download",
                "circular",
                "brochure",
                "information",
                "admit",
                "document",
            )

            if any(
                keyword in relevance_text
                for keyword in relevant_keywords
            ):
                relevant_links.append(
                    (
                        score,
                        absolute_url,
                        link_text,
                    )
                )

        if depth < MAX_DEPTH:
            relevant_links.sort(
                key=lambda item: (
                    item[0],
                    item[1],
                ),
                reverse=True,
            )

            for (
                _,
                next_url,
                _,
            ) in relevant_links[
                :MAX_FOLLOW_LINKS_PER_PAGE
            ]:
                if next_url not in visited:
                    queue.append(
                        (
                            next_url,
                            depth + 1,
                        )
                    )

    _log(
        f"BOUNDED DISCOVERY COMPLETE: "
        f"{pages_checked} pages checked, "
        f"{len(pdf_candidates)} PDF candidates"
    )

    return pdf_candidates


# ============================================================
# OFFICIAL PDF DISCOVERY
# ============================================================


def _find_official_pdf(
    exam_name: str,
    official_url: str,
    candidates: list[dict],
) -> dict:
    """
    Locate and download the official PDF.

    Discovery order:

        1. Verified URL itself
        2. PDF URLs already returned by original search
        3. Targeted PDF search on verified hostname
        4. Bounded official-site discovery

    Every accepted PDF must:

        - belong to the verified hostname
        - successfully download
        - pass actual PDF signature validation
    """

    _log(
        f"PDF DISCOVERY START: {official_url}"
    )

    # --------------------------------------------------------
    # Fetch verified source
    # --------------------------------------------------------

    _log(
        "FETCHING VERIFIED OFFICIAL SOURCE"
    )

    try:
        response, content_type = fetch_website(
            official_url
        )

    except Exception as error:

        _log(
            f"VERIFIED SOURCE FETCH FAILED: {error}"
        )

        raise ExamDiscoveryError(
            "Unable to fetch the verified official source."
        ) from error

    _log(
        f"VERIFIED SOURCE FETCH COMPLETE: "
        f"content_type={content_type}"
    )

    # --------------------------------------------------------
    # Verified source itself is PDF
    # --------------------------------------------------------

    if is_pdf(
        content_type,
        official_url,
    ):

        _log(
            "VERIFIED SOURCE IS ITSELF A PDF"
        )

        try:
            return _download_pdf_with_session(
                official_url,
                referer=official_url,
            )

        except Exception as error:

            raise ExamDiscoveryError(
                "The verified official PDF could not be downloaded."
            ) from error

    # --------------------------------------------------------
    # Verified source must be HTML
    # --------------------------------------------------------

    if "text/html" not in content_type.lower():

        raise ExamDiscoveryError(
            "The verified official source is neither "
            "a PDF nor an HTML page."
        )

    official_host = _get_hostname(
        official_url
    )

    # ========================================================
    # STEP 1
    # Inspect PDF URLs from original search.
    # ========================================================

    _log(
        "CHECKING PDFS FROM ORIGINAL SEARCH RESULTS"
    )

    existing_search_pdfs: dict[
        str,
        tuple[int, dict],
    ] = {}

    for candidate in candidates:

        candidate_url = candidate.get(
            "url"
        )

        if not candidate_url:
            continue

        if not _is_same_official_host(
            candidate_url,
            official_host,
        ):
            continue

        if ".pdf" not in candidate_url.lower():
            continue

        title = (
            candidate.get("title")
            or ""
        )

        text = (
            candidate.get("text")
            or ""
        )

        _add_pdf_candidate(
            existing_search_pdfs,
            candidate_url,
            f"{title} {text}".strip(),
            exam_name=exam_name,
        )

    _log(
        f"ORIGINAL SEARCH PDF CANDIDATES: "
        f"{len(existing_search_pdfs)}"
    )

    pdf = _download_best_pdf_candidate(
        existing_search_pdfs,
        exam_name=exam_name,
    )

    if pdf is not None:
        return pdf

    # ========================================================
    # STEP 2
    # Targeted official-domain PDF search.
    # ========================================================

    _log(
        "STARTING TARGETED OFFICIAL PDF SEARCH"
    )

    targeted_candidates = (
        _search_official_pdf_candidates(
            exam_name=exam_name,
            official_host=official_host,
        )
    )

    pdf = _download_best_pdf_candidate(
        targeted_candidates,
        exam_name=exam_name,
    )

    if pdf is not None:
        return pdf

    # ========================================================
    # STEP 3
    # Bounded official-site discovery.
    # ========================================================

    _log(
        "STARTING BOUNDED OFFICIAL-SITE DISCOVERY"
    )

    bounded_candidates = (
        _bounded_official_pdf_discovery(
            official_url=official_url,
            official_host=official_host,
            exam_name=exam_name,
        )
    )

    pdf = _download_best_pdf_candidate(
        bounded_candidates,
        exam_name=exam_name,
    )

    if pdf is not None:
        return pdf

    raise ExamDiscoveryError(
        "No official PDF notification could be found after "
        "checking the verified source, original search results, "
        "targeted official-domain PDF search, and bounded "
        "official-source discovery."
    )


# ============================================================
# PDF PAGE EXTRACTION
# ============================================================


def _parse_pdf_document(
    pdf_content: bytes,
    *,
    source_url: str,
    document_hash: str,
    file_path: str | None = None,
) -> ParsedDocument:
    """
    Parse the official PDF while preserving physical page boundaries.

    The parser deliberately does not perform AI extraction.

    Its only responsibilities are:

        PDF
          ↓
        physical pages
          ↓
        ParsedDocument

    Keeping parsing separate from AI extraction allows later stages
    to reason about sections and evidence without losing page
    provenance.
    """

    if not pdf_content:
        raise ExamDiscoveryError(
            "The official PDF is empty."
        )

    _log(
        "OPENING PDF FOR PAGE-AWARE PARSING"
    )

    try:
        document = pymupdf.open(
            stream=pdf_content,
            filetype="pdf",
        )

    except Exception as error:
        raise ExamDiscoveryError(
            "Unable to open the official PDF."
        ) from error

    pages: list[DocumentPage] = []

    try:
        for index, page in enumerate(document):
            page_number = index + 1

            try:
                text = page.get_text(
                    "text",
                ) or ""

            except Exception as error:
                _log(
                    f"PDF PAGE TEXT EXTRACTION FAILED: "
                    f"page={page_number} "
                    f"error={type(error).__name__}: {error}"
                )

                text = ""

            pages.append(
                DocumentPage(
                    page_number=page_number,
                    text=text,
                )
            )

    finally:
        document.close()

    if not pages:
        raise ExamDiscoveryError(
            "The official PDF contains no pages."
        )

    non_empty_pages = [
        page
        for page in pages
        if page.has_text
    ]

    if not non_empty_pages:
        raise ExamDiscoveryError(
            "The official PDF contains no extractable text."
        )

    parsed_document = ParsedDocument(
        source_url=source_url,
        document_hash=document_hash,
        file_path=file_path,
        pages=pages,
        metadata={
            "parser": "PyMuPDF",
            "page_count": len(pages),
            "non_empty_page_count": len(non_empty_pages),
        },
    )

    _log(
        "PDF PAGE-AWARE PARSING COMPLETE: "
        f"{parsed_document.page_count} pages, "
        f"{len(non_empty_pages)} non-empty pages, "
        f"{parsed_document.character_count} characters"
    )

    return parsed_document


# ============================================================
# EXISTING AI EXTRACTION PIPELINE
# ============================================================


def _extract_and_validate_pdf(
    pdf_content: bytes,
    *,
    source_url: str,
    document_hash: str,
    file_path: str | None = None,
) -> AggregatedExtractionResult:
    """
    Run the existing production extraction pipeline:

        PDF
          ↓
        pages
          ↓
        lossless chunks
          ↓
        AI extraction
          ↓
        aggregation
          ↓
        normalization
          ↓
        validation
    """

    document = _parse_pdf_document(
        pdf_content,
        source_url=source_url,
        document_hash=document_hash,
        file_path=file_path,
    )

    pages = [
        page.text
        for page in document.pages
    ]

    chunks = chunk_document_pages(
        pages,
        chunk_size=16000,
    )

    if not chunks:
        raise ExamDiscoveryError(
            "The official PDF produced no extractable chunks."
        )

    _log(
        f"AI EXTRACTION: {len(chunks)} chunks (parallel)"
    )

    try:
        chunk_results = extract_chunks_in_parallel(chunks)

    except Exception as error:
        _log(
            f"AI EXTRACTION FAILED: {type(error).__name__}: {error}"
        )

        raise ExamDiscoveryError(
            "AI extraction failed while processing "
            "the official notification."
        ) from error

    if not chunk_results:
        raise ExamDiscoveryError(
            "No AI extraction results were produced."
        )

    # --------------------------------------------------------
    # Aggregate
    # --------------------------------------------------------

    _log(
        "AI EXTRACTION AGGREGATION START"
    )

    try:
        aggregated_result = (
            aggregate_chunk_extractions(
                chunk_results
            )
        )

    except Exception as error:

        _log(
            f"AI EXTRACTION AGGREGATION FAILED: "
            f"{type(error).__name__}: {error}"
        )

        raise ExamDiscoveryError(
            "AI extraction results could not be safely aggregated."
        ) from error

    _log(
        "AI EXTRACTION AGGREGATION COMPLETE"
    )

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    _log(
        "EXTRACTION NORMALIZATION START"
    )
    

    try:
        normalized_extraction = (
            normalize_complete_extraction(
                aggregated_result.extraction
            )
        )

    except Exception as error:

        raise ExamDiscoveryError(
            "The extracted examination information could not "
            "be normalized safely."
        ) from error

    _log(
        "EXTRACTION NORMALIZATION COMPLETE"
    )
    _log(
    f"NORMALIZED EXTRACTION: {normalized_extraction.model_dump()}"
    )

    normalized_result = AggregatedExtractionResult(
        extraction=normalized_extraction,
        evidence=aggregated_result.evidence,
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    _log(
        "EXTRACTION VALIDATION START"
    )

    try:
        validation_errors = (
            validate_complete_extraction(
                normalized_extraction
            )
        )

    except Exception as error:

        raise ExamDiscoveryError(
            "Complete extraction validation failed."
        ) from error

    if validation_errors:

        raise ExamDiscoveryError(
            "The extracted examination information failed "
            f"validation: {validation_errors}"
        )

    _log(
        "EXTRACTION VALIDATION COMPLETE"
    )

    return normalized_result


# ============================================================
# DATABASE HELPERS
# ============================================================


def _get_or_create_conducting_body(
    db,
    body_name: str,
    official_url: str,
) -> ConductingBody:
    """
    Reuse an existing conducting body when possible.
    """

    body_name = (
        body_name or ""
    ).strip()

    if not body_name:
        raise ExamDiscoveryError(
            "The extraction did not identify a conducting body."
        )

    parsed = urlparse(
        official_url
    )

    main_website = (
        f"{parsed.scheme}://{parsed.netloc}/"
        if parsed.scheme and parsed.netloc
        else official_url
    )

    existing = db.scalar(
        select(ConductingBody)
        .where(
            ConductingBody.name
            == body_name
        )
        .limit(1)
    )

    if existing is not None:
        return existing

    body = ConductingBody(
        name=body_name,
        main_website=main_website,
        description=None,
        logo_url=None,
    )

    db.add(
        body
    )

    db.flush()

    return body


def _get_or_create_exam(
    db,
    exam_name: str,
    conducting_body: ConductingBody,
    official_url: str,
) -> Exam:

    existing = db.scalar(
        select(Exam)
        .where(
            Exam.name
            == exam_name
        )
        .limit(1)
    )

    if existing is not None:
        return existing

    exam = Exam(
        body_id=conducting_body.body_id,
        name=exam_name,
        type="Competitive",
        description=None,
        off_exam_page=official_url,
        status="ACTIVE",
    )

    db.add(
        exam
    )

    db.flush()

    return exam


# ============================================================
# CREATE OFFICIAL NOTIFICATION
# ============================================================


def _create_official_notification(
    db,
    exam: Exam,
    official_url: str,
    pdf_path: str,
    extraction: AggregatedExtractionResult,
) -> OfficialNotification:

    information = (
        extraction.extraction.exam_information
    )

    notification = OfficialNotification(
        exam_id=exam.exam_id,
        title=(
            information.exam_name
            or exam.name
        ),
        notification_type="EXAM",
        release_date=(
            information.release_date
        ),
        application_start_date=(
            information.application_start_date
        ),
        application_end_date=(
            information.application_end_date
        ),
        official_url=official_url,
        pdf_path=pdf_path,
        ai_summary=(
            "AI-discovered official examination "
            "notification. Awaiting administrator approval."
        ),
        ai_change_summary=None,
        approval_status="PENDING",
        rejection_reason=None,
        downloaded_on=datetime.now(),
    )

    db.add(
        notification
    )

    db.flush()

    # --------------------------------------------------------
    # Persist extracted exam dates
    # --------------------------------------------------------

    for exam_date in (
        information.exam_dates
        or []
    ):

        db.add(
            ExamDate(
                notification_id=(
                    notification.notification_id
                ),
                start_date=(
                    exam_date.start_date
                ),
                end_date=(
                    exam_date.end_date
                ),
            )
        )

    return notification


# ============================================================
# CREATE PENDING EXTRACTION
# ============================================================


def _create_pending_extraction(
    db,
    notification: OfficialNotification,
    pdf_path: str,
    extraction: AggregatedExtractionResult,
) -> ExtractionHistory:

    extracted_content = (
        serialize_aggregated_extraction(
            extraction
        )
    )

    history = ExtractionHistory(
        notification_id=(
            notification.notification_id
        ),
        extraction_type="COMPLETE_EXTRACTION",
        source_pdf_path=pdf_path,
        extracted_content=extracted_content,
        ai_summary=(
            "AI discovery extraction completed "
            "successfully. Awaiting administrator approval."
        ),
        change_detected=False,
        change_details=None,
        extraction_status="PENDING",
        created_at=datetime.now(),
    )

    db.add(
        history
    )

    db.flush()

    return history


# ============================================================
# PUBLIC DISCOVERY PIPELINE
# ============================================================


def _discover_exam_once(
    exam_name: str,
) -> dict:
    """
    Complete AI exam-discovery pipeline.

    Flow:

        exam name
          ↓
        web search
          ↓
        candidate sources
          ↓
        official-source verification
          ↓
        official PDF
          ↓
        existing AI extraction pipeline
          ↓
        normalization
          ↓
        validation
          ↓
        database records
          ↓
        PENDING extraction
          ↓
        administrator review

    Nothing is automatically approved.
    """

    exam_name = exam_name.strip()

    if not exam_name:
        raise ValueError(
            "Exam name cannot be empty."
        )

    if len(exam_name) > 200:
        raise ValueError(
            "Exam name cannot exceed 200 characters."
        )

    _log(
        f"PIPELINE START: {exam_name}"
    )

    # --------------------------------------------------------
    # 1. Search
    # --------------------------------------------------------

    candidates = _search_exam_sources(
        exam_name
    )

    # --------------------------------------------------------
    # 2. Verify official source
    # --------------------------------------------------------

    verification = _verify_source(
        exam_name,
        candidates,
    )

    official_url = (
        verification.selected_url
    )

    _log(
        f"VERIFIED OFFICIAL SOURCE: {official_url}"
    )

    # --------------------------------------------------------
    # 3. Locate and download official PDF
    # --------------------------------------------------------

    pdf = _find_official_pdf(
        exam_name=exam_name,
        official_url=official_url,
        candidates=candidates,
    )

    pdf_content = pdf.get(
        "content"
    )

    pdf_path = pdf.get(
        "path"
    )

    if not pdf_content:
        raise ExamDiscoveryError(
            "Official PDF download returned no content."
        )

    if not pdf_path:
        raise ExamDiscoveryError(
            "Official PDF was not persisted to storage."
        )

    _log(
        f"PDF DISCOVERY COMPLETE: {pdf_path}"
    )

    # --------------------------------------------------------
    # 4. Existing AI extraction
    # --------------------------------------------------------

    _log(
        "STARTING AI EXTRACTION"
    )

    extraction = _extract_and_validate_pdf(
        pdf_content,
        source_url=official_url,
        document_hash=pdf.get("document_hash") or "",
        file_path=str(pdf_path),
    )

    _log(
        "AI EXTRACTION COMPLETE"
    )

    information = (
        extraction.extraction.exam_information
    )

    extracted_exam_name = (
        information.exam_name
        or exam_name
    ).strip()

    conducting_body_name = (
        information.conducting_body
        or ""
    ).strip()

    if not conducting_body_name:
        raise ExamDiscoveryError(
            "AI extraction did not identify a conducting body."
        )

    # --------------------------------------------------------
    # 5. Database transaction
    # --------------------------------------------------------

    _log(
        "DATABASE PERSISTENCE START"
    )

    with SessionLocal() as db:

        try:

            conducting_body = (
                _get_or_create_conducting_body(
                    db=db,
                    body_name=conducting_body_name,
                    official_url=official_url,
                )
            )

            exam = _get_or_create_exam(
                db=db,
                exam_name=extracted_exam_name,
                conducting_body=conducting_body,
                official_url=official_url,
            )

            notification = (
                _create_official_notification(
                    db=db,
                    exam=exam,
                    official_url=official_url,
                    pdf_path=str(pdf_path),
                    extraction=extraction,
                )
            )

            pending_extraction = (
                _create_pending_extraction(
                    db=db,
                    notification=notification,
                    pdf_path=str(pdf_path),
                    extraction=extraction,
                )
            )

            db.commit()

            db.refresh(
                pending_extraction
            )

            db.refresh(
                notification
            )

            db.refresh(
                exam
            )

            _log(
                "DATABASE PERSISTENCE COMPLETE"
            )

            _log(
                "PIPELINE COMPLETE: PENDING"
            )

            return {
                "id": (
                    pending_extraction.extraction_id
                ),
                "extraction_id": (
                    pending_extraction.extraction_id
                ),
                "notification_id": (
                    notification.notification_id
                ),
                "exam_id": (
                    exam.exam_id
                ),
                "exam_name": (
                    exam.name
                ),
                "official_url": (
                    official_url
                ),
                "pdf_path": (
                    str(pdf_path)
                ),
                "status": (
                    pending_extraction.extraction_status
                ),
                "approval_status": (
                    notification.approval_status
                ),
            }

        except Exception as error:

            db.rollback()

            _log(
                f"DATABASE PERSISTENCE FAILED: {error}"
            )

            if isinstance(
                error,
                ExamDiscoveryError,
            ):
                raise

            raise ExamDiscoveryError(
                "The discovered examination data could not "
                "be persisted safely."
            ) from error

# ============================================================
# DUPLICATE DISCOVERY REQUEST COALESCING
# ============================================================

_DISCOVERY_JOBS_LOCK = threading.Lock()
_DISCOVERY_JOBS: dict[str, dict] = {}


def _discovery_key(exam_name: str) -> str:
    return " ".join(exam_name.strip().casefold().split())


def discover_exam(
    exam_name: str,
) -> dict:
    """
    Public discovery entry point.

    If the frontend submits the same discovery request more than
    once while the first one is still running, the duplicate request
    waits for the first pipeline instead of starting a second complete
    web-search/PDF/AI pipeline.
    """

    key = _discovery_key(exam_name)

    if not key:
        raise ValueError(
            "Exam name cannot be empty."
        )

    with _DISCOVERY_JOBS_LOCK:
        job = _DISCOVERY_JOBS.get(key)

        if job is None:
            job = {
                "event": threading.Event(),
                "result": None,
                "error": None,
            }
            _DISCOVERY_JOBS[key] = job
            owner = True
        else:
            owner = False

    if not owner:
        _log(
            f"DUPLICATE DISCOVERY REQUEST COALESCED: {exam_name}"
        )

        job["event"].wait()

        if job["error"] is not None:
            raise job["error"]

        if job["result"] is None:
            raise ExamDiscoveryError(
                "The discovery pipeline completed without a result."
            )

        return dict(job["result"])

    try:
        result = _discover_exam_once(
            exam_name
        )

        with _DISCOVERY_JOBS_LOCK:
            job["result"] = result

        return dict(result)

    except Exception as error:
        with _DISCOVERY_JOBS_LOCK:
            job["error"] = error
        raise

    finally:
        job["event"].set()

        with _DISCOVERY_JOBS_LOCK:
            if _DISCOVERY_JOBS.get(key) is job:
                del _DISCOVERY_JOBS[key]
def _parse_extracted_date(value: str | None, field_name: str) -> date | None:
    """Parse an extracted ISO date into a database date."""

    if value is None:
        return None

    if not isinstance(value, str):
        raise ValueError(
            f"{field_name} must be a date string in YYYY-MM-DD format"
        )

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(
            f"{field_name} must be a date in YYYY-MM-DD format: {value!r}"
        ) from exc