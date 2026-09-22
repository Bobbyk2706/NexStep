from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MonitoringReview(Base):
    """
    Human-in-the-loop review record for a monitored
    notification change.

    The review stores the complete AI/deterministic
    analysis required by an administrator before the
    change can be approved.
    """

    __tablename__ = "monitoringreview"

    review_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    notification_id: Mapped[int] = mapped_column(
        ForeignKey(
            "officialnotification.notification_id"
        ),
        nullable=False,
    )

    old_document_hash: Mapped[str]
    new_document_hash: Mapped[str]

    old_extraction: Mapped[str]
    new_extraction: Mapped[str]

    structural_changes: Mapped[str]
    semantic_analysis: Mapped[str]
    impact_analysis: Mapped[str]

    review_status: Mapped[str] = mapped_column(
        default="PENDING"
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        nullable=True
    )

    reviewed_by: Mapped[int | None] = mapped_column(
        ForeignKey("admin.admin_id"),
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now
    )

    notification = relationship(
        "OfficialNotification",
    )

    reviewer = relationship(
        "Admin",
    )