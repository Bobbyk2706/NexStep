from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.session import get_db
from app.models.student import Student
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.chatbot_service import answer_question

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Answer a logged-in student's question about exam eligibility,
    deadlines, or notifications.

    The answer is grounded in NexStep's own exam/eligibility data
    (see app.services.chatbot_service) rather than the model's own
    training-data knowledge of specific exams, so it stays correct
    even as NexStep's own notification data changes.
    """

    try:
        result = answer_question(
            db=db,
            message=payload.message,
            student=current_student,
            history=[turn.model_dump() for turn in payload.history],
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Assistant could not produce an answer: {error}",
        ) from error

    return ChatResponse(
        answer=result.answer,
        sources=[
            {
                "exam_id": s.exam_id,
                "exam_name": s.exam_name,
                "notification_title": s.notification_title,
                "official_url": s.official_url,
            }
            for s in result.sources
        ],
        grounded=result.grounded,
    )
