from pydantic import BaseModel, Field


class QualificationEntry(BaseModel):
    """Shape used for both the repeatable `qualifications` list and the
    single `previousQualification` entry — the frontend uses the same
    field set for both."""
    level: str
    institution: str | None = None
    field: str | None = None
    yearCompleted: str | None = None
    score: str | None = None


class WorkExperienceEntry(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None


class ProfileIn(BaseModel):
    name: str
    dob: str
    nationality: str
    state: str
    college: str
    branch: str
    yearOfStudy: str
    cgpa: str | None = None
    percentage: str | None = None
    qualifications: list[QualificationEntry] = Field(default_factory=list)
    workExperience: list[WorkExperienceEntry] = Field(default_factory=list)
    hasHigherQualification: bool = False
    previousQualification: QualificationEntry | None = None


class ProfileOut(BaseModel):
    name: str
    dob: str | None = None
    nationality: str | None = None
    state: str | None = None
    college: str | None = None
    branch: str | None = None
    yearOfStudy: str | None = None
    cgpa: str | None = None
    percentage: str | None = None
    qualifications: list[QualificationEntry] = Field(default_factory=list)
    workExperience: list[WorkExperienceEntry] = Field(default_factory=list)
    hasHigherQualification: bool = False
    previousQualification: QualificationEntry | None = None