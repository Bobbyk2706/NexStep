"""
Minimal SMTP email sender (standard library only).

Configuration comes from backend/.env, read at call time:

    EMAIL_ENABLED=true
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USERNAME=yourgmail@gmail.com
    SMTP_PASSWORD=your_16_char_app_password
    SMTP_FROM=NexStep <yourgmail@gmail.com>

The password is never logged.
"""

from __future__ import annotations

import logging
import os
import re
import smtplib
import ssl
from email.message import EmailMessage

logger = logging.getLogger("app.notifications")


class EmailSendError(RuntimeError):
    """Raised when an email could not be sent."""


# Requires a real dotted domain, so "x@nexstep" is not deliverable.
_ADDRESS_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@.]{2,}$")


def is_deliverable_address(address: str | None) -> bool:
    return bool(address and _ADDRESS_PATTERN.match(address.strip()))


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _settings() -> dict:
    try:
        port = int((os.getenv("SMTP_PORT") or "587").strip())
    except ValueError:
        port = 587

    username = (os.getenv("SMTP_USERNAME") or "").strip()

    return {
        "host": (os.getenv("SMTP_HOST") or "").strip(),
        "port": port,
        "username": username,
        "password": os.getenv("SMTP_PASSWORD") or "",
        "sender": (os.getenv("SMTP_FROM") or username).strip(),
    }


def is_email_enabled() -> bool:
    if not _truthy(os.getenv("EMAIL_ENABLED")):
        return False

    cfg = _settings()
    return bool(cfg["host"] and cfg["username"] and cfg["password"])


def send_email(
    to_address: str,
    subject: str,
    text_body: str,
    html_body: str | None = None,
) -> None:
    """Send one email. Raises EmailSendError on any failure."""

    if not is_email_enabled():
        raise EmailSendError("Email sending is disabled or not configured.")

    cfg = _settings()

    message = EmailMessage()
    message["Subject"] = " ".join((subject or "NexStep").split())
    message["From"] = cfg["sender"]
    message["To"] = to_address
    message.set_content(text_body)

    if html_body:
        message.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()

    try:
        if cfg["port"] == 465:
            with smtplib.SMTP_SSL(
                cfg["host"], cfg["port"], timeout=20, context=context
            ) as server:
                server.login(cfg["username"], cfg["password"])
                server.send_message(message)
        else:
            with smtplib.SMTP(cfg["host"], cfg["port"], timeout=20) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(cfg["username"], cfg["password"])
                server.send_message(message)

    except smtplib.SMTPAuthenticationError as exc:
        raise EmailSendError(
            "SMTP login failed. Check SMTP_USERNAME and the app password."
        ) from exc

    except (smtplib.SMTPException, OSError, ValueError) as exc:
        raise EmailSendError(f"Could not send email: {exc}") from exc

    logger.info("Email sent to %s", to_address)