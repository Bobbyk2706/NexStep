from __future__ import annotations

from pydantic import BaseModel, Field


class ExtractionEvidence(BaseModel):
    """
    Identifies where an extracted piece of information came from
    in the original document.
    """

    chunk_number: int
    page_numbers: list[int] = Field(default_factory=list)
    source_text: str