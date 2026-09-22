from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class WorkExperience(Base):
    __tablename__ = "work_experience"

    work_experience_id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.student_id")
    )

    company: Mapped[str | None]
    role: Mapped[str | None]
    duration: Mapped[str | None]

    student: Mapped["Student"] = relationship(
        back_populates="work_experiences"
    )