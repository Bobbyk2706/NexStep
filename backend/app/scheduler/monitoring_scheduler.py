from __future__ import annotations

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.services.exam_monitoring_service import (
    monitor_notification,
)

logger = logging.getLogger(__name__)


# ============================================================
# SCHEDULER
# ============================================================

scheduler = BackgroundScheduler()


# ============================================================
# APPROVED NOTIFICATIONS
# ============================================================


def get_approved_notification_ids() -> list[int]:
    """
    Return the IDs of all approved official notifications.

    Only APPROVED notifications are eligible for automatic
    monitoring.
    """

    with SessionLocal() as db:

        statement = (
    select(OfficialNotification.notification_id)
    .where(
        OfficialNotification.approval_status == "APPROVED",
        OfficialNotification.document_url.is_not(None),
        OfficialNotification.document_hash.is_not(None),
    )
    .order_by(OfficialNotification.notification_id)
)

        return list(
            db.scalars(statement).all()
        )


# ============================================================
# MONITORING CYCLE
# ============================================================


def run_monitoring_cycle() -> dict:
    """
    Execute one monitoring cycle.

    Every approved notification is monitored independently.

    A failure for one notification does not stop the
    remaining notifications from being processed.
    """

    logger.info(
        "Starting monitoring cycle."
    )

    notification_ids = (
        get_approved_notification_ids()
    )

    results: list[dict] = []

    for notification_id in notification_ids:

        try:

            result = monitor_notification(
                notification_id=notification_id
            )

            results.append(
                {
                    "notification_id": notification_id,
                    "status": "SUCCESS",
                    "result": result,
                }
            )

            logger.info(
                "Monitoring completed for notification %s: %s",
                notification_id,
                result.get("status"),
            )

        except Exception as exc:

            logger.exception(
                "Monitoring failed for notification %s.",
                notification_id,
            )

            results.append(
                {
                    "notification_id": notification_id,
                    "status": "FAILED",
                    "error": str(exc),
                }
            )

    summary = {
        "notifications_found": len(
            notification_ids
        ),
        "notifications_processed": len(
            results
        ),
        "successful": sum(
            result["status"] == "SUCCESS"
            for result in results
        ),
        "failed": sum(
            result["status"] == "FAILED"
            for result in results
        ),
        "results": results,
    }

    logger.info(
        "Monitoring cycle completed: %s",
        summary,
    )

    return summary


# ============================================================
# SCHEDULER START
# ============================================================


def start_monitoring_scheduler() -> None:
    """
    Start the monitoring scheduler.

    The monitoring cycle runs once every 24 hours.

    Calling this function multiple times does not create
    duplicate scheduler instances.
    """

    if scheduler.running:
        logger.info(
            "Monitoring scheduler is already running."
        )
        return

    scheduler.add_job(
        run_monitoring_cycle,
        trigger="interval",
        hours=24,
        id="official_notification_monitoring",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    logger.info(
        "Monitoring scheduler started."
    )


# ============================================================
# SCHEDULER STOP
# ============================================================


def stop_monitoring_scheduler() -> None:
    """
    Stop the monitoring scheduler safely.
    """

    if not scheduler.running:
        logger.info(
            "Monitoring scheduler is not running."
        )
        return

    scheduler.shutdown(
        wait=False
    )

    logger.info(
        "Monitoring scheduler stopped."
    )


# ============================================================
# MANUAL EXECUTION
# ============================================================


def run_monitoring_cycle_now() -> dict:
    """
    Execute one monitoring cycle immediately.

    This is useful for:
        - development
        - testing
        - demonstrations
        - manually triggering monitoring

    It does not modify the scheduler configuration.
    """

    return run_monitoring_cycle()