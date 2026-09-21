from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.session import SessionLocal
from app.models.student import Student
from app.models.tracked_exam import TrackedExam
from app.models.studentexameligibility import (
    StudentExamEligibility,
)
from app.services.eligibility_service import (
    evaluate_eligibility,
)


class EligibilityReEvaluationError(RuntimeError):
    """
    Raised when monitoring-triggered eligibility re-evaluation
    cannot be completed safely.
    """


@dataclass(frozen=True)
class StudentEligibilityChange:
    """
    Result of re-evaluating one tracked student.
    """

    student_id: int
    exam_id: int
    old_status: str | None
    new_status: str
    status_changed: bool
    reason: str


@dataclass(frozen=True)
class EligibilityReEvaluationResult:
    """
    Result of re-evaluating all tracked students for an exam.
    """

    exam_id: int
    students_evaluated: int
    status_changes: int
    results: list[StudentEligibilityChange]


def _get_tracked_students(
    *,
    exam_id: int,
    db: Session,
) -> list[Student]:
    """
    Load all students currently tracking the exam.

    Student education and work-experience records are eagerly
    loaded because the existing eligibility engine requires them.
    """

    tracked_students = db.scalars(
        select(Student)
        .join(
            TrackedExam,
            TrackedExam.student_id == Student.student_id,
        )
        .where(
            TrackedExam.exam_id == exam_id,
            TrackedExam.tracking_status == "ACTIVE",
        )
        .options(
            selectinload(Student.educations),
            selectinload(Student.work_experiences),
        )
        .order_by(Student.student_id)
    ).unique().all()

    return list(tracked_students)


def _get_latest_eligibility(
    *,
    student_id: int,
    exam_id: int,
    db: Session,
) -> StudentExamEligibility | None:
    """
    Return the latest stored eligibility evaluation for a
    student/exam pair.

    Historical evaluations remain untouched.
    """

    return db.scalar(
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


def _create_eligibility_record(
    *,
    student_id: int,
    exam_id: int,
    eligible: bool,
    reason: str,
    db: Session,
) -> StudentExamEligibility:
    """
    Store a new eligibility evaluation.

    Existing evaluations are deliberately preserved.
    """

    record = StudentExamEligibility(
        student_id=student_id,
        exam_id=exam_id,
        eligibility_status=(
            "ELIGIBLE"
            if eligible
            else "NOT_ELIGIBLE"
        ),
        reason=reason,
        evaluated_at=datetime.now(),
    )

    db.add(record)
    db.flush()

    return record


def _re_evaluate_student(
    *,
    student: Student,
    exam_id: int,
    db: Session,
) -> StudentEligibilityChange:
    """
    Re-evaluate one student against the latest approved
    eligibility rules for the exam.
    """

    old_record = _get_latest_eligibility(
        student_id=student.student_id,
        exam_id=exam_id,
        db=db,
    )

    try:
        evaluation = evaluate_eligibility(
            student=student,
            exam_id=exam_id,
            db=db,
        )
    except Exception as error:
        raise EligibilityReEvaluationError(
            "Eligibility evaluation failed for student "
            f"{student.student_id} and exam {exam_id}."
        ) from error

    reason = "\n".join(evaluation.reasons)

    new_record = _create_eligibility_record(
        student_id=student.student_id,
        exam_id=exam_id,
        eligible=evaluation.eligible,
        reason=reason,
        db=db,
    )

    new_status = new_record.eligibility_status

    if old_record is None:
        return StudentEligibilityChange(
            student_id=student.student_id,
            exam_id=exam_id,
            old_status=None,
            new_status=new_status,
            status_changed=False,
            reason=reason,
        )

    status_changed = (
        old_record.eligibility_status
        != new_status
    )

    return StudentEligibilityChange(
        student_id=student.student_id,
        exam_id=exam_id,
        old_status=old_record.eligibility_status,
        new_status=new_status,
        status_changed=status_changed,
        reason=reason,
    )


def re_evaluate_exam_eligibility(
    *,
    exam_id: int,
    requires_eligibility_re_evaluation: bool,
    db: Session | None = None,
) -> EligibilityReEvaluationResult:
    """
    Re-evaluate eligibility for all active students tracking
    the specified exam.

    The caller supplies the deterministic Phase 5 decision
    indicating whether eligibility actually needs to be
    re-evaluated.

    If re-evaluation is not required, no students are touched.

    Existing eligibility records are preserved as history.
    A new evaluation record is created for every affected
    tracked student.

    A student without a previous eligibility record receives
    their first evaluation. This is not considered a status
    change because there is no previous status to compare.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        if not requires_eligibility_re_evaluation:
            return EligibilityReEvaluationResult(
                exam_id=exam_id,
                students_evaluated=0,
                status_changes=0,
                results=[],
            )

        students = _get_tracked_students(
            exam_id=exam_id,
            db=db,
        )

        results: list[StudentEligibilityChange] = []

        for student in students:
            result = _re_evaluate_student(
                student=student,
                exam_id=exam_id,
                db=db,
            )

            results.append(result)

        status_changes = sum(
            1
            for result in results
            if result.status_changed
        )

        if owns_session:
            db.commit()

        return EligibilityReEvaluationResult(
            exam_id=exam_id,
            students_evaluated=len(results),
            status_changes=status_changes,
            results=results,
        )

    except EligibilityReEvaluationError:
        if owns_session:
            db.rollback()

        raise

    except Exception as error:
        raise EligibilityReEvaluationError(
            f"Eligibility evaluation failed for student "
            f"{student.student_id} and exam {exam_id}: {error}"
        ) from error