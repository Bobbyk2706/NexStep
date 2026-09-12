import app.models

from app.database.session import SessionLocal

from sqlalchemy import select

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
    pdf_path,
    ai_summary,
    ai_change_summary,
    approval_status,
    rejection_reason
):
    with SessionLocal() as s:

        exam = s.scalar(
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
            pdf_path=pdf_path,
            ai_summary=ai_summary,
            ai_change_summary=ai_change_summary,
            approval_status=approval_status,
            rejection_reason=rejection_reason
        )

        for exam_date in exam_dates:
            date_record = ExamDate(
                start_date=exam_date["start_date"],
                end_date=exam_date["end_date"]
            )

            official_notification.exam_dates.append(
                date_record
            )

        exam.official_notifications.append(
            official_notification
        )

        s.add(official_notification)
        s.commit()

        s.refresh(official_notification)

        return official_notification.notification_id