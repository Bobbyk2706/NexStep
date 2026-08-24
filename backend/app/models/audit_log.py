from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "auditlog"

    audit_id: Mapped[int] = mapped_column(primary_key=True)

    admin_id: Mapped[int | None] = mapped_column(
        ForeignKey("admin.admin_id")
    )

    action_type: Mapped[str]
    entity_type: Mapped[str]

    entity_id: Mapped[int | None]
    description: Mapped[str | None]
    old_value: Mapped[str | None]
    new_value: Mapped[str | None]

    created_at: Mapped[datetime | None]

    admin: Mapped["Admin | None"] = relationship(
        back_populates="audit_logs"
    )