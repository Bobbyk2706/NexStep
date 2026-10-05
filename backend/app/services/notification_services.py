"""
Student notifications: in-app rows + email delivery.

Every notification is saved first; the email is sent afterwards in a
background thread, so an admin's Approve button never waits on SMTP and
a mail failure never undoes an approval.

Public API
----------
create_notification(...)                    one student, one notification
queue_new_exam_notifications(id)            new exam approved -> eligible students
queue_exam_changed_notifications(id, rid)   details changed   -> tracking students
queue_eligibility_change_notifications(r)   eligibility flipped -> that student
send_deadline_reminders()                   daily job -> tracking, not-ineligible
resend_email(id)                            admin retry
list_notification_log() / notification_summary()   admin page
get_notifications() / mark_notification_as_read()  kept for existing callers
"""

from __future__ import annotations

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from html import escape

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.database.session import SessionLocal
from app.models.exam import Exam
from app.models.notification import Notification
from app.models.official_notification import OfficialNotification
from app.models.student import Student
from app.models.studentexameligibility import StudentExamEligibility
from app.models.tracked_exam import TrackedExam
from app.services.email_service import (
    EmailSendError,
    is_deliverable_address,
    is_email_enabled,
    send_email,
)

logger = logging.getLogger("app.notifications")


# The frontend maps these by substring (see src/api/notifications.js):
#   DEADLINE -> deadline, ELIGIBLE -> new-eligible, EXAM -> exam, else update.
NEW_EXAM = "NEW_ELIGIBLE_EXAM"
EXAM_UPDATED = "EXAM_UPDATED"
DEADLINE = "DEADLINE_REMINDER"
ELIGIBILITY_CHANGED = "ELIGIBILITY_CHANGED"

_BLOCKED_STATUSES = {"suspended", "inactive", "disabled"}

# Emails go out on this pool; fan-out jobs on the other, so a big
# fan-out can never starve email delivery.
_email_pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="notif-email")
_job_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="notif-job")


# ============================================================
# EMAIL DELIVERY
# ============================================================


def _exam_link(exam_id: int | None) -> str:
    base = (os.getenv("FRONTEND_URL") or "http://localhost:5173").rstrip("/")
    return f"{base}/exams/{exam_id}" if exam_id else base


def _render_email(
    student_name: str,
    notification: Notification,
) -> tuple[str, str]:
    link = _exam_link(notification.exam_id)
    name = (student_name or "there").strip()

    text = (
        f"Hi {name},\n\n"
        f"{notification.message}\n\n"
        f"View details: {link}\n\n"
        "- NexStep"
    )

    html = (
        '<div style="font-family:Arial,sans-serif;max-width:560px;'
        'margin:auto;color:#1e293b">'
        f"<p>Hi {escape(name)},</p>"
        f"<p>{escape(notification.message)}</p>"
        f'<p><a href="{escape(link)}" style="background:#4f46e5;color:#fff;'
        'padding:10px 18px;border-radius:8px;text-decoration:none">'
        "View details</a></p>"
        '<p style="color:#94a3b8;font-size:12px">Sent by NexStep</p>'
        "</div>"
    )

    return text, html


def _deliver_email(notification_id: int) -> None:
    """Send the email for one saved notification and record the result."""

    try:
        with SessionLocal() as s:
            notification = s.get(Notification, notification_id)

            if notification is None:
                return

            student = s.get(Student, notification.student_id)
            address = (student.email or "").strip() if student else ""

            if not is_deliverable_address(address):
                notification.email_status = "SKIPPED"
                notification.email_error = "Student email address is not valid."
                s.commit()
                return

            if not is_email_enabled():
                notification.email_status = "SKIPPED"
                notification.email_error = (
                    "Email sending is disabled or not configured."
                )
                s.commit()
                return

            text, html = _render_email(student.name, notification)

            try:
                send_email(address, notification.title, text, html)

            except EmailSendError as exc:
                notification.email_status = "FAILED"
                notification.email_error = str(exc)[:500]
                notification.email_sent_at = None
                logger.warning(
                    "Email FAILED for notification %s: %s",
                    notification_id,
                    exc,
                )

            else:
                notification.email_status = "SENT"
                notification.email_error = None
                notification.email_sent_at = datetime.now()

            s.commit()

    except Exception:
        logger.exception(
            "Email delivery crashed for notification %s", notification_id
        )


