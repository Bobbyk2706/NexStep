from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.exam_date import ExamDate
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.exam import Exam
    from app.models.eligibility_rule_group import EligibilityRuleGroup
    from app.models.extraction_history import ExtractionHistory

class OfficialNotification(Base):
    __tablename__ = "officialnotification"

    notification_id: Mapped[int] = mapped_column(primary_key=True)

    exam_id: Mapped[int] = mapped_column(
        ForeignKey("exam.exam_id")
    )

    title: Mapped[str]
    notification_type: Mapped[str]

    release_date: Mapped[date | None]
    application_start_date: Mapped[date | None]
    application_end_date: Mapped[date | None]

    exam_dates: Mapped[list["ExamDate"]] = relationship(
        back_populates="notification",
        cascade="all, delete-orphan"
    )

    official_url: Mapped[str]
    pdf_path: Mapped[str]

    ai_summary: Mapped[str | None]
    ai_change_summary: Mapped[str | None]

    approval_status: Mapped[str]
    rejection_reason: Mapped[str | None]

    downloaded_on: Mapped[datetime | None]

    exam: Mapped["Exam"] = relationship(
    back_populates="official_notifications"
    )

    rule_groups: Mapped[list["EligibilityRuleGroup"]] = relationship(
        back_populates="notification"
    )

    extraction_history: Mapped[list["ExtractionHistory"]] = relationship(
        back_populates="notification"
    )
    exam_dates: Mapped[list["ExamDate"]] = relationship(
    back_populates="notification",
    cascade="all, delete-orphan"
)