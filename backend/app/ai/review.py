from datetime import datetime
from app.ai.llm_client import extract_exam_information
from app.ai.validation import validate_exam_information
from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.extraction_history import ExtractionHistory


def create_pending_extraction(
    notification_id,
    source_pdf_path,
    extracted_content,
    ai_summary
):
    db = SessionLocal()

    extraction = ExtractionHistory(
        notification_id=notification_id,
        extraction_type="EXAM_INFORMATION",
        source_pdf_path=source_pdf_path,
        extracted_content=extracted_content,
        ai_summary=ai_summary,
        change_detected=False,
        change_details=None,
        extraction_status="PENDING",
        created_at=datetime.now()
    )

    db.add(extraction)
    db.commit()
    db.refresh(extraction)

    db.close()

    return extraction


def approve_extraction(extraction_id):
    db = SessionLocal()

    extraction = db.get(ExtractionHistory, extraction_id)

    if extraction is None:
        db.close()
        raise ValueError("Extraction not found.")

    extraction.extraction_status = "APPROVED"

    notification = db.get(
        OfficialNotification,
        extraction.notification_id
    )

    if notification is None:
        db.close()
        raise ValueError("Official notification not found.")

    notification.approval_status = "APPROVED"

    db.commit()
    db.refresh(extraction)

    db.close()

    return extraction


def reject_extraction(extraction_id, feedback):
    db = SessionLocal()

    extraction = db.get(ExtractionHistory, extraction_id)

    if extraction is None:
        db.close()
        raise ValueError("Extraction not found.")

    extraction.extraction_status = "REJECTED"
    extraction.change_details = feedback

    notification = db.get(
        OfficialNotification,
        extraction.notification_id
    )

    if notification is None:
        db.close()
        raise ValueError("Official notification not found.")

    notification.approval_status = "REJECTED"
    notification.rejection_reason = feedback

    db.commit()
    db.refresh(extraction)

    db.close()

    return extraction
def retry_extraction(extraction_id):
    db=SessionLocal()
    extraction=db.get(ExtractionHistory,extraction_id)
    if extraction is None:
        db.close()
        raise ValueError("Extraction is not found")
    if extraction.extraction_status!="REJECTED":
        db.close()
        raise ValueError