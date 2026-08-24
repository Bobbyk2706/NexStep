from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.models.base import Base


class StudentExamEligibility(Base):
    __tablename__ = "studentexameligibility"

    eligibility_id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.student_id")
    )

    exam_id: Mapped[int] = mapped_column(
        ForeignKey("exam.exam_id")
    )

    eligibility_status: Mapped[str]
    reason: Mapped[str | None]
    evaluated_at: Mapped[datetime | None]
    student: Mapped["Student"] = relationship(
    back_populates="eligibility_records"
    )

    exam: Mapped["Exam"] = relationship(
    back_populates="eligibility_records"
    )