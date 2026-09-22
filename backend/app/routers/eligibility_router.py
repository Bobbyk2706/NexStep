from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_student, get_current_admin
from app.models.student import Student
from app.models.admin import Admin
from app.services.student_exam_eligibility_service import (
    create_eligibility,
    get_eligibility,
)
from app.schemas.eligibility import EligibilityOut

router = APIRouter(prefix="/eligibility", tags=["eligibility"])


def _to_out(record) -> EligibilityOut:
    return EligibilityOut.model_validate(record)


def _raise_for_value_error(exc: ValueError):
    """Existing services raise plain ValueError for everything — map the
    message to a sensible HTTP status rather than always returning 500."""
    message = str(exc)
    not_found_markers = ("not found", "No official notifications found")
    if any(marker in message for marker in not_found_markers):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    # Anything else (unsupported attribute, missing current education, etc.)
    # means the rule config or the student's profile can't be evaluated as-is.
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)


# ------------------------------------------------------------- student ---

@router.post(
    "/{exam_id}/evaluate",
    response_model=EligibilityOut,
    status_code=status.HTTP_201_CREATED,
)
def evaluate_my_eligibility(
    exam_id: int,
    current_student: Student = Depends(get_current_student),
):
    """Evaluates and stores a fresh eligibility result for the current
    student against the given exam's latest official notification."""
    try:
        create_eligibility(current_student.student_id, exam_id)
    except ValueError as exc:
        _raise_for_value_error(exc)

    record = get_eligibility(current_student.student_id, exam_id)
    return _to_out(record)


@router.get("/{exam_id}", response_model=EligibilityOut)
def get_my_eligibility(
    exam_id: int,
    current_student: Student = Depends(get_current_student),
):
    """Returns the most recently stored eligibility result — does not
    evaluate on the fly. Call POST /eligibility/{exam_id}/evaluate first
    if no result exists yet, or to refresh a stale one."""
    record = get_eligibility(current_student.student_id, exam_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No eligibility record yet — "
            "POST /eligibility/{exam_id}/evaluate first",
        )
    return _to_out(record)


# --------------------------------------------------------------- admin ---

@router.post(
    "/admin/{student_id}/{exam_id}/evaluate",
    response_model=EligibilityOut,
    status_code=status.HTTP_201_CREATED,
)
def evaluate_student_eligibility(
    student_id: int,
    exam_id: int,
    current_admin: Admin = Depends(get_current_admin),
):
    try:
        create_eligibility(student_id, exam_id)
    except ValueError as exc:
        _raise_for_value_error(exc)

    record = get_eligibility(student_id, exam_id)
    return _to_out(record)


@router.get("/admin/{student_id}/{exam_id}", response_model=EligibilityOut)
def get_student_eligibility(
    student_id: int,
    exam_id: int,
    current_admin: Admin = Depends(get_current_admin),
):
    record = get_eligibility(student_id, exam_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No eligibility record found",
        )
    return _to_out(record)