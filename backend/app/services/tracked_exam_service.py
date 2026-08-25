from datetime import datetime

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.student import Student
from app.models.exam import Exam
from app.models.tracked_exam import TrackedExam


def track_exam(
    student_id,
    exam_id
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

        tracked_exam = TrackedExam(
            tracked_at=datetime.now(),
            tracking_status="ACTIVE"
        )

        student.tracked_exams.append(tracked_exam)
        exam.tracked_exams.append(tracked_exam)

        s.add(tracked_exam)
        s.commit()

        return tracked_exam.tracking_id
def get_tracked_exams(student_id):

    with SessionLocal() as s:

        student = s.scalar(
            select(Student).where(
                Student.student_id == student_id
            )
        )

        if student is None:
            raise ValueError("Student not found")

        return student.tracked_exams
def untrack_exam(tracking_id):

    with SessionLocal() as s:

        tracked_exam = s.scalar(
            select(TrackedExam).where(
                TrackedExam.tracking_id == tracking_id
            )
        )

        if tracked_exam is None:
            raise ValueError("Tracked exam not found")

        tracked_exam.tracking_status = "INACTIVE"

        s.commit()