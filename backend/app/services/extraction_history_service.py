from __future__ import annotations

from datetime import datetime


from sqlalchemy import select
from sqlalchemy.orm import Session

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
    extraction_status,
    db: Session | None = None,
):
    """
    Create an ExtractionHistory record.

    If an existing database session is supplied through `db`,
    this function participates in that transaction and does
    not commit it.

    If no session is supplied, this function creates and commits
    its own transaction for backward compatibility.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        notification = db.scalar(
            select(OfficialNotification).where(
                OfficialNotification.notification_id
                == notification_id
            )
        )

        if notification is None:
            raise ValueError(
                "Official notification not found."
            )

        extraction = ExtractionHistory(
            extraction_type=extraction_type,
            source_pdf_path=source_pdf_path,
            extracted_content=extracted_content,
            ai_summary=ai_summary,
            change_detected=change_detected,
            change_details=change_details,
            extraction_status=extraction_status,
            created_at=datetime.now(),
        )

        notification.extraction_history.append(
            extraction
        )

        db.add(extraction)

        # Generate extraction_id before the transaction
        # is committed.
        db.flush()

        extraction_id = extraction.extraction_id

        if owns_session:
            db.commit()

        return extraction_id

    except Exception:
        if owns_session:
            db.rollback()
        raise

    finally:
        if owns_session:
            db.close()