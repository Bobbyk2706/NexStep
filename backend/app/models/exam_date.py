from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.official_notification import OfficialNotification


class ExamDate(Base):
    __tablename__ = "examdate"

    exam_date_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("officialnotification.notification_id")
    )

    start_date: Mapped[date]
    end_date: Mapped[date]

    notification: Mapped["OfficialNotification"] = relationship(
        back_populates="exam_dates"
    )