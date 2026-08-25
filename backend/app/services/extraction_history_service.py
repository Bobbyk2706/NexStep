from datetime import datetime

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.extraction_history import ExtractionHistory


def create_extraction_history(
    notification_id,
    extraction_type,
    source_pdf_path,
    extracted_content,
    ai_summary,
    change_detected,
    change_details,
    extraction_status
):
    with SessionLocal() as s:

        notification = s.scalar(
            select(OfficialNotification).where(
                OfficialNotification.notification_id == notification_id
            )
        )

        if notification is None:
            raise ValueError("Official notification not found")

        extraction = ExtractionHistory(
            extraction_type=extraction_type,
            source_pdf_path=source_pdf_path,
            extracted_content=extracted_content,
            ai_summary=ai_summary,
            change_detected=change_detected,
            change_details=change_details,
            extraction_status=extraction_status,
            created_at=datetime.now()
        )

        notification.extraction_history.append(extraction)

        s.add(extraction)
        s.commit()

        return extraction.extraction_id