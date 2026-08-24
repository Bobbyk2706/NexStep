from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EligibilityRuleGroup(Base):
    __tablename__ = "eligibilityrulegroup"

    group_id: Mapped[int] = mapped_column(primary_key=True)

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("officialnotification.notification_id")
    )

    group_number: Mapped[int]
    logical_operator: Mapped[str]

    rules: Mapped[list["EligibilityRule"]] = relationship(
        back_populates="group"
    )
    notification: Mapped["OfficialNotification"] = relationship(
    back_populates="rule_groups"
    )