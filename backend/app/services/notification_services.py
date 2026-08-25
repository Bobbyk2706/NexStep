from datetime import datetime

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.student import Student
from app.models.exam import Exam
from app.models.notification import Notification


def create_notification(
    student_id,
    notification_type,
    title,
    message,
    exam_id=None
):
    with SessionLocal() as s:

        student = s.scalar(
            select(Student).where(
                Student.student_id == student_id
            )
        )

        if student is None:
            raise ValueError("Student not found")

        exam = None

        if exam_id is not None:
            exam = s.scalar(
                select(Exam).where(
                    Exam.exam_id == exam_id
                )
            )

            if exam is None:
                raise ValueError("Exam not found")

        notification = Notification(
            notification_type=notification_type,
            title=title,
            message=message,
            is_read=False,
            created_at=datetime.now(),
            read_at=None
        )

        student.notifications.append(notification)

        if exam is not None:
            exam.notifications.append(notification)

        s.add(notification)
        s.commit()

        return notification.notification_id