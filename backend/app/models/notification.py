from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Notification(Base):
    __tablename__ = "notification"

    notification_id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.student_id")
    )

    exam_id: Mapped[int | None] = mapped_column(
        ForeignKey("exam.exam_id")
    )

    notification_type: Mapped[str]
    title: Mapped[str]
    message: Mapped[str]
    is_read: Mapped[bool]

    created_at: Mapped[datetime | None]
    read_at: Mapped[datetime | None]

    student: Mapped["Student"] = relationship(
        back_populates="notifications"
    )

    exam: Mapped["Exam | None"] = relationship(
        back_populates="notifications"
    )