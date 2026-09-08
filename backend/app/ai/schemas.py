from pydantic import BaseModel, Field


class EligibilityInformation(BaseModel):
    minimum_age: int | None = None
    maximum_age: int | None = None

    educational_qualification: str | None = None
    nationality: str | None = None
    work_experience: str | None = None

    other_requirements: list[str] = Field(default_factory=list)


class ExamInformation(BaseModel):
    exam_name: str | None = None
    conducting_body: str | None = None

    application_start_date: str | None = None
    application_end_date: str | None = None
    exam_date: str | None = None

    eligibility: EligibilityInformation