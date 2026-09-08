from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Education(Base):
    __tablename__ = "education"

    education_id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.student_id")
    )

    qualification: Mapped[str]
    specialization: Mapped[str | None]
    cgpa: Mapped[float | None]
    percentage: Mapped[float | None]
    current_year: Mapped[int | None]
    year_of_passing: Mapped[int | None]
    is_current: Mapped[bool | None]

    # Added for the profile flow (see
    # database/migrations/0002_profile_schema.sql).
    institution: Mapped[str | None]
    # e.g. "Final Year"/"Graduated" — the frontend's yearOfStudy is a
    # label, not the numeric current_year above, so kept separate.
    year_of_study_label: Mapped[str | None]
    # True only on the single "previousQualification" entry — see
    # migration 0002 for why this exists.
    is_higher_qualification: Mapped[bool | None]

    student: Mapped["Student"] = relationship(
        back_populates="educations"
    )