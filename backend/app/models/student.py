from __future__ import annotations
from datetime import date
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.base import Base

class Student(Base):
    __tablename__='student'
    student_id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    date_of_birth: Mapped[date]
    nationality: Mapped[str]
    state: Mapped[str]
    gender: Mapped[str]
    educations:Mapped[list['Education']]=relationship(
        back_populates='student'
    )
    eligibility_records: Mapped[list["StudentExamEligibility"]] = relationship(
    back_populates="student"
    )
    notifications: Mapped[list["Notification"]] = relationship(
    back_populates="student"
    )

    tracked_exams: Mapped[list["TrackedExam"]] = relationship(
        back_populates="student"
    )