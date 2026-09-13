from __future__ import annotations


def chunk_text(
    text: str,
    chunk_size: int = 30000,
) -> list[str]:
    """
    Split the complete document into chunks.

    Every character from the original text is preserved.
    No content is filtered or removed.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    chunks = []

    for start in range(0, len(text), chunk_size):
        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

    return chunks