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


    # Added for auth integration (see database/migrations/0001_add_auth_columns.sql).
    # NULL/'' account_status is treated as active; only an explicit
    # 'suspended'/'inactive'/'disabled' blocks login.
    account_status: Mapped[str | None] = mapped_column(default="active")
    # Bumped on every refresh-token issuance/rotation and on logout, so a
    # refresh token's embedded "trv" claim can be checked against it to
    # revoke old sessions.
    token_version: Mapped[str | None]






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