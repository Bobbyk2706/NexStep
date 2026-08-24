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

    student: Mapped["Student"] = relationship(
        back_populates="educations"
    )
    