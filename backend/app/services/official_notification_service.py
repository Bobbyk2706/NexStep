import app.models 
from app.database.session import SessionLocal
from sqlalchemy import select
from app.models.exam import Exam
from app.models.official_notification import OfficialNotification
def off_not(
        exam_id,
        title,
        notification_type,
        release_date,
        application_start_date,
        application_end_date,
        exam_date,
        official_url,
        pdf_path,
        ai_summary,
        ai_change_summary,
        approval_status,
        rejection_reason
    ):
    with SessionLocal() as s:
        exam=s.scalar(select(Exam).where(Exam.exam_id==exam_id))
        official_notification=OfficialNotification(
            title=title,
            notification_type=notification_type,
            release_date=release_date,
            application_start_date=application_start_date,
            application_end_date=application_end_date,
            exam_date=exam_date,
            official_url=official_url,
            pdf_path=pdf_path,
            ai_summary=ai_summary,
            ai_change_summary=ai_change_summary,
            approval_status=approval_status,
            rejection_reason=rejection_reason
        )
        exam.official_notifications.append(official_notification)
        s.add(official_notification)
        s.commit()
        return official_notification.notification_id