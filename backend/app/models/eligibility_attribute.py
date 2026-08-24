from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EligibilityAttribute(Base):
    __tablename__ = "eligibilityattribute"

    attribute_id: Mapped[int] = mapped_column(primary_key=True)

    attribute_name: Mapped[str]
    source_table: Mapped[str]
    source_column: Mapped[str]
    data_type: Mapped[str]
    description: Mapped[str]
    rules: Mapped[list['EligibilityRule']]=relationship(
        back_populates='attribute'
    )