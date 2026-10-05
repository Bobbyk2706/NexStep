"""
Email sender: SMTP (local development) or an HTTPS email API (deployment).

Render's free web services block outbound SMTP ports (25/465/587), so a
deployed app must send through an HTTPS API instead. Pick the transport
in backend/.env:

    EMAIL_ENABLED=true
    EMAIL_PROVIDER=smtp          # smtp (default) | brevo | resend

  smtp   (works on your own computer):
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USERNAME=yourgmail@gmail.com
    SMTP_PASSWORD=your_16_char_app_password
    SMTP_FROM=NexStep <yourgmail@gmail.com>

  brevo / resend   (works on Render free):
    EMAIL_API_KEY=your_api_key
    EMAIL_FROM=NexStep <sender-you-verified-with-the-provider@example.com>

Secrets are never logged.
"""

from __future__ import annotations

import logging
import os
import re
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import parseaddr

import requests

logger = logging.getLogger("app.notifications")

_API_PROVIDERS = {"brevo", "resend"}


class EmailSendError(RuntimeError):
    """Raised when an email could not be sent."""


# Requires a real dotted domain, so "x@nexstep" is not deliverable.
_ADDRESS_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@.]{2,}$")


def is_deliverable_address(address: str | None) -> bool:
    return bool(address and _ADDRESS_PATTERN.match(address.strip()))


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _provider() -> str:
    return (os.getenv("EMAIL_PROVIDER") or "smtp").strip().lower()


def _api_key() -> str:
    return (os.getenv("EMAIL_API_KEY") or "").strip()


def _api_sender() -> str:
    return (
        os.getenv("EMAIL_FROM") or os.getenv("SMTP_FROM") or ""
    ).strip()


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

    if _provider() in _API_PROVIDERS:
        return bool(_api_key() and _api_sender())

    cfg = _settings()
    return bool(cfg["host"] and cfg["username"] and cfg["password"])


# ------------------------------------------------------------- HTTPS APIs ---


def _api_error_text(response: requests.Response) -> str:
    try:
        data = response.json()
        message = data.get("message") or data.get("error") or ""
    except ValueError:
        message = ""

    return str(message)[:200]


def _send_via_api(
    provider: str,
    to_address: str,
    subject: str,
    text_body: str,
    html_body: str | None,
) -> None:
    key = _api_key()
    sender = _api_sender()

    if provider == "resend":
        url = "https://api.resend.com/emails"
        headers = {"Authorization": f"Bearer {key}"}
        payload = {
            "from": sender,
            "to": [to_address],
            "subject": subject,
            "text": text_body,
        }
        if html_body:
            payload["html"] = html_body

    else:  # brevo
        name, address = parseaddr(sender)
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {"api-key": key, "accept": "application/json"}
        payload = {
            "sender": {"name": name or "NexStep", "email": address or sender},
            "to": [{"email": to_address}],
            "subject": subject,
            "textContent": text_body,
        }
        if html_body:
            payload["htmlContent"] = html_body

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20,
        )
    except requests.RequestException as exc:
        raise EmailSendError(
            f"Could not reach the {provider} email service."
        ) from exc

    if response.status_code in (401, 403):
        raise EmailSendError(
            f"{provider} rejected the credentials or sender "
            "(check EMAIL_API_KEY and that EMAIL_FROM is verified). "
            + _api_error_text(response)
        )

    if response.status_code >= 400:
        raise EmailSendError(
            f"{provider} rejected the email (HTTP {response.status_code}). "
            + _api_error_text(response)
        )


# -------------------------------------------------------------------- SMTP ---


def _send_via_smtp(
    to_address: str,
    subject: str,
    text_body: str,
    html_body: str | None,
) -> None:
    cfg = _settings()

    message = EmailMessage()
    message["Subject"] = subject
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


# ------------------------------------------------------------------ public ---


def send_email(
    to_address: str,
    subject: str,
    text_body: str,
    html_body: str | None = None,
) -> None:
    """Send one email. Raises EmailSendError on any failure."""

    if not is_email_enabled():
        raise EmailSendError("Email sending is disabled or not configured.")

    subject = " ".join((subject or "NexStep").split())
    provider = _provider()

    if provider in _API_PROVIDERS:
        _send_via_api(provider, to_address, subject, text_body, html_body)
    else:
        _send_via_smtp(to_address, subject, text_body, html_body)

    logger.info("Email sent to %s via %s", to_address, provider)