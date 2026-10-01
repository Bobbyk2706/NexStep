from __future__ import annotations

import logging

from apscheduler.schedulers.background import (
    BackgroundScheduler,
)
from sqlalchemy import select

from app.ai.llm_client import (
    analyze_monitoring_semantic_changes,
)
from app.database.session import SessionLocal
from app.models.official_notification import (
    OfficialNotification,
)
from app.services.monitoring_pipeline_service import (
    run_monitoring_pipeline,
)

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


# ============================================================
# APPROVED NOTIFICATIONS
# ============================================================

def get_approved_notification_ids() -> list[int]:
    """
    Return approved official notifications that have enough
    document information for monitoring.
    """

    with SessionLocal() as db:
        statement = (
            select(
                OfficialNotification.notification_id
            )
            .where(
                OfficialNotification.approval_status
                == "APPROVED",
                OfficialNotification.document_url.is_not(None),
                OfficialNotification.document_hash.is_not(None),
            )
            .order_by(
                OfficialNotification.notification_id
            )
        )

        return list(
            db.scalars(statement).all()
        )


# ============================================================
# SAFE API RESULT
# ============================================================

def _build_safe_monitoring_result(
    result: dict,
) -> dict:
    """
    Convert the detailed monitoring result into a small
    JSON-safe API response.

    Never expose PDF bytes or full extraction content.
    """

    return {
        "notification_id": result.get(
            "notification_id"
        ),
        "status": result.get("status"),
        "changed": result.get(
            "changed",
            False,
        ),
        "review_id": result.get(
            "review_id"
        ),
        "previous_hash": result.get(
            "previous_hash"
        ),
        "current_hash": result.get(
            "current_hash"
        ),
        "change_count": result.get(
            "change_count"
        ),
        "requires_human_review": result.get(
            "requires_human_review"
        ),
        "requires_eligibility_re_evaluation": result.get(
            "requires_eligibility_re_evaluation"
        ),
    }


# ============================================================
# MONITORING CYCLE
# ============================================================

def run_monitoring_cycle() -> dict:
    """
    Run the complete monitoring pipeline for every approved
    official notification.

    Flow:

        official document
              ↓
        hash comparison
              ↓
          NO_CHANGE
              ↓
        CHANGE_DETECTED
              ↓
        new extraction
              ↓
        structural comparison
              ↓
        AI semantic analysis
              ↓
        impact classification
              ↓
        MonitoringReview(PENDING)
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
            result = run_monitoring_pipeline(
                notification_id=notification_id,
                analyzer=(
                    analyze_monitoring_semantic_changes
                ),
            )

            safe_result = (
                _build_safe_monitoring_result(
                    result
                )
            )

            results.append(
                {
                    "notification_id": notification_id,
                    "status": "SUCCESS",
                    "result": safe_result,
                }
            )

            logger.info(
                "Monitoring completed for notification "
                "%s: %s",
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
# AUTOMATIC SCHEDULER
# ============================================================

def start_monitoring_scheduler() -> None:

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


def stop_monitoring_scheduler() -> None:

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
# MANUAL RUN
# ============================================================

def run_monitoring_cycle_now() -> dict:
    """
    Run monitoring immediately.

    Used by the admin dashboard.
    """

    return run_monitoring_cycle()