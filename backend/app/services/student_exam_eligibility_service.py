from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.session import SessionLocal
from app.models.student import Student
from app.models.exam import Exam
from app.models.studentexameligibility import (
    StudentExamEligibility,
)
from app.services.eligibility_service import (
    evaluate_eligibility,
)


def create_eligibility(
    student_id: int,
    exam_id: int,
):
    """
    Evaluate a student against the latest approved exam rules
    and store a new eligibility evaluation.

    Previous evaluations are preserved as history.
    """

    with SessionLocal() as session:

        student = session.scalar(
            select(Student)
            .options(
                selectinload(
                    Student.educations
                ),
                selectinload(
                    Student.work_experiences
                ),
            )
            .where(
                Student.student_id
                == student_id
            )
        )

        if student is None:
            raise ValueError(
                "Student not found."
            )

        exam = session.scalar(
            select(Exam).where(
                Exam.exam_id == exam_id
            )
        )

        if exam is None:
            raise ValueError(
                "Exam not found."
            )

        evaluation = evaluate_eligibility(
            student=student,
            exam_id=exam_id,
            db=session,
        )

        reason = "\n".join(
            evaluation.reasons
        )

        result = StudentExamEligibility(
            student_id=student_id,
            exam_id=exam_id,
            eligibility_status=(
                "ELIGIBLE"
                if evaluation.eligible
                else "NOT_ELIGIBLE"
            ),
            reason=reason,
            evaluated_at=datetime.now(),
        )

        session.add(result)

        session.commit()

        session.refresh(result)

        return result.eligibility_id


def get_eligibility(
    student_id: int,
    exam_id: int,
):
    """
    Return the latest eligibility evaluation for a
    student/exam pair.

    Historical evaluations remain stored in the database.
    """

    with SessionLocal() as session:

        result = session.scalar(
            select(StudentExamEligibility)
            .where(
                StudentExamEligibility.student_id
                == student_id,
                StudentExamEligibility.exam_id
                == exam_id,
            )
            .order_by(
                StudentExamEligibility.evaluated_at.desc(),
                StudentExamEligibility.eligibility_id.desc(),
            )
        )

        return result