def resend_email(notification_id: int) -> str:
    """Retry one email now (used by the admin page). Returns new status."""

    with SessionLocal() as s:
        notification = s.get(Notification, notification_id)

        if notification is None:
            raise ValueError("Notification not found")

        notification.email_status = "PENDING"
        notification.email_error = None
        s.commit()

    _deliver_email(notification_id)

    with SessionLocal() as s:
        notification = s.get(Notification, notification_id)
        return notification.email_status or "PENDING"


# ============================================================
# CREATE ONE NOTIFICATION
# ============================================================


def create_notification(
    student_id,
    notification_type,
    title,
    message,
    exam_id=None,
    dedupe_key=None,
    send_email=True,
):
    """
    Save a notification for one student and queue its email.

    Returns the new notification_id, or None when `dedupe_key` shows this
    student was already notified about this event.
    """

    with SessionLocal() as s:
        student = s.get(Student, student_id)

        if student is None:
            raise ValueError("Student not found")

        if exam_id is not None and s.get(Exam, exam_id) is None:
            raise ValueError("Exam not found")

        if dedupe_key:
            existing = s.scalar(
                select(Notification.notification_id).where(
                    Notification.dedupe_key == dedupe_key
                )
            )
            if existing is not None:
                return None

        notification = Notification(
            student_id=student_id,
            exam_id=exam_id,
            notification_type=notification_type,
            title=title,
            message=message,
            is_read=False,
            created_at=datetime.now(),
            read_at=None,
            dedupe_key=dedupe_key,
            email_status="PENDING" if send_email else None,
        )
        s.add(notification)

        try:
            s.commit()
        except IntegrityError:
            # Another worker saved the same dedupe_key first.
            s.rollback()
            return None

        notification_id = notification.notification_id

    if send_email:
        _email_pool.submit(_deliver_email, notification_id)

    return notification_id


# ============================================================
# HELPERS
# ============================================================


def _active_student_ids(s, student_ids) -> list[int]:
    ids = list(student_ids)

    if not ids:
        return []

    rows = s.execute(
        select(Student.student_id, Student.account_status).where(
            Student.student_id.in_(ids)
        )
    ).all()

    return [
        student_id
        for student_id, status in rows
        if (status or "").lower() not in _BLOCKED_STATUSES
    ]


def _tracking_student_ids(s, exam_id: int) -> list[int]:
    ids = s.scalars(
        select(TrackedExam.student_id)
        .where(
            TrackedExam.exam_id == exam_id,
            TrackedExam.tracking_status == "ACTIVE",
        )
        .distinct()
    ).all()

    return _active_student_ids(s, ids)


def _latest_eligibility_status(s, student_id: int, exam_id: int):
    return s.scalar(
        select(StudentExamEligibility.eligibility_status)
        .where(
            StudentExamEligibility.student_id == student_id,
            StudentExamEligibility.exam_id == exam_id,
        )
        .order_by(
            StudentExamEligibility.evaluated_at.desc(),
            StudentExamEligibility.eligibility_id.desc(),
        )
        .limit(1)
    )


def _run_safely(label: str, fn, *args) -> None:
    """Run a fan-out job; log (never raise) so callers are unaffected."""

    try:
        count = fn(*args)
        logger.info("%s finished: %s notification(s) created", label, count)
    except Exception:
        logger.exception("%s failed", label)


# ============================================================
# TRIGGER 1: NEW EXAM APPROVED -> ELIGIBLE STUDENTS
# ============================================================


def notify_new_exam_approved(notification_id: int) -> int:
    from app.services.eligibility_service import evaluate_eligibility

    with SessionLocal() as s:
        official = s.get(OfficialNotification, notification_id)

        if official is None or official.approval_status != "APPROVED":
            return 0

        exam_id = official.exam_id
        exam = s.get(Exam, exam_id)
        exam_name = exam.name if exam else official.title
        deadline = official.application_end_date

        students = s.scalars(
            select(Student)
            .options(
                selectinload(Student.educations),
                selectinload(Student.work_experiences),
            )
            .order_by(Student.student_id)
        ).unique().all()

        recipients: list[int] = []

        for student in students:
            if (student.account_status or "").lower() in _BLOCKED_STATUSES:
                continue

            try:
                evaluation = evaluate_eligibility(
                    student=student,
                    exam_id=exam_id,
                    db=s,
                )
            except Exception:
                # Incomplete profile or unevaluable rules: skip this student.
                continue

            if evaluation.eligible:
                recipients.append(student.student_id)

    message = f"You meet the eligibility criteria for {exam_name}."

    if deadline:
        message += f" Applications close on {deadline:%d %b %Y}."

    message += " Open NexStep to see the dates and requirements."

    created = 0

    for student_id in recipients:
        try:
            result = create_notification(
                student_id,
                NEW_EXAM,
                f"You're eligible: {exam_name}",
                message,
                exam_id,
                dedupe_key=f"new_exam:{student_id}:{notification_id}",
            )
            created += 1 if result is not None else 0
        except Exception:
            logger.exception(
                "Could not notify student %s about new exam", student_id
            )

    return created


