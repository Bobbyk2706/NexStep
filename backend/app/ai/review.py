from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.extraction_history import ExtractionHistory
import datetime
def create_pending_extractions(notification_id,source_pdf_path,extracted_content,ai_summary):
    db=SessionLocal()
    extraction = ExtractionHistory(
    notification_id=notification_id,
    extraction_type="EXAM_INFORMATION",
    source_pdf_path=source_pdf_path,
    extracted_content=extracted_content,
    ai_summary=ai_summary,
    change_detected=False,
    change_details=None,
    extraction_status="PENDING",
    created_at=datetime.datetime.now()
    )
    db.add(extraction)
    db.commit()
    return extraction
