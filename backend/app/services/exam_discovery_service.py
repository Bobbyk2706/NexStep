import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pymupdf

STORAGE_DIR = Path("storage/notifications")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_website(url):
    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        ""
    )

    return response, content_type


def extract_links(html, base_url):
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = soup.find_all("a")

    seen_urls = set()
    relevant_links = []

    for link in links:
        href = link.get("href")

        if not href:
            continue

        if href.startswith("javascript:"):
            continue

        if href.startswith("#"):
            continue

        full_url = urljoin(
            base_url,
            href
        )

        if not full_url.startswith("https"):
            continue

        if full_url in seen_urls:
            continue

        seen_urls.add(full_url)

        text = link.get_text(strip=True)

        relevant_links.append({
            "url": full_url,
            "text": text
        })

    return relevant_links


def is_pdf(content_type, url):
    if (
        "application/pdf" in content_type.lower()
        or url.lower().endswith(".pdf")
    ):
        return True

    return False


def get_pdf_filename(url):
    parsed_url = urlparse(url)

    filename = os.path.basename(
        parsed_url.path
    )

    if not filename:
        filename = "document.pdf"

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    return filename


def download_pdf(url):
    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    if "application/pdf" not in content_type:
        raise ValueError(
            f"Expected PDF but received: {content_type}"
        )

    pdf_content = response.content

    filename = get_pdf_filename(url)
    file_path = STORAGE_DIR / filename

    with open(file_path, "wb") as file:
        file.write(pdf_content)

    return {
        "content": pdf_content,
        "path": str(file_path)
    }


def extract_pdf_text(pdf_content):
    doc = pymupdf.open(
        stream=pdf_content,
        filetype="pdf"
    )

    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    doc.close()

    return text


def discover_exam_sources(official_url):
    response, content_type = fetch_website(
        official_url
    )

    if is_pdf(
        content_type,
        official_url
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
            "pdf_path": pdf["path"]
        }

    if "text/html" not in content_type.lower():
        return []

    links = extract_links(
        response.text,
        official_url
    )

    return {
        "url": official_url,
        "content_type": content_type,
        "text": response.text,
        "links": links
    }


MAX_DEPTH = 2


def crawl_exam_sources(official_url):
    visited = set()

    to_visit = [
        (official_url, 0)
    ]

    discovered_sources = []

    while to_visit:
        current_url, depth = to_visit.pop(0)

        if current_url in visited:
            continue

        if depth > MAX_DEPTH:
            continue

        visited.add(current_url)

        try:
            response, content_type = fetch_website(
                current_url
            )

        except Exception as e:
            print(
                "Failed:",
                current_url,
                e
            )
            continue

        if is_pdf(
            content_type,
            current_url
        ):
            try:
                pdf = download_pdf(
                    current_url
                )

                text = extract_pdf_text(
                    pdf["content"]
                )

                discovered_sources.append({
                    "url": current_url,
                    "content_type": content_type,
                    "text": text,
                    "pdf_path": pdf["path"]
                })

            except Exception as e:
                print(
                    "PDF failed:",
                    current_url,
                    e
                )

            continue

        if "text/html" not in content_type.lower():
            continue

        links = extract_links(
            response.text,
            current_url
        )

        for link in links:
            next_url = link["url"]

            if next_url in visited:
                continue

            discovered_sources.append(link)

            if depth < MAX_DEPTH:
                to_visit.append(
                    (
                        next_url,
                        depth + 1
                    )
                )

    return discovered_sources