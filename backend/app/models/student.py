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
    # These four used to be required at signup. The frontend's actual
    # signup only collects name/email/password; DOB/nationality/state
    # are filled in later via PUT /student/profile, and gender isn't
    # collected by the profile form at all yet (see
    # database/migrations/0002_profile_schema.sql). Nullable here so
    # gender-based eligibility rules simply won't fire until/unless the
    # frontend adds that field.
    date_of_birth: Mapped[date | None]
    nationality: Mapped[str | None]
    state: Mapped[str | None]
    gender: Mapped[str | None]


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
    work_experiences: Mapped[list["WorkExperience"]] = relationship(
        back_populates="student"
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