from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel

from app.ai.review import (
    approve_extraction,
    reject_extraction,
    retry_extraction,
)
from app.auth.dependencies import get_current_admin
from app.database.session import SessionLocal
from app.models.admin import Admin
from app.models.exam import Exam
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification


router = APIRouter(
    prefix="/admin/extractions",
    tags=["Admin Review"],
)


class RejectionRequest(BaseModel):
    feedback: str


# ---------------------------------------------------------------------------
# List extractions
# ---------------------------------------------------------------------------

@router.get("")
def list_extractions(
    status_filter: str | None = None,
    current_admin: Admin = Depends(get_current_admin),
):
    """
    Return extraction history for the admin dashboard/review list.

    Optional filtering:
        GET /admin/extractions?status_filter=PENDING
        GET /admin/extractions?status_filter=APPROVED
        GET /admin/extractions?status_filter=REJECTED
    """

    db = SessionLocal()

    try:
        query = (
            db.query(
                ExtractionHistory,
                OfficialNotification,
                Exam,
            )
            .join(
                OfficialNotification,
                ExtractionHistory.notification_id
                == OfficialNotification.notification_id,
            )
            .join(
                Exam,
                OfficialNotification.exam_id
                == Exam.exam_id,
            )
        )

        if status_filter:
            query = query.filter(
                ExtractionHistory.extraction_status
                == status_filter
            )

        rows = (
            query
            .order_by(
                ExtractionHistory.created_at.desc()
            )
            .all()
        )

        return [
            {
                "extraction_id": extraction.extraction_id,
                "notification_id": extraction.notification_id,
                "exam_id": exam.exam_id,
                "exam_name": exam.name,
                "notification_title": notification.title,
                "extraction_type": extraction.extraction_type,
                "status": extraction.extraction_status,
                "change_detected": extraction.change_detected,
                "change_details": extraction.change_details,
                "created_at": extraction.created_at,
            }
            for extraction, notification, exam in rows
        ]

    finally:
        db.close()


# ---------------------------------------------------------------------------
# Get extraction for review
# ---------------------------------------------------------------------------

@router.get("/{extraction_id}")
def get_extraction_for_review(
    extraction_id: int,
    current_admin: Admin = Depends(get_current_admin),
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


# ---------------------------------------------------------------------------
# Approve
# ---------------------------------------------------------------------------

@router.post(
    "/{extraction_id}/approve",
    status_code=status.HTTP_200_OK,
)
def approve_extraction_review(
    extraction_id: int,
    current_admin: Admin = Depends(get_current_admin),
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

        if "no longer the latest" in message.lower():
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


# ---------------------------------------------------------------------------
# Reject
# ---------------------------------------------------------------------------

@router.post(
    "/{extraction_id}/reject",
    status_code=status.HTTP_200_OK,
)
def reject_extraction_review(
    extraction_id: int,
    request: RejectionRequest,
    current_admin: Admin = Depends(get_current_admin),
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


# ---------------------------------------------------------------------------
# Retry
# ---------------------------------------------------------------------------

@router.post(
    "/{extraction_id}/retry",
    status_code=status.HTTP_200_OK,
)
def retry_extraction_review(
    extraction_id: int,
    current_admin: Admin = Depends(get_current_admin),
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