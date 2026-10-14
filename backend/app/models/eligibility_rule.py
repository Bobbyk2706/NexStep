from __future__ import annotations

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EligibilityRule(Base):
    __tablename__ = "eligibilityrule"

    rule_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey("eligibilityrulegroup.group_id")
    )

    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("eligibilityattribute.attribute_id")
    )

    operator: Mapped[str]

    value: Mapped[str] = mapped_column(
        Text
    )

    group: Mapped["EligibilityRuleGroup"] = relationship(
        back_populates="rules"
    )

    attribute: Mapped["EligibilityAttribute"] = relationship(
        back_populates="rules"
    )