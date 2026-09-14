from __future__ import annotations

import json

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)


def serialize_aggregated_extraction(
    result: AggregatedExtractionResult,
) -> str:
    """
    Serialize the complete aggregated extraction,
    including evidence, for persistent storage.
    """

    return json.dumps(
        result.model_dump(),
        ensure_ascii=False,
    )


def deserialize_aggregated_extraction(
    value: str,
) -> AggregatedExtractionResult:
    """
    Restore an aggregated extraction from persistent storage.
    """

    data = json.loads(value)

    return AggregatedExtractionResult.model_validate(
        data
    )