def queue_new_exam_notifications(notification_id: int) -> None:
    _job_pool.submit(
        _run_safely,
        "New-exam notifications",
        notify_new_exam_approved,
        notification_id,
    )


# ============================================================
# TRIGGER 2: EXAM DETAILS CHANGED -> TRACKING STUDENTS
# ============================================================


def notify_exam_details_changed(
    notification_id: int,
    review_id: int | None = None,
) -> int:
    with SessionLocal() as s:
        official = s.get(OfficialNotification, notification_id)

        if official is None:
            return 0

        exam_id = official.exam_id
        exam = s.get(Exam, exam_id)
        exam_name = exam.name if exam else official.title
        summary = (official.ai_change_summary or "").strip()
        student_ids = _tracking_student_ids(s, exam_id)

    event_key = (
        review_id if review_id is not None else int(datetime.now().timestamp())
    )

    message = f"The official notification for {exam_name} was updated. "
    message += summary or "Check the new dates and eligibility rules."

    created = 0

    for student_id in student_ids:
        try:
            result = create_notification(
                student_id,
                EXAM_UPDATED,
                f"Update: {exam_name}",
                message[:1000],
                exam_id,
                dedupe_key=f"exam_updated:{student_id}:{event_key}",
            )
            created += 1 if result is not None else 0
        except Exception:
            logger.exception(
                "Could not notify student %s about exam update", student_id
            )

    return created


def queue_exam_changed_notifications(
    notification_id: int,
    review_id: int | None = None,
) -> None:
    _job_pool.submit(
        _run_safely,
        "Exam-update notifications",
        notify_exam_details_changed,
        notification_id,
        review_id,
    )


# ============================================================
# TRIGGER 3: ELIGIBILITY CHANGED -> THAT STUDENT
# ============================================================


def notify_eligibility_changes(result) -> int:
    """`result` is an EligibilityReEvaluationResult."""

    changes = [r for r in result.results if r.status_changed]

    if not changes:
        return 0

    with SessionLocal() as s:
        exam = s.get(Exam, result.exam_id)
        exam_name = exam.name if exam else f"exam {result.exam_id}"

    created = 0

    for change in changes:
        became_eligible = change.new_status == "ELIGIBLE"

        if became_eligible:
            title = f"You are now eligible for {exam_name}"
            message = (
                "Based on the updated notification, you now meet the "
                "eligibility criteria."
            )
        else:
            title = f"Your eligibility for {exam_name} has changed"
            message = (
                "Based on the updated notification, you no longer meet "
                "all the eligibility criteria."
            )
            reason = (change.reason or "").strip()
            if reason:
                message += " " + reason[:300]

        try:
            notification_id = create_notification(
                change.student_id,
                ELIGIBILITY_CHANGED,
                title,
                message,
                result.exam_id,
            )
            created += 1 if notification_id is not None else 0
        except Exception:
            logger.exception(
                "Could not notify student %s about eligibility change",
                change.student_id,
            )

    return created


def queue_eligibility_change_notifications(result) -> None:
    _job_pool.submit(
        _run_safely,
        "Eligibility-change notifications",
        notify_eligibility_changes,
        result,
    )


# ============================================================
# TRIGGER 4: APPLICATION DEADLINE -> DAILY JOB
# ============================================================


