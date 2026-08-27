import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pymupdf
KEYWORDS = [
    "exam",
    "examination",
    "notification",
    "calendar",
    "active-exams",
    "forthcoming-exams",
]


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

def is_candidate_source(url, text):

    url = url.lower()
    text = text.lower()

    if (
        any(keyword in url for keyword in KEYWORDS)
        or
        any(keyword in text for keyword in KEYWORDS)
    ):
        return True

    return False

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

        text = link.get_text(
            strip=True
        )

        if not is_candidate_source(full_url, text):
            continue

        relevant_links.append({
            "url": full_url,
            "text": text
        })

    return relevant_links


def discover_exam_sources(official_url):

    response, content_type = fetch_website(
        official_url
    )
    if is_pdf(content_type,official_url):
        pdf_content=download_pdf(official_url)
        text=extract_pdf_text(pdf_content)
        return {
            'content_type':content_type,
            'text':text,
            'url':official_url        
        }

    if "text/html" not in content_type.lower():
        return []

    return extract_links(
        response.text,
        official_url
    ) 
def is_pdf(content_type,url):
    if 'application/pdf' in content_type.lower() or url.lower().endswith('.pdf'):
        return True
    return False
def download_pdf(url):
    response=requests.get(url,timeout=20)
    response.raise_for_status()
    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()
    if "application/pdf" not in content_type:
        raise ValueError(
            f"Expected PDF but received: {content_type}"
        )
    return response.content
def extract_pdf_text(pdf_content):
    doc = pymupdf.open(
        stream=pdf_content,
        filetype="pdf"
    )
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text