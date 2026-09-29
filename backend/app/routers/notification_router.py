from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_student
from app.database.session import get_db
from app.models.notification import Notification
from app.models.student import Student

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _to_out(notification: Notification) -> dict:
    return {
        "notification_id": notification.notification_id,
        "student_id": notification.student_id,
        "exam_id": notification.exam_id,
        "notification_type": notification.notification_type,
        "title": notification.title,
        "message": notification.message,
        "is_read": notification.is_read,
        "created_at": notification.created_at,
        "read_at": notification.read_at,
    }


@router.get("")
def get_my_notifications(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    notifications = db.scalars(
        select(Notification)
        .where(Notification.student_id == current_student.student_id)
        .order_by(Notification.created_at.desc(), Notification.notification_id.desc())
    ).all()

    return [_to_out(notification) for notification in notifications]


@router.post("/{notification_id}/read")
def mark_my_notification_as_read(
    notification_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    notification = db.scalar(
        select(Notification).where(
            Notification.notification_id == notification_id,
            Notification.student_id == current_student.student_id,
        )
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    notification.is_read = True
    notification.read_at = datetime.now()
    db.commit()

    return _to_out(notification)


@router.post("/read-all")
def mark_all_my_notifications_as_read(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    notifications = db.scalars(
        select(Notification).where(
            Notification.student_id == current_student.student_id,
            Notification.is_read.is_(False),
        )
    ).all()

    now = datetime.now()
    for notification in notifications:
        notification.is_read = True
        notification.read_at = now

    db.commit()

    return [_to_out(notification) for notification in notifications]
