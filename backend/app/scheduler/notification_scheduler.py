"""
Daily deadline reminders.

Uses its own scheduler so it never interferes with the monitoring
scheduler. Started and stopped from app/main.py.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.notification_services import send_deadline_reminders

logger = logging.getLogger("app.notifications")

scheduler = BackgroundScheduler()


def _run_deadline_reminders() -> None:
    try:
        result = send_deadline_reminders()
        logger.info("Deadline reminders finished: %s", result)
    except Exception:
        logger.exception("Deadline reminders failed.")


def start_notification_scheduler() -> None:
    if scheduler.running:
        return

    # Every day at 09:00 server time. If the server was down then, run
    # within an hour of coming back.
    scheduler.add_job(
        _run_deadline_reminders,
        trigger="cron",
        hour=9,
        minute=0,
        id="deadline_reminders",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=3600,
    )

    # Catch-up shortly after startup. Safe to repeat: reminders are
    # de-duplicated per student, exam and tier.
    scheduler.add_job(
        _run_deadline_reminders,
        trigger="date",
        run_date=datetime.now() + timedelta(seconds=30),
        id="deadline_reminders_startup",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Notification scheduler started.")


def stop_notification_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Notification scheduler stopped.")