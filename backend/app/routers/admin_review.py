from __future__ import annotations

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from pydantic import BaseModel

from app.ai.review import (
    approve_extraction,
    reject_extraction,
    retry_extraction,
)
from app.database.session import SessionLocal
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification


router = APIRouter(
    prefix="/admin/extractions",
    tags=["Admin Review"],
)


class RejectionRequest(BaseModel):
    feedback: str


@router.get("/{extraction_id}")
def get_extraction_for_review(
    extraction_id: int,
):
    db = SessionLocal()

    try:
        extraction = db.get(
            ExtractionHistory,
            extraction_id,
        )

        if extraction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Extraction not found.",
            )

        notification = db.get(
            OfficialNotification,
            extraction.notification_id,
        )

        if notification is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Official notification not found.",
            )

        return {
            "extraction_id": extraction.extraction_id,
            "status": extraction.extraction_status,
            "notification_id": extraction.notification_id,
            "original_document": notification.pdf_path,
            "official_url": notification.official_url,
            "extracted_content": extraction.extracted_content,
            "ai_summary": extraction.ai_summary,
            "change_detected": extraction.change_detected,
            "change_details": extraction.change_details,
            "created_at": extraction.created_at,
        }

    finally:
        db.close()


@router.post(
    "/{extraction_id}/approve",
    status_code=status.HTTP_200_OK,
)
def approve_extraction_review(
    extraction_id: int,
):
    """
    Approve an extraction through the HITL review workflow.

    The underlying approval service is responsible for:

    - pending-status validation
    - latest-extraction protection
    - deserialization
    - normalization
    - validation
    - exam-date persistence
    - recursive eligibility persistence
    - atomic transaction commit
    """

    try:
        extraction = approve_extraction(
            extraction_id,
        )

    except ValueError as error:
        message = str(error)

        if (
            "no longer the latest"
            in message.lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            ) from error

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve extraction.",
        ) from error

    return {
        "message": "Extraction approved successfully.",
        "extraction_id": extraction.extraction_id,
        "status": extraction.extraction_status,
    }


@router.post(
    "/{extraction_id}/reject",
    status_code=status.HTTP_200_OK,
)
def reject_extraction_review(
    extraction_id: int,
    request: RejectionRequest,
):
    """
    Reject an extraction with admin feedback.
    """

    feedback = request.feedback.strip()

    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejection feedback cannot be empty.",
        )

    try:
        extraction = reject_extraction(
            extraction_id,
            feedback,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject extraction.",
        ) from error

    return {
        "message": "Extraction rejected successfully.",
        "extraction_id": extraction.extraction_id,
        "status": extraction.extraction_status,
        "feedback": feedback,
    }


@router.post(
    "/{extraction_id}/retry",
    status_code=status.HTTP_200_OK,
)
def retry_extraction_review(
    extraction_id: int,
):
    """
    Retry extraction using the existing review workflow.
    """

    try:
        extraction = retry_extraction(
            extraction_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retry extraction.",
        ) from error

    return {
        "message": "Extraction retry completed.",
        "extraction_id": extraction.extraction_id,
        "status": extraction.extraction_status,
        "extraction_type": extraction.extraction_type,
    }