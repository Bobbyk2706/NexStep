from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.official_notification import (
    OfficialNotification,
)
from app.services.exam_discovery_service import (
    download_pdf,
)


# ============================================================
# MONITORING RESULT
# ============================================================


def monitor_notification(
    notification_id: int,
    db: Session | None = None,
):
    """
    Check the exact official document associated with an
    approved notification.

    This phase only performs deterministic hash comparison.

    It does NOT:
        - overwrite approved data
        - create a new extraction
        - run Gemini
        - approve changes
        - reject changes
        - re-evaluate students
        - send notifications
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:

        # ----------------------------------------------------
        # 1. Load notification
        # ----------------------------------------------------

        notification = db.scalar(
            select(OfficialNotification)
            .where(
                OfficialNotification.notification_id
                == notification_id
            )
        )

        if notification is None:
            raise ValueError(
                "Official notification not found."
            )

        # ----------------------------------------------------
        # 2. Only approved notifications are monitored
        # ----------------------------------------------------

        if notification.approval_status != "APPROVED":
            raise ValueError(
                "Only approved official notifications "
                "can be monitored."
            )

        # ----------------------------------------------------
        # 3. Exact source URL is required
        # ----------------------------------------------------

        if not notification.document_url:
            raise ValueError(
                "Approved notification has no document URL."
            )

        # ----------------------------------------------------
        # 4. Existing approved hash is required
        # ----------------------------------------------------

        if not notification.document_hash:
            raise ValueError(
                "Approved notification has no document hash."
            )

        # ----------------------------------------------------
        # 5. Download current document.
        #
        # IMPORTANT:
        # save_to_storage=False prevents a newly detected
        # document from overwriting the approved PDF.
        # ----------------------------------------------------

        current_document = download_pdf(
            notification.document_url,
            save_to_storage=False,
        )

        current_hash = (
            current_document[
                "document_hash"
            ]
        )

        stored_hash = (
            notification.document_hash
        )

        # ----------------------------------------------------
        # 6. Deterministic comparison
        # ----------------------------------------------------

        if current_hash == stored_hash:

            return {
                "notification_id": notification_id,
                "status": "NO_CHANGE",
                "changed": False,
                "previous_hash": stored_hash,
                "current_hash": current_hash,
                "document_url": (
                    notification.document_url
                ),
            }

        # ----------------------------------------------------
        # 7. Changed document
        #
        # Nothing is written to the approved notification.
        # ----------------------------------------------------

        return {
            "notification_id": notification_id,
            "status": "CHANGE_DETECTED",
            "changed": True,
            "previous_hash": stored_hash,
            "current_hash": current_hash,
            "document_url": (
                notification.document_url
            ),
            "content": current_document[
                "content"
            ],
        }

    finally:

        if owns_session:
            db.close()