def send_deadline_reminders(window_days: int = 7) -> dict:
    """
    Remind students tracking an exam whose application deadline is within
    `window_days`. Students whose latest eligibility is NOT_ELIGIBLE are
    skipped.

    Each student gets at most one reminder per tier (7 / 3 / 1 days).
    A tier is chosen from the days left, so a missed day never loses a
    reminder, and running this twice is harmless (de-duplicated).
    """

    today = date.today()
    last_day = today + timedelta(days=window_days)

    jobs: list[tuple] = []

    with SessionLocal() as s:
        exams = s.execute(
            select(
                OfficialNotification.notification_id,
                OfficialNotification.exam_id,
                OfficialNotification.title,
                OfficialNotification.application_end_date,
            ).where(
                OfficialNotification.approval_status == "APPROVED",
                OfficialNotification.application_end_date.is_not(None),
                OfficialNotification.application_end_date >= today,
                OfficialNotification.application_end_date <= last_day,
            )
        ).all()

        for official_id, exam_id, title, end_date in exams:
            exam = s.get(Exam, exam_id)
            exam_name = exam.name if exam else title
            days_left = (end_date - today).days
            tier = 1 if days_left <= 1 else 3 if days_left <= 3 else 7

            for student_id in _tracking_student_ids(s, exam_id):
                status = _latest_eligibility_status(s, student_id, exam_id)

                if status == "NOT_ELIGIBLE":
                    continue

                jobs.append(
                    (student_id, exam_id, exam_name, end_date,
                     days_left, tier, official_id)
                )

    created = 0

    for (student_id, exam_id, exam_name, end_date,
         days_left, tier, official_id) in jobs:

        if days_left <= 0:
            title = f"Last day to apply: {exam_name}"
            when = "today"
        else:
            title = f"{days_left} day(s) left to apply: {exam_name}"
            when = f"on {end_date:%d %b %Y} ({days_left} day(s) left)"

        try:
            result = create_notification(
                student_id,
                DEADLINE,
                title,
                f"Applications for {exam_name} close {when}.",
                exam_id,
                dedupe_key=f"deadline:{student_id}:{official_id}:{tier}",
            )
            created += 1 if result is not None else 0
        except Exception:
            logger.exception(
                "Could not create deadline reminder for student %s",
                student_id,
            )

    return {"exams_in_window": len(exams), "created": created}


# ============================================================
# ADMIN PAGE QUERIES
# ============================================================


def list_notification_log(
    *,
    email_status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    with SessionLocal() as s:
        statement = (
            select(
                Notification,
                Student.name,
                Student.email,
                Exam.name,
            )
            .join(Student, Student.student_id == Notification.student_id)
            .outerjoin(Exam, Exam.exam_id == Notification.exam_id)
            .order_by(
                Notification.created_at.desc(),
                Notification.notification_id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        if email_status:
            statement = statement.where(
                Notification.email_status == email_status
            )

        rows = s.execute(statement).all()

        return [
            {
                "notification_id": n.notification_id,
                "student_id": n.student_id,
                "student_name": student_name,
                "student_email": student_email,
                "exam_id": n.exam_id,
                "exam_name": exam_name,
                "notification_type": n.notification_type,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at,
                "email_status": n.email_status,
                "email_sent_at": n.email_sent_at,
                "email_error": n.email_error,
            }
            for n, student_name, student_email, exam_name in rows
        ]


def notification_summary() -> dict:
    with SessionLocal() as s:
        total = s.scalar(select(func.count(Notification.notification_id))) or 0
        rows = s.execute(
            select(Notification.email_status, func.count()).group_by(
                Notification.email_status
            )
        ).all()

    counts = {(status or "NONE"): count for status, count in rows}

    return {
        "total": total,
        "sent": counts.get("SENT", 0),
        "failed": counts.get("FAILED", 0),
        "skipped": counts.get("SKIPPED", 0),
        "pending": counts.get("PENDING", 0),
        "no_email": counts.get("NONE", 0),
    }


# ============================================================
# KEPT FOR EXISTING CALLERS
# ============================================================


def get_notifications(student_id):

    with SessionLocal() as s:

        student = s.scalar(
            select(Student).where(
                Student.student_id == student_id
            )
        )

        if student is None:
            raise ValueError("Student not found")

        return student.notifications


def mark_notification_as_read(notification_id):

    with SessionLocal() as s:

        notification = s.scalar(
            select(Notification).where(
                Notification.notification_id == notification_id
            )
        )

        if notification is None:
            raise ValueError("Notification not found")

        notification.is_read = True
        notification.read_at = datetime.now()

        s.commit()