from datetime import date

from app.ai.extraction_schemas import CompleteExtractionData
from app.ai.eligibility_rule_validation import (
    validate_eligibility_rules,
)


def validate_exam_information(
    extraction: CompleteExtractionData
) -> list[str]:

    errors = []

    exam_information = extraction.exam_information

    # -----------------------------
    # Required basic information
    # -----------------------------

    if not exam_information.exam_name:
        errors.append(
            "Exam information: exam_name cannot be empty."
        )

    if not exam_information.conducting_body:
        errors.append(
            "Exam information: conducting_body cannot be empty."
        )

    # -----------------------------
    # Validate dates
    # -----------------------------

    date_fields = {
        "release_date": exam_information.release_date,
        "application_start_date":
            exam_information.application_start_date,
        "application_end_date":
            exam_information.application_end_date,
    }

    parsed_dates = {}

    for field_name, value in date_fields.items():

        if value is None:
            continue

        try:
            parsed_dates[field_name] = date.fromisoformat(value)
        except ValueError:
            errors.append(
                f"Exam information: {field_name} "
                f"must use YYYY-MM-DD format."
            )

    # -----------------------------
    # Application date consistency
    # -----------------------------

    application_start = parsed_dates.get(
        "application_start_date"
    )

    application_end = parsed_dates.get(
        "application_end_date"
    )

    if application_start and application_end:

        if application_start > application_end:
            errors.append(
                "Exam information: "
                "application_start_date cannot be "
                "after application_end_date."
            )

    # -----------------------------
    # Validate examination dates
    # -----------------------------

    for index, exam_date in enumerate(
        exam_information.exam_dates,
        start=1
    ):

        try:
            start_date = date.fromisoformat(
                exam_date.start_date
            )
        except ValueError:
            errors.append(
                f"Exam information: "
                f"exam_dates[{index}].start_date "
                f"must use YYYY-MM-DD format."
            )
            start_date = None

        try:
            end_date = date.fromisoformat(
                exam_date.end_date
            )
        except ValueError:
            errors.append(
                f"Exam information: "
                f"exam_dates[{index}].end_date "
                f"must use YYYY-MM-DD format."
            )
            end_date = None

        if start_date and end_date:

            if start_date > end_date:
                errors.append(
                    f"Exam information: "
                    f"exam_dates[{index}].start_date "
                    f"cannot be after end_date."
                )

    return errors


def validate_complete_extraction(
    extraction: CompleteExtractionData
) -> list[str]:

    errors = []

    # Validate exam information
    errors.extend(
        validate_exam_information(extraction)
    )

    # Validate eligibility rules
    errors.extend(
        validate_eligibility_rules(
            extraction.eligibility_rules
        )
    )

    return errors