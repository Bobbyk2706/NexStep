from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_admin
from app.services.ai_exam_discovery_service import (
    DiscoveryPersistenceError,
    ExamDiscoveryError,
    NoNotificationFoundError,
    discover_exam,
)


router = APIRouter(
    prefix="/admin/extractions",
    tags=["admin-discovery"],
)


class CreateExamExtractionRequest(BaseModel):
    exam_name: str = Field(
        min_length=1,
        max_length=200,
    )


class CreateExamExtractionResponse(BaseModel):
    id: int
    extraction_id: int
    notification_id: int
    exam_id: int
    exam_name: str
    official_url: str
    pdf_path: str
    status: str
    approval_status: str


@router.post(
    "",
    response_model=CreateExamExtractionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exam_extraction(
    payload: CreateExamExtractionRequest,
    admin=Depends(get_current_admin),
):
    """
    Start the complete AI exam-discovery pipeline.

    The pipeline ends with a PENDING extraction.
    No information is automatically approved.
    """

    try:
        return discover_exam(payload.exam_name)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Subclasses of ExamDiscoveryError must be caught BEFORE it.
    except NoNotificationFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NO_NOTIFICATION_FOUND",
                "message": str(exc),
                "official_url": exc.official_url,
                "pages_checked": exc.pages_checked,
            },
        ) from exc

    except DiscoveryPersistenceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "PERSISTENCE_FAILED",
                "message": str(exc),
            },
        ) from exc

    except ExamDiscoveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exam discovery failed unexpectedly.",
        ) from exc