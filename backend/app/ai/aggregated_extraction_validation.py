from __future__ import annotations

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.complete_extraction_validation import (
    validate_complete_extraction,
)


def validate_aggregated_extraction(
    result: AggregatedExtractionResult,
) -> list[str]:
    """
    Validate the aggregated structured extraction.

    Evidence is not modified because validation is read-only.
    """

    return validate_complete_extraction(
        result.extraction
    )