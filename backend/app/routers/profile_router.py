from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.dependencies import get_current_student
from app.models.student import Student
from app.models.education import Education
from app.models.work_experience import WorkExperience
from app.schemas.profile import (
    ProfileIn,
    ProfileOut,
    QualificationEntry,
    WorkExperienceEntry,
)

router = APIRouter(prefix="/student", tags=["profile"])

_YEAR_LABEL_TO_INT = {
    "1st Year": 1,
    "2nd Year": 2,
    "3rd Year": 3,
    "4th Year": 4,
}


def _parse_int(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _parse_score(value: str | None) -> tuple[float | None, float | None]:
    """Returns (cgpa, percentage) — the frontend's per-qualification
    'score' field is a single free-text box covering either."""
    if not value:
        return None, None
    cleaned = value.strip()
    if "%" in cleaned:
        try:
            return None, float(cleaned.replace("%", "").strip())
        except ValueError:
            return None, None
    try:
        return float(cleaned), None
    except ValueError:
        return None, None


def _fmt_num(value: float) -> str:
    """Drop a trailing .0 so a score like 92% doesn't come back as 92.0%."""
    return str(int(value)) if value == int(value) else str(value)


def _entry_to_out(edu: Education) -> QualificationEntry:
    if edu.percentage is not None:
        score_str = f"{_fmt_num(edu.percentage)}%"
    elif edu.cgpa is not None:
        score_str = _fmt_num(edu.cgpa)
    else:
        score_str = None
    return QualificationEntry(
        level=edu.qualification,
        institution=edu.institution,
        field=edu.specialization,
        yearCompleted=str(edu.year_of_passing) if edu.year_of_passing else None,
        score=score_str,
    )


def student_has_profile(db: Session, student_id: int) -> bool:
    return (
        db.query(Education)
        .filter(Education.student_id == student_id)
        .first()
        is not None
    )


@router.get("/profile", response_model=ProfileOut | None)
def get_profile(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    current = (
        db.query(Education)
        .filter(Education.student_id == current_student.student_id, Education.is_current.is_(True))
        .first()
    )
    if current is None:
        # No profile saved yet — matches the mock's `return null`.
        return None

    past_quals = (
        db.query(Education)
        .filter(
            Education.student_id == current_student.student_id,
            Education.is_current.isnot(True),
            Education.is_higher_qualification.isnot(True),
        )
        .all()
    )
    higher_qual = (
        db.query(Education)
        .filter(
            Education.student_id == current_student.student_id,
            Education.is_higher_qualification.is_(True),
        )
        .first()
    )
    work_rows = (
        db.query(WorkExperience)
        .filter(WorkExperience.student_id == current_student.student_id)
        .all()
    )

    return ProfileOut(
        name=current_student.name,
        dob=current_student.date_of_birth.isoformat() if current_student.date_of_birth else None,
        nationality=current_student.nationality,
        state=current_student.state,
        college=current.institution,
        branch=current.specialization,
        yearOfStudy=current.year_of_study_label,
        cgpa=_fmt_num(current.cgpa) if current.cgpa is not None else None,
        percentage=_fmt_num(current.percentage) if current.percentage is not None else None,
        qualifications=[_entry_to_out(e) for e in past_quals],
        workExperience=[
            WorkExperienceEntry(company=w.company, role=w.role, duration=w.duration)
            for w in work_rows
        ],
        hasHigherQualification=higher_qual is not None,
        previousQualification=_entry_to_out(higher_qual) if higher_qual else None,
    )


@router.put("/profile", response_model=ProfileOut)
def save_profile(
    payload: ProfileIn,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    # Full replace: delete everything previously stored for this student
    # and re-insert from the payload — avoids partial-update matching
    # logic for a form that's edited and resubmitted as a whole.
    db.query(Education).filter(Education.student_id == current_student.student_id).delete()
    db.query(WorkExperience).filter(WorkExperience.student_id == current_student.student_id).delete()

    current_student.name = payload.name
    try:
        current_student.date_of_birth = date.fromisoformat(payload.dob)
    except ValueError:
        current_student.date_of_birth = None
    current_student.nationality = payload.nationality
    current_student.state = payload.state

    cgpa = float(payload.cgpa) if payload.cgpa else None
    percentage = float(payload.percentage) if payload.percentage else None

    db.add(Education(
        student_id=current_student.student_id,
        qualification="Bachelor's",
        specialization=payload.branch,
        institution=payload.college,
        year_of_study_label=payload.yearOfStudy,
        current_year=_YEAR_LABEL_TO_INT.get(payload.yearOfStudy),
        cgpa=cgpa,
        percentage=percentage,
        is_current=True,
    ))

    for q in payload.qualifications:
        cgpa_q, pct_q = _parse_score(q.score)
        db.add(Education(
            student_id=current_student.student_id,
            qualification=q.level,
            specialization=q.field,
            institution=q.institution,
            year_of_passing=_parse_int(q.yearCompleted),
            cgpa=cgpa_q,
            percentage=pct_q,
            is_current=False,
        ))

    if payload.hasHigherQualification and payload.previousQualification:
        pq = payload.previousQualification
        cgpa_p, pct_p = _parse_score(pq.score)
        db.add(Education(
            student_id=current_student.student_id,
            qualification=pq.level,
            specialization=pq.field,
            institution=pq.institution,
            year_of_passing=_parse_int(pq.yearCompleted),
            cgpa=cgpa_p,
            percentage=pct_p,
            is_current=False,
            is_higher_qualification=True,
        ))

    for w in payload.workExperience:
        db.add(WorkExperience(
            student_id=current_student.student_id,
            company=w.company,
            role=w.role,
            duration=w.duration,
        ))

    db.commit()
    return get_profile(current_student=current_student, db=db)