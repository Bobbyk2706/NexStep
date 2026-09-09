from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.official_notification import OfficialNotification


class ExtractionHistory(Base):
    __tablename__ = "extractionhistory"

    extraction_id: Mapped[int] = mapped_column(primary_key=True)

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("officialnotification.notification_id")
    )

    extraction_type: Mapped[str]
    source_pdf_path: Mapped[str]

    extracted_content: Mapped[str | None]
    ai_summary: Mapped[str | None]

    change_detected: Mapped[bool]
    change_details: Mapped[str | None]

    extraction_status: Mapped[str]

    created_at: Mapped[datetime | None]

    notification: Mapped["OfficialNotification"] = relationship(
        back_populates="extraction_history"
    )