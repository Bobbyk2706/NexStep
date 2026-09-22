from __future__ import annotations

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.complete_extraction_normalizer import (
    normalize_complete_extraction,
)


def normalize_aggregated_extraction(
    result: AggregatedExtractionResult,
) -> AggregatedExtractionResult:
    """
    Normalize the structured extraction while preserving
    all provenance evidence unchanged.
    """

    normalized_extraction = normalize_complete_extraction(
        result.extraction
    )

    return AggregatedExtractionResult(
        extraction=normalized_extraction,
        evidence=result.evidence.copy(),
    )