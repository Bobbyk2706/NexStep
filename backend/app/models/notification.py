from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String
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

    # --- email delivery -------------------------------------------------
    #
    # Prevents the same event from notifying the same student twice
    # (for example one deadline reminder tier). NULL = no de-duplication;
    # PostgreSQL allows many NULLs in a unique index.
    dedupe_key: Mapped[str | None] = mapped_column(
        String(200), unique=True, index=True
    )

    # NULL (no email wanted) | PENDING | SENT | FAILED | SKIPPED
    email_status: Mapped[str | None] = mapped_column(String(20))
    email_sent_at: Mapped[datetime | None]
    email_error: Mapped[str | None]

    student: Mapped["Student"] = relationship(
        back_populates="notifications"
    )

    exam: Mapped["Exam | None"] = relationship(
        back_populates="notifications"
    )