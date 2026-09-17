from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pymupdf
import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parents[2]

STORAGE_DIR = (
    BASE_DIR
    / "storage"
    / "notifications"
)

STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# WEBSITE FETCHING
# ============================================================


def fetch_website(url):
    response = requests.get(
        url,
        timeout=20,
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        "",
    )

    return response, content_type


# ============================================================
# LINK EXTRACTION
# ============================================================


def extract_links(
    html,
    base_url,
):
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    links = soup.find_all("a")

    seen_urls = set()
    relevant_links = []

    for link in links:

        href = link.get("href")

        if not href:
            continue

        if href.startswith(
            "javascript:"
        ):
            continue

        if href.startswith("#"):
            continue

        full_url = urljoin(
            base_url,
            href,
        )

        if not full_url.startswith(
            "https"
        ):
            continue

        if full_url in seen_urls:
            continue

        seen_urls.add(full_url)

        text = link.get_text(
            strip=True
        )

        relevant_links.append(
            {
                "url": full_url,
                "text": text,
            }
        )

    return relevant_links


# ============================================================
# PDF DETECTION
# ============================================================


def is_pdf(
    content_type,
    url,
):
    """
    Determine whether a resource is likely a PDF based on
    HTTP Content-Type or URL.

    This function is used during source discovery.

    Actual downloaded PDF content is validated separately
    using the PDF file signature.
    """

    if (
        "application/pdf"
        in content_type.lower()
    ):
        return True

    if url.lower().endswith(".pdf"):
        return True

    return False


def _has_pdf_signature(
    content,
):
    """
    Check the PDF magic number.

    A valid PDF begins with:

        %PDF-
    """

    return content.startswith(
        b"%PDF-"
    )


# ============================================================
# PDF STORAGE
# ============================================================


def get_pdf_filename(url):
    parsed_url = urlparse(url)

    filename = os.path.basename(
        parsed_url.path
    )

    if not filename:
        filename = "document.pdf"

    if not filename.lower().endswith(
        ".pdf"
    ):
        filename += ".pdf"

    return filename


def download_pdf(url):
    """
    Download and validate a PDF.

    The response is accepted only when the actual content
    begins with the PDF signature.

    A generic Content-Type such as application/octet-stream
    is allowed when the downloaded bytes are actually a PDF.

    The returned document_hash is the SHA-256 hash of the
    exact downloaded bytes.
    """

    response = requests.get(
        url,
        timeout=20,
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        "",
    ).lower()

    pdf_content = response.content

    if not pdf_content:
        raise ValueError(
            "Downloaded document is empty."
        )

    if not _has_pdf_signature(
        pdf_content
    ):
        raise ValueError(
            "Downloaded content is not a valid PDF."
        )

    document_hash = hashlib.sha256(
        pdf_content
    ).hexdigest()

    filename = get_pdf_filename(
        url
    )

    file_path = (
        STORAGE_DIR
        / filename
    )

    with open(
        file_path,
        "wb",
    ) as file:
        file.write(
            pdf_content
        )

    return {
        "content": pdf_content,
        "path": str(file_path),
        "url": url,
        "document_hash": document_hash,
        "content_type": content_type,
    }


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================


def extract_pdf_text(
    pdf_content,
):
    if not pdf_content:
        raise ValueError(
            "PDF content is empty."
        )

    if not _has_pdf_signature(
        pdf_content
    ):
        raise ValueError(
            "Content is not a valid PDF."
        )

    doc = pymupdf.open(
        stream=pdf_content,
        filetype="pdf",
    )

    try:
        text = ""

        for page in doc:
            text += (
                page.get_text()
                + "\n"
            )

        return text

    finally:
        doc.close()


# ============================================================
# DIRECT SOURCE DISCOVERY
# ============================================================


def discover_exam_sources(
    official_url,
):
    response, content_type = fetch_website(
        official_url
    )

    if is_pdf(
        content_type,
        official_url,
    ):
        pdf = download_pdf(
            official_url
        )

        text = extract_pdf_text(
            pdf["content"]
        )

        return {
            "url": official_url,
            "content_type": content_type,
            "text": text,
            "content": pdf["content"],
            "pdf_path": pdf["path"],
            "document_url": pdf["url"],
            "document_hash": pdf[
                "document_hash"
            ],
        }

    if "text/html" not in content_type.lower():
        return []

    links = extract_links(
        response.text,
        official_url,
    )

    # The previous implementation referenced `text` and
    # `pdf` here even though they only existed in the PDF
    # branch. Return the discovered links instead.
    return links


# ============================================================
# CONTROLLED CRAWLING
# ============================================================


MAX_DEPTH = 2


def crawl_exam_sources(
    official_url,
):
    visited = set()

    to_visit = [
        (
            official_url,
            0,
        )
    ]

    discovered_sources = []

    while to_visit:

        current_url, depth = (
            to_visit.pop(0)
        )

        if current_url in visited:
            continue

        if depth > MAX_DEPTH:
            continue

        visited.add(
            current_url
        )

        try:
            response, content_type = (
                fetch_website(
                    current_url
                )
            )

        except Exception as error:
            print(
                "Failed:",
                current_url,
                error,
            )
            continue

        # ----------------------------------------------------
        # PDF SOURCE
        # ----------------------------------------------------

        if is_pdf(
            content_type,
            current_url,
        ):

            try:
                pdf = download_pdf(
                    current_url
                )

                text = extract_pdf_text(
                    pdf["content"]
                )

                discovered_sources.append(
                    {
                        "url": current_url,
                        "content_type": content_type,
                        "text": text,
                        "content": pdf[
                            "content"
                        ],
                        "pdf_path": pdf[
                            "path"
                        ],
                        "document_url": pdf[
                            "url"
                        ],
                        "document_hash": pdf[
                            "document_hash"
                        ],
                    }
                )

            except Exception as error:
                print(
                    "PDF failed:",
                    current_url,
                    error,
                )

            continue

        # ----------------------------------------------------
        # NON-HTML RESOURCE
        # ----------------------------------------------------

        if (
            "text/html"
            not in content_type.lower()
        ):
            continue

        # ----------------------------------------------------
        # HTML PAGE
        # ----------------------------------------------------

        links = extract_links(
            response.text,
            current_url,
        )

        for link in links:

            next_url = link["url"]

            if next_url in visited:
                continue

            discovered_sources.append(
                link
            )

            if depth < MAX_DEPTH:
                to_visit.append(
                    (
                        next_url,
                        depth + 1,
                    )
                )

    return discovered_sources