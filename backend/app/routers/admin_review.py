from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.review import (
    approve_extraction,
    reject_extraction,
)
from app.database.session import SessionLocal
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification


router = APIRouter(
    prefix="/admin/extractions",
    tags=["Admin Review"]
)


class RejectionRequest(BaseModel):
    feedback: str


@router.get("/{extraction_id}")
def get_extraction_for_review(extraction_id: int):
    db = SessionLocal()

    extraction = db.get(ExtractionHistory, extraction_id)

    if extraction is None:
        db.close()
        return {"error": "Extraction not found."}

    notification = db.get(
        OfficialNotification,
        extraction.notification_id
    )

    if notification is None:
        db.close()
        return {"error": "Official notification not found."}

    result = {
        "extraction_id": extraction.extraction_id,
        "status": extraction.extraction_status,
        "original_document": notification.pdf_path,
        "official_url": notification.official_url,
        "extracted_content": extraction.extracted_content,
        "ai_summary": extraction.ai_summary,
        "change_detected": extraction.change_detected,
        "change_details": extraction.change_details
    }

    db.close()

    return result


@router.post("/{extraction_id}/approve")
def approve_extraction_review(extraction_id: int):
    extraction = approve_extraction(extraction_id)

    return {
        "message": "Extraction approved successfully.",
        "extraction_id": extraction.extraction_id,
        "status": extraction.extraction_status
    }


@router.post("/{extraction_id}/reject")
def reject_extraction_review(
    extraction_id: int,
    request: RejectionRequest
):
    extraction = reject_extraction(
        extraction_id,
        request.feedback
    )

    return {
        "message": "Extraction rejected successfully.",
        "extraction_id": extraction.extraction_id,
        "status": extraction.extraction_status,
        "feedback": request.feedback
    }