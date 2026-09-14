from __future__ import annotations

from pydantic import BaseModel

from app.ai.extraction_evidence import ExtractionEvidence
from app.ai.extraction_schemas import CompleteExtractionData


class ChunkExtractionResult(BaseModel):
    extraction: CompleteExtractionData
    evidence: list[ExtractionEvidence]