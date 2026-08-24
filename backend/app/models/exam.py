

from sqlalchemy.orm import Mapped, mapped_column,relationship

from sqlalchemy import ForeignKey
from app.models.base import Base


class Exam(Base):
    __tablename__ = "exam"

    exam_id: Mapped[int] = mapped_column(primary_key=True)

    body_id: Mapped[int]=mapped_column(ForeignKey('conducting_body.body_id'))

    name: Mapped[str]
    type: Mapped[str]
    description: Mapped[str | None]
    off_exam_page: Mapped[str | None]
    status: Mapped[str | None]
    body:Mapped['ConductingBody']=relationship(
        back_populates='exams'
    )
    eligibility_records: Mapped[list["StudentExamEligibility"]] = relationship(
    back_populates="exam"
    )
    official_notifications: Mapped[list["OfficialNotification"]] = relationship(
    back_populates="exam"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="exam"
    )

    tracked_exams: Mapped[list["TrackedExam"]] = relationship(
        back_populates="exam"
    )