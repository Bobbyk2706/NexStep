from datetime import date

from app.ai.schemas import ExamInformation


def validate_exam_information(
    exam: ExamInformation
) -> list[str]:

    errors = []

    # Application date validation
    if (
        exam.application_start_date
        and exam.application_end_date
    ):
        start_date = date.fromisoformat(
            exam.application_start_date
        )

        end_date = date.fromisoformat(
            exam.application_end_date
        )

        if start_date > end_date:
            errors.append(
                "Application start date is after "
                "application end date."
            )

    # Exam date range validation
    for exam_date in exam.exam_dates:

        start_date = date.fromisoformat(
            exam_date.start_date
        )

        end_date = date.fromisoformat(
            exam_date.end_date
        )

        if start_date > end_date:
            errors.append(
                "Exam start date is after exam end date."
            )

    # Application must end before the examination begins
    if (
        exam.application_end_date
        and exam.exam_dates
    ):
        application_end = date.fromisoformat(
            exam.application_end_date
        )

        earliest_exam_date = min(
            date.fromisoformat(
                exam_date.start_date
            )
            for exam_date in exam.exam_dates
        )

        if application_end > earliest_exam_date:
            errors.append(
                "Application end date is after "
                "the examination begins."
            )

    # Age validation
    if (
        exam.eligibility.minimum_age is not None
        and exam.eligibility.maximum_age is not None
    ):
        if (
            exam.eligibility.minimum_age
            > exam.eligibility.maximum_age
        ):
            errors.append(
                "Minimum age is greater than maximum age."
            )

    return errors