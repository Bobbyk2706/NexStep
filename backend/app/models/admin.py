from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Admin(Base):
    __tablename__ = "admin"

    admin_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    account_status: Mapped[str | None]

    updated_timestamp: Mapped[datetime | None]
    created_timestamp: Mapped[datetime | None]

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="admin"
    )