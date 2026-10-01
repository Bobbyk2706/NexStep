from __future__ import annotations

from pydantic import BaseModel, Field


class ExtractionEvidence(BaseModel):
    """
    Identifies where an extracted piece of information came from
    in the original document.

    The first three fields are the original (chunk-based) shape and
    are kept unchanged so previously stored extractions still load.
    The remaining fields are populated by the v2 pipeline.
    """

    chunk_number: int
    page_numbers: list[int] = Field(default_factory=list)
    source_text: str

    # --- v2 pipeline (all optional, backward compatible) ---------

    # Human-readable name of the extracted field this supports,
    # e.g. "Application end date" or "Eligibility: nationality".
    field: str | None = None

    # True  = the quoted text was located in the source document.
    # False = the model quoted text that could not be located.
    # None  = not checked (legacy extractions).
    verified: bool | None = None

    # Title of the document section the passage belongs to.
    section: str | None = None
