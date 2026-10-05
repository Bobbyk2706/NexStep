"""
Email-verified signup.

Flow:
    start_signup   -> validates, emails a 6-digit code, saves a PendingSignup
    verify_signup  -> checks the code, THEN creates the Student
    resend_code    -> sends a fresh code (cooldown + cap)

No Student row exists until the code is confirmed.

Dev option (backend/.env): SIGNUP_CODE_IN_LOG=true prints the code in the
server log when SMTP is not configured. Never use it in production.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import secrets
from datetime import datetime, timedelta
from html import escape

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.security import hash_password, new_token_version
from app.models.pending_signup import PendingSignup
from app.models.student import Student
from app.services.email_service import (
    EmailSendError,
    is_deliverable_address,
    is_email_enabled,
    send_email,
)

logger = logging.getLogger("app.notifications")

CODE_TTL_MINUTES = 10
RESEND_COOLDOWN_SECONDS = 60
MAX_ATTEMPTS = 5          # wrong codes before the signup must be restarted
MAX_SENDS_PER_HOUR = 5    # codes per email address per hour


class SignupVerificationError(Exception):
    """A problem the person can read and act on."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.status_code = status_code


# ------------------------------------------------------------- helpers ---


def _key(email: str) -> str:
    return email.strip().lower()


