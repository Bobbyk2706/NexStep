from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.session import SessionLocal
from app.models.exam import Exam
from app.models.student import Student
from app.models.tracked_exam import TrackedExam


def track_exam(
    student_id: int,
    exam_id: int,
):
    with SessionLocal() as s:

        student = s.scalar(
            select(Student).where(
                Student.student_id == student_id
            )
        )

        if student is None:
            raise ValueError("Student not found")

        exam = s.scalar(
            select(Exam).where(
                Exam.exam_id == exam_id
            )
        )

        if exam is None:
            raise ValueError("Exam not found")

        existing = s.scalar(
            select(TrackedExam).where(
                TrackedExam.student_id == student_id,
                TrackedExam.exam_id == exam_id,
                TrackedExam.tracking_status == "ACTIVE",
            )
        )

        if existing is not None:
            raise ValueError("Exam is already tracked")

        tracked_exam = TrackedExam(
            student_id=student_id,
            exam_id=exam_id,
            tracked_at=datetime.now(),
            tracking_status="ACTIVE",
        )

        s.add(tracked_exam)
        s.commit()
        s.refresh(tracked_exam)

        return tracked_exam.tracking_id


def get_tracked_exams(
    student_id: int,
):
    with SessionLocal() as s:

        student = s.scalar(
            select(Student).where(
                Student.student_id == student_id
            )
        )

        if student is None:
            raise ValueError("Student not found")

        statement = (
            select(TrackedExam)
            .options(
                selectinload(TrackedExam.exam),
            )
            .where(
                TrackedExam.student_id == student_id,
                TrackedExam.tracking_status == "ACTIVE",
            )
            .order_by(
                TrackedExam.tracked_at.desc()
            )
        )

        return list(
            s.scalars(statement).all()
        )


def untrack_exam(
    student_id: int,
    tracking_id: int,
):
    with SessionLocal() as s:

        tracked_exam = s.scalar(
            select(TrackedExam).where(
                TrackedExam.tracking_id == tracking_id,
                TrackedExam.student_id == student_id,
            )
        )

        if tracked_exam is None:
            raise ValueError(
                "Tracked exam not found"
            )

        if tracked_exam.tracking_status != "ACTIVE":
            raise ValueError(
                "Exam is not currently tracked"
            )

        tracked_exam.tracking_status = "INACTIVE"

        s.commit()