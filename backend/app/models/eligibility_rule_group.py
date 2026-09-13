from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.official_notification import OfficialNotification
    from app.models.eligibility_rule import EligibilityRule


class EligibilityRuleGroup(Base):
    __tablename__ = "eligibilityrulegroup"

    group_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    notification_id: Mapped[int] = mapped_column(
        ForeignKey("officialnotification.notification_id")
    )

    group_number: Mapped[int]

    logical_operator: Mapped[str]

    parent_group_id: Mapped[int | None] = mapped_column(
        ForeignKey("eligibilityrulegroup.group_id")
    )

    rules: Mapped[list["EligibilityRule"]] = relationship(
        back_populates="group"
    )

    notification: Mapped["OfficialNotification"] = relationship(
        back_populates="rule_groups"
    )

    parent_group: Mapped["EligibilityRuleGroup | None"] = relationship(
        remote_side="EligibilityRuleGroup.group_id",
        back_populates="child_groups"
    )

    child_groups: Mapped[list["EligibilityRuleGroup"]] = relationship(
        back_populates="parent_group"
    )