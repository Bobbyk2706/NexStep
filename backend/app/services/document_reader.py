from __future__ import annotations

from pathlib import Path

import pymupdf


def extract_pdf_pages(
    pdf_path: str | Path,
) -> list[str]:
    """
    Extract PDF text page-by-page.

    The returned list preserves the original PDF page order.

    No text is filtered, normalized, or discarded.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    pages: list[str] = []

    document = pymupdf.open(path)

    try:
        for page in document:
            pages.append(page.get_text())
    finally:
        document.close()

    return pages