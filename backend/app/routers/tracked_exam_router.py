from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_student
from app.models.student import Student
from app.schemas.tracked_exam import TrackedExamOut
from app.services.tracked_exam_service import (
    get_tracked_exams,
    track_exam,
    untrack_exam,
)


router = APIRouter(
    prefix="/tracked-exams",
    tags=["tracked-exams"],
)


@router.post(
    "/{exam_id}",
    response_model=TrackedExamOut,
    status_code=status.HTTP_201_CREATED,
)
def track_my_exam(
    exam_id: int,
    current_student: Student = Depends(
        get_current_student
    ),
):
    try:
        tracking_id = track_exam(
            student_id=current_student.student_id,
            exam_id=exam_id,
        )

    except ValueError as exc:
        message = str(exc)

        if message in {
            "Student not found",
            "Exam not found",
        }:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        if message == "Exam is already tracked":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message,
        )

    tracked_exams = get_tracked_exams(
        current_student.student_id
    )

    tracked_exam = next(
        (
            record
            for record in tracked_exams
            if record.tracking_id == tracking_id
        ),
        None,
    )

    if tracked_exam is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "Tracked exam was created but "
                "could not be retrieved."
            ),
        )

    return tracked_exam


@router.get(
    "",
    response_model=list[TrackedExamOut],
)
def get_my_tracked_exams(
    current_student: Student = Depends(
        get_current_student
    ),
):
    try:
        return get_tracked_exams(
            current_student.student_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete(
    "/{tracking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def untrack_my_exam(
    tracking_id: int,
    current_student: Student = Depends(
        get_current_student
    ),
):
    try:
        untrack_exam(
            student_id=current_student.student_id,
            tracking_id=tracking_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return None