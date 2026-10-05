from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.dependencies import get_current_admin
from app.services.notification_services import (
    list_notification_log,
    notification_summary,
    resend_email,
    send_deadline_reminders,
)

router = APIRouter(
    prefix="/admin/notifications",
    tags=["admin-notifications"],
)

_EMAIL_STATUSES = {"PENDING", "SENT", "FAILED", "SKIPPED"}


@router.get("")
def get_notification_log(
    email_status: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    admin=Depends(get_current_admin),
):
    """Notifications sent to students, newest first."""

    if email_status is not None:
        email_status = email_status.upper()

        if email_status not in _EMAIL_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_status must be PENDING, SENT, FAILED or SKIPPED.",
            )

    return list_notification_log(
        email_status=email_status,
        limit=limit,
        offset=offset,
    )


@router.get("/summary")
def get_summary(admin=Depends(get_current_admin)):
    return notification_summary()


@router.post("/{notification_id}/retry-email")
def retry_email(
    notification_id: int,
    admin=Depends(get_current_admin),
):
    try:
        new_status = resend_email(notification_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return {
        "notification_id": notification_id,
        "email_status": new_status,
    }


@router.post("/run-deadline-reminders")
def run_deadline_reminders(admin=Depends(get_current_admin)):
    """Run the deadline-reminder job now (it also runs daily)."""

    return send_deadline_reminders()