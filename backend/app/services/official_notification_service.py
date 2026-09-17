from __future__ import annotations

from datetime import date


from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.exam import Exam
from app.models.official_notification import OfficialNotification
from app.models.exam_date import ExamDate



def off_not(
    exam_id,
    title,
    notification_type,
    release_date,
    application_start_date,
    application_end_date,
    exam_dates,
    official_url,
    document_url,
    pdf_path,
    document_hash,
    ai_summary,
    ai_change_summary,
    approval_status,
    rejection_reason,
    db: Session | None = None,
):
    """
    Create an OfficialNotification and its ExamDate records.

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
        exam = db.scalar(
            select(Exam).where(
                Exam.exam_id == exam_id
            )
        )

        if exam is None:
            raise ValueError(
                "Exam not found."
            )

        official_notification = OfficialNotification(
            title=title,
            notification_type=notification_type,
            release_date=release_date,
            application_start_date=application_start_date,
            application_end_date=application_end_date,
            official_url=official_url,
            document_url=document_url,
            pdf_path=pdf_path,
            document_hash=document_hash,
            ai_summary=ai_summary,
            ai_change_summary=ai_change_summary,
            approval_status=approval_status,
            rejection_reason=rejection_reason,
        )

        for exam_date in exam_dates:
            date_record = ExamDate(
                start_date=exam_date["start_date"],
                end_date=exam_date["end_date"],
            )

            official_notification.exam_dates.append(
                date_record
            )

        exam.official_notifications.append(
            official_notification
        )

        db.add(official_notification)

        # Make notification_id available before the caller
        # creates the extraction history record.
        db.flush()

        notification_id = (
            official_notification.notification_id
        )

        if owns_session:
            db.commit()

        return notification_id

    except Exception:
        if owns_session:
            db.rollback()
        raise

    finally:
        if owns_session:
            db.close()