from __future__ import annotations

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.chunk_extraction_result import ChunkExtractionResult
from app.ai.extraction_evidence import ExtractionEvidence
from app.ai.extraction_schemas import CompleteExtractionData
from app.ai.exam_schemas import (
    EligibilityInformation,
    ExamDateRange,
    ExamInformation,
)
from app.ai.eligibility_schemas import (
    EligibilityRuleGroupData,
    EligibilityRulesData,
)


def _merge_unique[T](items: list[T]) -> list[T]:
    """
    Preserve order while removing exact duplicates.
    """

    result: list[T] = []

    for item in items:
        if item not in result:
            result.append(item)

    return result


def _merge_scalar(
    field_name: str,
    values: list[str | int | None],
) -> str | int | None:
    """
    Safely merge a scalar field.

    Missing values are ignored.

    If all present values are identical, the value is kept.

    If different non-null values exist, an exception is raised.

    We never guess which conflicting value is correct.
    """

    present_values = [
        value
        for value in values
        if value is not None
    ]

    if not present_values:
        return None

    unique_values = _merge_unique(present_values)

    if len(unique_values) > 1:
        raise ValueError(
            f"Conflicting values found for "
            f"{field_name}: {unique_values}"
        )

    return unique_values[0]


def _merge_exam_dates(
    extractions: list[CompleteExtractionData],
) -> list[ExamDateRange]:
    """
    Merge examination date ranges.

    Exact duplicate ranges are removed.

    Different ranges are preserved because they may represent
    different examination sessions.
    """

    exam_dates: list[ExamDateRange] = []

    for extraction in extractions:
        for exam_date in extraction.exam_information.exam_dates:
            if exam_date not in exam_dates:
                exam_dates.append(exam_date)

    return exam_dates


def _merge_other_requirements(
    extractions: list[CompleteExtractionData],
) -> list[str]:
    """
    Merge explicitly extracted additional requirements.

    Exact duplicates are removed.
    Different requirements are preserved.
    """

    requirements: list[str] = []

    for extraction in extractions:
        requirements.extend(
            extraction.exam_information
            .eligibility.other_requirements
        )

    return _merge_unique(requirements)


def _merge_eligibility_information(
    extractions: list[CompleteExtractionData],
) -> EligibilityInformation:
    """
    Safely merge eligibility summary information.

    Scalar conflicts are rejected.

    Different additional requirements are preserved.
    """

    eligibility_information = [
        extraction.exam_information.eligibility
        for extraction in extractions
    ]

    return EligibilityInformation(
        minimum_age=_merge_scalar(
            "eligibility.minimum_age",
            [
                item.minimum_age
                for item in eligibility_information
            ],
        ),
        maximum_age=_merge_scalar(
            "eligibility.maximum_age",
            [
                item.maximum_age
                for item in eligibility_information
            ],
        ),
        educational_qualification=_merge_scalar(
            "eligibility.educational_qualification",
            [
                item.educational_qualification
                for item in eligibility_information
            ],
        ),
        nationality=_merge_scalar(
            "eligibility.nationality",
            [
                item.nationality
                for item in eligibility_information
            ],
        ),
        work_experience=_merge_scalar(
            "eligibility.work_experience",
            [
                item.work_experience
                for item in eligibility_information
            ],
        ),
        other_requirements=_merge_other_requirements(
            extractions
        ),
    )


def _merge_eligibility_rule_groups(
    extractions: list[CompleteExtractionData],
) -> list[EligibilityRuleGroupData]:
    """
    Safely aggregate eligibility rule groups.

    IMPORTANT:

    Rule groups originating from different chunks are NOT
    automatically merged.

    A chunk boundary has no logical meaning.

    For example:

        Chunk 1:
            AND
                Date of Birth >= 1994-08-02

        Chunk 2:
            AND
                Date of Birth <= 2005-08-01

    We cannot safely assume that these two groups belong
    to one logical expression.

    Therefore they remain separate.

    Exact duplicate groups are removed.

    Nested groups already explicitly represented inside
    an individual extraction are preserved exactly.
    """

    groups: list[EligibilityRuleGroupData] = []

    for extraction in extractions:
        for group in extraction.eligibility_rules.rule_groups:

            if group not in groups:
                groups.append(group)

    return groups


def _merge_evidence(
    results: list[ChunkExtractionResult],
) -> list[ExtractionEvidence]:
    """
    Collect and deduplicate provenance information.

    Evidence is produced by Python from the original
    DocumentChunk and is therefore not trusted to the LLM.
    """

    evidence: list[ExtractionEvidence] = []

    for result in results:
        evidence.extend(result.evidence)

    return _merge_unique(evidence)


def aggregate_chunk_extractions(
    results: list[ChunkExtractionResult],
) -> AggregatedExtractionResult:
    """
    Aggregate structured information extracted from multiple
    document chunks while preserving provenance.

    Safety principles:

    1. Missing information is ignored.
    2. Exact duplicate information is removed.
    3. Conflicting scalar information raises ValueError.
    4. Different examination date ranges are preserved.
    5. Different eligibility requirements are preserved.
    6. Rule groups from different chunks are NOT logically merged.
    7. Nested logical structures are preserved.
    8. No logical relationship is inferred across chunks.
    9. Evidence is preserved.
    10. No LLM is used during aggregation.

    The result should subsequently go through:

        normalization
            ↓
        validation
            ↓
        HITL review
            ↓
        approval
    """

    if not results:
        raise ValueError(
            "At least one chunk extraction result is required."
        )

    # Extract the structured extraction objects.
    extractions = [
        result.extraction
        for result in results
    ]

    # ---------------------------------------------------------
    # EXAM INFORMATION
    # ---------------------------------------------------------

    exam_name = _merge_scalar(
        "exam_information.exam_name",
        [
            extraction.exam_information.exam_name
            for extraction in extractions
        ],
    )

    conducting_body = _merge_scalar(
        "exam_information.conducting_body",
        [
            extraction.exam_information.conducting_body
            for extraction in extractions
        ],
    )

    release_date = _merge_scalar(
        "exam_information.release_date",
        [
            extraction.exam_information.release_date
            for extraction in extractions
        ],
    )

    application_start_date = _merge_scalar(
        "exam_information.application_start_date",
        [
            extraction.exam_information.application_start_date
            for extraction in extractions
        ],
    )

    application_end_date = _merge_scalar(
        "exam_information.application_end_date",
        [
            extraction.exam_information.application_end_date
            for extraction in extractions
        ],
    )

    exam_dates = _merge_exam_dates(extractions)

    eligibility = _merge_eligibility_information(
        extractions
    )

    exam_information = ExamInformation(
        exam_name=exam_name,
        conducting_body=conducting_body,
        release_date=release_date,
        application_start_date=application_start_date,
        application_end_date=application_end_date,
        exam_dates=exam_dates,
        eligibility=eligibility,
    )

    # ---------------------------------------------------------
    # ELIGIBILITY RULES
    # ---------------------------------------------------------

    rule_groups = _merge_eligibility_rule_groups(
        extractions
    )

    eligibility_rules = EligibilityRulesData(
        rule_groups=rule_groups
    )

    # ---------------------------------------------------------
    # EVIDENCE
    # ---------------------------------------------------------

    evidence = _merge_evidence(results)

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    return AggregatedExtractionResult(
        extraction=CompleteExtractionData(
            exam_information=exam_information,
            eligibility_rules=eligibility_rules,
        ),
        evidence=evidence,
    )