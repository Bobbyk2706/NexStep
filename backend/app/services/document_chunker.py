from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    """
    A lossless portion of a document together with its
    original page provenance.
    """

    chunk_number: int
    text: str
    page_numbers: list[int]


def chunk_document_pages(
    pages: list[str],
    chunk_size: int = 30000,
) -> list[DocumentChunk]:
    """
    Create lossless chunks from page text while preserving
    the pages contributing to each chunk.

    No text is filtered or discarded.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    if not pages:
        return []

    chunks: list[DocumentChunk] = []

    current_text = ""
    current_pages: list[int] = []

    for page_number, page_text in enumerate(pages, start=1):

        if not page_text:
            continue

        remaining_text = page_text

        while remaining_text:

            available = chunk_size - len(current_text)

            piece = remaining_text[:available]
            remaining_text = remaining_text[available:]

            current_text += piece

            if page_number not in current_pages:
                current_pages.append(page_number)

            if len(current_text) == chunk_size:
                chunks.append(
                    DocumentChunk(
                        chunk_number=len(chunks) + 1,
                        text=current_text,
                        page_numbers=current_pages.copy(),
                    )
                )

                current_text = ""
                current_pages = []

    if current_text:
        chunks.append(
            DocumentChunk(
                chunk_number=len(chunks) + 1,
                text=current_text,
                page_numbers=current_pages.copy(),
            )
        )

    return chunks
def chunk_text(
    text: str,
    chunk_size: int = 30000,
) -> list[str]:
    """
    Losslessly split plain document text into fixed-size chunks.

    This is a compatibility helper for callers that only have
    complete document text and do not need page provenance.

    No characters are filtered, normalized, or discarded.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    if not text:
        return []

    return [
        text[start:start + chunk_size]
        for start in range(0, len(text), chunk_size)
    ]