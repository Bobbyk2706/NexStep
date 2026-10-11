import logging
import threading
import time
from collections import defaultdict, deque

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.session import get_db
from app.models.student import Student
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.chatbot_service import answer_question

logger = logging.getLogger("app.assistant")

router = APIRouter(prefix="/assistant", tags=["assistant"])


# Simple per-student limit so one account cannot use up the AI quota.
# It lives in this process's memory, which is enough for one instance.
_WINDOW_SECONDS = 600
_MAX_REQUESTS = 20
_recent: dict[int, deque] = defaultdict(deque)
_lock = threading.Lock()


def _check_rate_limit(student_id: int) -> None:
    now = time.monotonic()

    with _lock:
        recent = _recent[student_id]

        while recent and now - recent[0] > _WINDOW_SECONDS:
            recent.popleft()

        if len(recent) >= _MAX_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You have asked a lot of questions. Please wait a few minutes and try again.",
            )

        recent.append(now)


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """
    Answer a logged-in student's question about exams, eligibility,
    deadlines, or how NexStep works.

    Exam facts come from NexStep's own database (see
    app.services.chatbot_service), not from the model's memory.
    """

    _check_rate_limit(current_student.student_id)

    try:
        result = answer_question(
            db=db,
            message=payload.message,
            student=current_student,
            history=[turn.model_dump() for turn in payload.history],
        )
    except Exception as error:
        logger.exception("Assistant failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The assistant could not produce an answer. Please try again.",
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
        unavailable=result.unavailable,
    )