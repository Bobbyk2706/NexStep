from datetime import datetime

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.student import Student
from app.models.exam import Exam
from app.models.studentexameligibility import StudentExamEligibility
from app.services.eligibility_service import check_eligibility


def create_eligibility(student_id, exam_id):

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

        eligible = check_eligibility(
            student,
            exam_id
        )

        result = StudentExamEligibility(
            eligibility_status="ELIGIBLE" if eligible else "NOT_ELIGIBLE",
            reason=None,
            evaluated_at=datetime.now()
        )

        student.eligibility_records.append(result)
        exam.eligibility_records.append(result)

        s.add(result)
        s.commit()

        return result.eligibility_id
def get_eligibility(student_id, exam_id):

    with SessionLocal() as s:

        result = s.scalar(
            select(StudentExamEligibility).where(
                StudentExamEligibility.student_id == student_id,
                StudentExamEligibility.exam_id == exam_id
            )
        )

        if result is None:
            return None

        return result    