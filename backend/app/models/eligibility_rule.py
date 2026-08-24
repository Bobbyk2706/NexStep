from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
class EligibilityRule(Base):
    __tablename__ = "eligibilityrule"
    rule_id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("eligibilityrulegroup.group_id")
    )
    attribute_id: Mapped[int] = mapped_column(
        ForeignKey("eligibilityattribute.attribute_id")
    )
    operator: Mapped[str]
    value: Mapped[str]
    group: Mapped["EligibilityRuleGroup"] = relationship(
        back_populates="rules"
    )
    attribute: Mapped["EligibilityAttribute"] = relationship(
        back_populates="rules"
    )