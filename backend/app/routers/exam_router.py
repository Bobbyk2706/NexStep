from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.exam import (
    ExamDetailOut,
    ExamListOut,
)
from app.services.exam_service import (
    get_all_exams,
    get_exam_by_id,
    search_exams,
)
from app.services.official_notification_service import (
    get_latest_approved_notification,
)


router = APIRouter(
    prefix="/exams",
    tags=["exams"],
)


def _exam_to_list_response(exam) -> dict:
    """
    Converts an Exam SQLAlchemy object into the structure
    expected by ExamListOut.
    """
    return {
        "exam_id": exam.exam_id,
        "name": exam.name,
        "type": exam.type,
        "description": exam.description,
        "off_exam_page": exam.off_exam_page,
        "status": exam.status,
        "conducting_body": exam.body,
    }


@router.get(
    "",
    response_model=list[ExamListOut],
)
def list_exams():
    """
    Returns all exams available in the database.
    """
    exams = get_all_exams()

    return [
        _exam_to_list_response(exam)
        for exam in exams
    ]


@router.get(
    "/search",
    response_model=list[ExamListOut],
)
def search_exam_list(
    q: str = Query(
        ...,
        min_length=1,
        description="Search by exam name or description",
    ),
):
    """
    Searches exams by name or description.
    """
    exams = search_exams(q)

    return [
        _exam_to_list_response(exam)
        for exam in exams
    ]


@router.get(
    "/{exam_id}",
    response_model=ExamDetailOut,
)
def get_exam(exam_id: int):
    """
    Returns detailed information about one exam, including
    its latest approved official notification.
    """
    exam = get_exam_by_id(exam_id)

    if exam is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found",
        )

    notification = get_latest_approved_notification(exam_id)

    return {
        "exam_id": exam.exam_id,
        "name": exam.name,
        "type": exam.type,
        "description": exam.description,
        "off_exam_page": exam.off_exam_page,
        "status": exam.status,
        "conducting_body": exam.body,
        "latest_approved_notification": notification,
    }