def _new_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def _hash_code(code: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(8)
    digest = hashlib.sha256(f"{salt}:{code}".encode("utf-8")).hexdigest()
    return f"{salt}:{digest}"


def _code_matches(code: str, stored: str) -> bool:
    salt = stored.partition(":")[0]
    return hmac.compare_digest(_hash_code(code, salt), stored)


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _seconds_until_resend(pending: PendingSignup, now: datetime) -> int:
    ready_at = pending.last_sent_at + timedelta(seconds=RESEND_COOLDOWN_SECONDS)
    return max(0, int((ready_at - now).total_seconds()) + 1) if ready_at > now else 0


def _deliver_code(email: str, name: str, code: str) -> None:
    subject = "Your NexStep verification code"

    text = (
        f"Hi {name},\n\n"
        f"Your NexStep verification code is: {code}\n\n"
        f"It expires in {CODE_TTL_MINUTES} minutes. If you didn't try to "
        "create a NexStep account, you can ignore this email.\n\n"
        "- NexStep"
    )

    html = (
        '<div style="font-family:Arial,sans-serif;max-width:480px;'
        'margin:auto;color:#1e293b">'
        f"<p>Hi {escape(name)},</p>"
        "<p>Your NexStep verification code is:</p>"
        '<p style="font-size:32px;font-weight:700;letter-spacing:6px;'
        f'margin:16px 0">{code}</p>'
        f"<p>It expires in {CODE_TTL_MINUTES} minutes. If you didn't try to "
        "create a NexStep account, you can ignore this email.</p>"
        '<p style="color:#94a3b8;font-size:12px">Sent by NexStep</p>'
        "</div>"
    )

    if is_email_enabled():
        try:
            send_email(email, subject, text, html)
        except EmailSendError as exc:
            logger.warning("Verification email failed for %s: %s", email, exc)
            raise SignupVerificationError(
                "We couldn't send the verification email. Please try again.",
                503,
            ) from exc
        return

    if _truthy(os.getenv("SIGNUP_CODE_IN_LOG")):
        logger.warning(
            "DEV ONLY: signup verification code for %s is %s", email, code
        )
        return

    raise SignupVerificationError(
        "Email verification is unavailable right now. Please try again later.",
        503,
    )


# --------------------------------------------------------------- start ---


def start_signup(
    db: Session,
    *,
    name: str,
    email: str,
    password: str,
) -> dict:
    name = " ".join(name.split())
    email = email.strip()
    key = _key(email)

    if not name:
        raise SignupVerificationError("Enter your full name.")

    if not is_deliverable_address(email):
        raise SignupVerificationError("Enter a valid email address.")

    if (
        db.query(Student.student_id)
        .filter(func.lower(Student.email) == key)
        .first()
        is not None
    ):
        raise SignupVerificationError("Email already registered")

    now = datetime.now()

    # Housekeeping: drop long-expired attempts.
    db.query(PendingSignup).filter(
        PendingSignup.expires_at < now - timedelta(days=1)
    ).delete(synchronize_session=False)

    existing = (
        db.query(PendingSignup)
        .filter(func.lower(PendingSignup.email) == key)
        .order_by(PendingSignup.pending_id.desc())
        .first()
    )

    send_count = 1

    if existing is not None:
        wait = _seconds_until_resend(existing, now)

        if wait > 0:
            raise SignupVerificationError(
                f"Please wait {wait} seconds before requesting another code.",
                429,
            )

        if existing.created_at > now - timedelta(hours=1):
            if existing.send_count >= MAX_SENDS_PER_HOUR:
                raise SignupVerificationError(
                    "Too many codes were requested for this email. "
                    "Please try again in an hour.",
                    429,
                )
            send_count = existing.send_count + 1

    code = _new_code()

    # Send first: if the email can't be sent, nothing is saved.
    _deliver_code(email, name, code)

    db.query(PendingSignup).filter(
        func.lower(PendingSignup.email) == key
    ).delete(synchronize_session=False)

    db.add(
        PendingSignup(
            email=email,
            name=name,
            password_hash=hash_password(password),
            code_hash=_hash_code(code),
            expires_at=now + timedelta(minutes=CODE_TTL_MINUTES),
            attempts=0,
            send_count=send_count,
            last_sent_at=now,
            created_at=existing.created_at if existing and send_count > 1 else now,
        )
    )
    db.commit()

    return {
        "email": email,
        "expiresInSeconds": CODE_TTL_MINUTES * 60,
        "resendAfterSeconds": RESEND_COOLDOWN_SECONDS,
    }


# -------------------------------------------------------------- verify ---


def verify_signup(db: Session, *, email: str, code: str) -> Student:
    key = _key(email)
    now = datetime.now()

    pending = (
        db.query(PendingSignup)
        .filter(func.lower(PendingSignup.email) == key)
        .order_by(PendingSignup.pending_id.desc())
        .first()
    )

    if pending is None:
        raise SignupVerificationError(
            "No signup is waiting for this email. Please start again."
        )

    if pending.expires_at < now:
        # Keep the pending row so "Resend code" can issue a fresh code.
        # Rows that stay expired for a day are purged by start_signup().
        raise SignupVerificationError(
            "This code has expired. Please request a new one."
        )

    if not _code_matches(code.strip(), pending.code_hash):
        pending.attempts += 1
        remaining = MAX_ATTEMPTS - pending.attempts

        if remaining <= 0:
            db.delete(pending)
            db.commit()
            raise SignupVerificationError(
                "Too many incorrect codes. Please start the signup again."
            )

        db.commit()
        raise SignupVerificationError(
            f"Incorrect code. {remaining} attempt(s) left."
        )

    # Code confirmed: now (and only now) create the account.
    if (
        db.query(Student.student_id)
        .filter(func.lower(Student.email) == key)
        .first()
        is not None
    ):
        db.delete(pending)
        db.commit()
        raise SignupVerificationError("Email already registered")

    student = Student(
        name=pending.name,
        email=pending.email,
        password_hash=pending.password_hash,
        account_status="active",
        token_version=new_token_version(),
    )
    db.add(student)

    db.query(PendingSignup).filter(
        func.lower(PendingSignup.email) == key
    ).delete(synchronize_session=False)

    db.commit()
    db.refresh(student)

    return student


# -------------------------------------------------------------- resend ---


def resend_code(db: Session, *, email: str) -> dict:
    key = _key(email)
    now = datetime.now()

    pending = (
        db.query(PendingSignup)
        .filter(func.lower(PendingSignup.email) == key)
        .order_by(PendingSignup.pending_id.desc())
        .first()
    )

    if pending is None:
        raise SignupVerificationError(
            "No signup is waiting for this email. Please start again."
        )

    wait = _seconds_until_resend(pending, now)

    if wait > 0:
        raise SignupVerificationError(
            f"Please wait {wait} seconds before requesting another code.",
            429,
        )

    if (
        pending.created_at > now - timedelta(hours=1)
        and pending.send_count >= MAX_SENDS_PER_HOUR
    ):
        raise SignupVerificationError(
            "Too many codes were requested for this email. "
            "Please try again in an hour.",
            429,
        )

    code = _new_code()

    _deliver_code(pending.email, pending.name, code)

    pending.code_hash = _hash_code(code)
    pending.expires_at = now + timedelta(minutes=CODE_TTL_MINUTES)
    pending.attempts = 0
    pending.send_count += 1
    pending.last_sent_at = now
    db.commit()

    return {
        "email": pending.email,
        "expiresInSeconds": CODE_TTL_MINUTES * 60,
        "resendAfterSeconds": RESEND_COOLDOWN_SECONDS,
    }