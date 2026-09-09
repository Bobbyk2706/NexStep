from datetime import date

from app.ai.schemas import ExamInformation


def validate_exam_information(exam: ExamInformation) -> list[str]:
    errors = []

    if (
        exam.application_start_date
        and exam.application_end_date
    ):
        start_date = date.fromisoformat(exam.application_start_date)
        end_date = date.fromisoformat(exam.application_end_date)

        if start_date > end_date:
            errors.append(
                "Application start date is after application end date."
            )

    if (
        exam.application_end_date
        and exam.exam_date
    ):
        application_end = date.fromisoformat(
            exam.application_end_date
        )
        exam_date = date.fromisoformat(
            exam.exam_date
        )

        if application_end > exam_date:
            errors.append(
                "Application end date is after exam date."
            )

    if (
        exam.eligibility.minimum_age is not None
        and exam.eligibility.maximum_age is not None
    ):
        if exam.eligibility.minimum_age > exam.eligibility.maximum_age:
            errors.append(
                "Minimum age is greater than maximum age."
            )

    return errors