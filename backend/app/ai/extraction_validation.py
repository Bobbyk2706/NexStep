from app.ai.extraction_schemas import CompleteExtractionData
from app.ai.eligibility_rule_normalizer import normalize_eligibility_rules
from app.ai.eligibility_rule_validation import validate_eligibility_rules


def normalize_and_validate_extraction(
    extraction: CompleteExtractionData
) -> CompleteExtractionData:

    normalized_eligibility = normalize_eligibility_rules(
        extraction.eligibility_rules
    )

    validation_errors = validate_eligibility_rules(
        normalized_eligibility
    )

    if validation_errors:
        raise ValueError(
            "Eligibility validation failed: "
            + " | ".join(validation_errors)
        )

    return CompleteExtractionData(
        exam_information=extraction.exam_information,
        eligibility_rules=normalized_eligibility
    )