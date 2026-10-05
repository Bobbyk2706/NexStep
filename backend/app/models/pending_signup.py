from __future__ import annotations

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PendingSignup(Base):
    """
    A signup that is waiting for email verification.

    No Student row exists until the emailed code is confirmed. The
    password is stored only as a bcrypt hash and the code only as a
    salted hash.
    """

    __tablename__ = "pending_signup"

    pending_id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(320), index=True)
    name: Mapped[str] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(200))

    code_hash: Mapped[str] = mapped_column(String(200))
    expires_at: Mapped[datetime]

    attempts: Mapped[int] = mapped_column(default=0, server_default="0")
    send_count: Mapped[int] = mapped_column(default=1, server_default="1")

    last_sent_at: Mapped[datetime]
    created_at: Mapped[datetime]