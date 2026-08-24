from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TrackedExam(Base):
    __tablename__ = "trackedexam"

    tracking_id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.student_id")
    )

    exam_id: Mapped[int] = mapped_column(
        ForeignKey("exam.exam_id")
    )

    tracked_at: Mapped[datetime | None]
    tracking_status: Mapped[str]

    student: Mapped["Student"] = relationship(
        back_populates="tracked_exams"
    )

    exam: Mapped["Exam"] = relationship(
        back_populates="tracked_exams"
    )