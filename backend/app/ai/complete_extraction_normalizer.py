from datetime import datetime

from app.ai.extraction_schemas import CompleteExtractionData
from app.ai.eligibility_rule_normalizer import (
    normalize_eligibility_rules,
)


def normalize_date(value: str | None) -> str | None:
    if value is None:
        return None

    value = value.strip()

    # Already normalized
    try:
        parsed_date = datetime.strptime(value, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Common formats Gemini may return
    formats = [
        "%d %B, %Y",
        "%d %B %Y",
        "%B %d, %Y",
        "%B %d %Y",
        "%d.%m.%Y"
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(
                value,
                date_format
            )
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(
        f"Unable to normalize date: {value}"
    )


def normalize_exam_information(exam_information):
    normalized_exam_dates = []

    for exam_date in exam_information.exam_dates:
        start_date = normalize_date(exam_date.start_date)
        end_date = normalize_date(exam_date.end_date)

        normalized_exam_dates.append(
            exam_date.model_copy(
                update={
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )
        )

    return exam_information.model_copy(
        update={
            "release_date": normalize_date(
                exam_information.release_date
            ),
            "application_start_date": normalize_date(
                exam_information.application_start_date
            ),
            "application_end_date": normalize_date(
                exam_information.application_end_date
            ),
            "exam_dates": normalized_exam_dates,
        }
    )


def normalize_complete_extraction(
    extraction: CompleteExtractionData,
) -> CompleteExtractionData:

    normalized_exam_information = normalize_exam_information(
        extraction.exam_information
    )

    normalized_eligibility_rules = normalize_eligibility_rules(
        extraction.eligibility_rules
    )

    return CompleteExtractionData(
        exam_information=normalized_exam_information,
        eligibility_rules=normalized_eligibility_rules,
    )