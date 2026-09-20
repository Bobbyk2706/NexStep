from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.change_impact_schemas import (
    ChangeImpactAnalysis,
)
from app.ai.complete_extraction_normalizer import (
    normalize_complete_extraction,
)
from app.ai.complete_extraction_validation import (
    validate_complete_extraction,
)
from app.ai.extraction_serialization import (
    deserialize_aggregated_extraction,
)
from app.ai.semantic_change_schemas import (
    SemanticChangeAnalysis,
)
from app.database.session import SessionLocal
from app.models.admin import Admin
from app.models.monitoring_review import MonitoringReview
from app.models.official_notification import (
    OfficialNotification,
)
from app.services.approved_extraction_service import (
    persist_approved_extraction,
)
from app.services.structural_change_detection_service import (
    StructuralChangeReport,
)


class MonitoringReviewError(RuntimeError):
    """
    Raised when a monitoring HITL operation cannot be
    completed safely.
    """


VALID_REVIEW_STATUSES = {
    "PENDING",
    "APPROVED",
    "REJECTED",
}


def _serialize(value: Any) -> str:
    """
    Serialize structured analysis for immutable storage.
    """

    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="python")

    return json.dumps(
        value,
        ensure_ascii=False,
        default=str,
    )


def _deserialize_monitoring_extraction(
    value: str,
) -> AggregatedExtractionResult:
    """
    Deserialize the stored monitoring extraction.

    Monitoring reviews are expected to contain the same
    AggregatedExtractionResult structure used by the normal
    extraction pipeline.
    """

    if not value:
        raise MonitoringReviewError(
            "Monitoring review contains no new extraction."
        )

    try:
        result = deserialize_aggregated_extraction(
            value
        )
    except Exception as error:
        raise MonitoringReviewError(
            "Stored monitoring extraction could not "
            "be deserialized safely."
        ) from error

    if not isinstance(
        result,
        AggregatedExtractionResult,
    ):
        raise MonitoringReviewError(
            "Stored monitoring extraction has an "
            "invalid structure."
        )

    return result


class _MonitoringExtractionAdapter:
    """
    Small adapter allowing the existing approved-extraction
    persistence function to be reused.

    No ExtractionHistory row is created for monitoring.
    """

    def __init__(
        self,
        *,
        notification_id: int,
        ai_summary: str | None,
    ) -> None:
        self.notification_id = notification_id
        self.ai_summary = ai_summary
        self.extraction_status = "PENDING"


def create_monitoring_review(
    *,
    notification_id: int,
    old_document_hash: str,
    new_document_hash: str,
    old_extraction: Any,
    new_extraction: Any,
    structural_report: StructuralChangeReport,
    semantic_analysis: SemanticChangeAnalysis,
    impact_analysis: ChangeImpactAnalysis,
    db: Session | None = None,
) -> int:
    """
    Create a PENDING monitoring review.

    This function only creates the HITL record.
    It does not modify the approved notification.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        notification = db.scalar(
            select(OfficialNotification)
            .where(
                OfficialNotification.notification_id
                == notification_id
            )
        )

        if notification is None:
            raise MonitoringReviewError(
                "Official notification not found."
            )

        if not old_document_hash:
            raise MonitoringReviewError(
                "Old document hash is required."
            )

        if not new_document_hash:
            raise MonitoringReviewError(
                "New document hash is required."
            )

        if (
            old_document_hash
            == new_document_hash
        ):
            raise MonitoringReviewError(
                "A monitoring review cannot be created "
                "for an unchanged document."
            )

        if not structural_report.change_detected:
            raise MonitoringReviewError(
                "A monitoring review requires a detected "
                "structural change."
            )

        review = MonitoringReview(
            notification_id=notification_id,
            old_document_hash=old_document_hash,
            new_document_hash=new_document_hash,
            old_extraction=_serialize(
                old_extraction
            ),
            new_extraction=_serialize(
                new_extraction
            ),
            structural_changes=_serialize(
                structural_report
            ),
            semantic_analysis=_serialize(
                semantic_analysis
            ),
            impact_analysis=_serialize(
                impact_analysis
            ),
            review_status="PENDING",
        )

        db.add(review)
        db.flush()

        review_id = review.review_id

        if owns_session:
            db.commit()

        return review_id

    except Exception:
        if owns_session:
            db.rollback()

        raise

    finally:
        if owns_session:
            db.close()


def approve_monitoring_review(
    *,
    review_id: int,
    admin_id: int,
    db: Session | None = None,
) -> int:
    """
    Approve a pending monitoring review.

    This function records the human decision only.

    It does NOT yet publish the monitored document into
    the authoritative notification data.

    Publishing is performed by
    apply_approved_monitoring_review().
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        admin = db.scalar(
            select(Admin)
            .where(
                Admin.admin_id == admin_id
            )
        )

        if admin is None:
            raise MonitoringReviewError(
                "Admin not found."
            )

        review = db.scalar(
            select(MonitoringReview)
            .where(
                MonitoringReview.review_id
                == review_id
            )
            .with_for_update()
        )

        if review is None:
            raise MonitoringReviewError(
                "Monitoring review not found."
            )

        if review.review_status != "PENDING":
            raise MonitoringReviewError(
                "Only PENDING monitoring reviews "
                "can be approved."
            )

        notification = db.scalar(
            select(OfficialNotification)
            .where(
                OfficialNotification.notification_id
                == review.notification_id
            )
            .with_for_update()
        )

        if notification is None:
            raise MonitoringReviewError(
                "Official notification not found."
            )

        # --------------------------------------------------------
        # Safety check:
        #
        # The approved notification must still represent the
        # document against which this review was created.
        # --------------------------------------------------------

        if (
            notification.document_hash
            != review.old_document_hash
        ):
            raise MonitoringReviewError(
                "Monitoring review is stale. The approved "
                "notification has changed since this review "
                "was created."
            )

        review.review_status = "APPROVED"
        review.reviewed_by = admin_id
        review.reviewed_at = datetime.now()
        review.rejection_reason = None

        db.flush()

        if owns_session:
            db.commit()

        return review.review_id

    except Exception:
        if owns_session:
            db.rollback()

        raise

    finally:
        if owns_session:
            db.close()


def reject_monitoring_review(
    *,
    review_id: int,
    admin_id: int,
    rejection_reason: str,
    db: Session | None = None,
) -> int:
    """
    Reject a pending monitoring review.

    Rejection does not modify the approved notification.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        admin = db.scalar(
            select(Admin)
            .where(
                Admin.admin_id == admin_id
            )
        )

        if admin is None:
            raise MonitoringReviewError(
                "Admin not found."
            )

        if not rejection_reason.strip():
            raise MonitoringReviewError(
                "Rejection reason is required."
            )

        review = db.scalar(
            select(MonitoringReview)
            .where(
                MonitoringReview.review_id
                == review_id
            )
            .with_for_update()
        )

        if review is None:
            raise MonitoringReviewError(
                "Monitoring review not found."
            )

        if review.review_status != "PENDING":
            raise MonitoringReviewError(
                "Only PENDING monitoring reviews "
                "can be rejected."
            )

        review.review_status = "REJECTED"
        review.reviewed_by = admin_id
        review.reviewed_at = datetime.now()
        review.rejection_reason = (
            rejection_reason.strip()
        )

        db.flush()

        if owns_session:
            db.commit()

        return review.review_id

    except Exception:
        if owns_session:
            db.rollback()

        raise

    finally:
        if owns_session:
            db.close()


def apply_approved_monitoring_review(
    *,
    review_id: int,
    db: Session | None = None,
) -> int:
    """
    Publish an APPROVED monitoring review into the
    authoritative exam data.

    Pipeline:

        APPROVED MonitoringReview
                ↓
        lock review
                ↓
        lock notification
                ↓
        stale-document check
                ↓
        deserialize new extraction
                ↓
        normalize
                ↓
        validate
                ↓
        persist exam dates
                ↓
        persist eligibility rule tree
                ↓
        update document hash
                ↓
        commit atomically

    Student eligibility is intentionally NOT re-evaluated
    here. That belongs to the next phase.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        # --------------------------------------------------------
        # 1. Lock monitoring review
        # --------------------------------------------------------

        review = db.scalar(
            select(MonitoringReview)
            .where(
                MonitoringReview.review_id
                == review_id
            )
            .with_for_update()
        )

        if review is None:
            raise MonitoringReviewError(
                "Monitoring review not found."
            )

        # --------------------------------------------------------
        # 2. Only APPROVED reviews may be published
        # --------------------------------------------------------

        if review.review_status != "APPROVED":
            raise MonitoringReviewError(
                "Only APPROVED monitoring reviews "
                "can be applied."
            )

        if review.reviewed_by is None:
            raise MonitoringReviewError(
                "Approved monitoring review has no "
                "recorded administrator."
            )

        # --------------------------------------------------------
        # 3. Lock authoritative notification
        # --------------------------------------------------------

        notification = db.scalar(
            select(OfficialNotification)
            .where(
                OfficialNotification.notification_id
                == review.notification_id
            )
            .with_for_update()
        )

        if notification is None:
            raise MonitoringReviewError(
                "Official notification not found."
            )

        # --------------------------------------------------------
        # 4. Prevent stale publication
        # --------------------------------------------------------

        if (
            notification.document_hash
            != review.old_document_hash
        ):
            raise MonitoringReviewError(
                "Monitoring review is stale. The approved "
                "notification no longer matches the document "
                "from which this review was created."
            )

        # --------------------------------------------------------
        # 5. Prevent accidental double application
        # --------------------------------------------------------

        if (
            notification.document_hash
            == review.new_document_hash
        ):
            raise MonitoringReviewError(
                "Monitoring review has already been applied."
            )

        # --------------------------------------------------------
        # 6. Deserialize the new extraction
        # --------------------------------------------------------

        extraction_result = (
            _deserialize_monitoring_extraction(
                review.new_extraction
            )
        )

        # --------------------------------------------------------
        # 7. Normalize
        # --------------------------------------------------------

        try:
            normalized_extraction = (
                normalize_complete_extraction(
                    extraction_result.extraction
                )
            )
        except Exception as error:
            raise MonitoringReviewError(
                "Approved monitoring extraction could "
                "not be normalized safely."
            ) from error

        normalized_result = AggregatedExtractionResult(
            extraction=normalized_extraction,
            evidence=extraction_result.evidence,
        )

        # --------------------------------------------------------
        # 8. Validate again immediately before publication
        # --------------------------------------------------------

        try:
            validation_errors = (
                validate_complete_extraction(
                    normalized_extraction
                )
            )
        except Exception as error:
            raise MonitoringReviewError(
                "Approved monitoring extraction could "
                "not be validated safely."
            ) from error

        if validation_errors:
            raise MonitoringReviewError(
                "Approved monitoring extraction failed "
                "validation: "
                f"{validation_errors}"
            )

        # --------------------------------------------------------
        # 9. Extract semantic summary for audit/display
        # --------------------------------------------------------

        semantic_summary = None

        try:
            semantic_payload = json.loads(
                review.semantic_analysis
            )

            if isinstance(
                semantic_payload,
                dict,
            ):
                summary = semantic_payload.get(
                    "overall_summary"
                )

                if summary is not None:
                    semantic_summary = str(
                        summary
                    ).strip() or None

        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            # The semantic analysis is already stored as part
            # of the review. Failure to read the optional
            # display summary must not silently alter the
            # extraction itself.
            semantic_summary = None

        # --------------------------------------------------------
        # 10. Reuse the authoritative extraction persistence
        #     implementation.
        #
        # This keeps monitoring publication consistent with
        # normal extraction approval:
        #
        # - notification dates
        # - exam dates
        # - recursive eligibility rule tree
        # - approval state
        # --------------------------------------------------------

        extraction_adapter = (
            _MonitoringExtractionAdapter(
                notification_id=(
                    notification.notification_id
                ),
                ai_summary=(
                    notification.ai_summary
                ),
            )
        )

        try:
            persist_approved_extraction(
                session=db,
                extraction_history=(
                    extraction_adapter
                ),
                extraction_result=(
                    normalized_result
                ),
            )
        except Exception as error:
            raise MonitoringReviewError(
                "Approved monitoring extraction could "
                "not be published safely."
            ) from error

        # --------------------------------------------------------
        # 11. Update the authoritative document fingerprint
        # --------------------------------------------------------

        notification.document_hash = (
            review.new_document_hash
        )

        notification.downloaded_on = datetime.now()

        if semantic_summary is not None:
            notification.ai_change_summary = (
                semantic_summary
            )

        db.flush()

        # --------------------------------------------------------
        # 12. Commit only when this function owns the session.
        #
        # If a caller supplied the session, the caller owns
        # the outer transaction.
        # --------------------------------------------------------

        if owns_session:
            db.commit()

        return review.review_id

    except MonitoringReviewError:
        if owns_session:
            db.rollback()

        raise

    except Exception as error:
        if owns_session:
            db.rollback()

        raise MonitoringReviewError(
            "Monitoring review could not be applied safely."
        ) from error

    finally:
        if owns_session:
            db.close()


def get_monitoring_review(
    review_id: int,
    db: Session | None = None,
) -> MonitoringReview:
    """
    Retrieve one monitoring review.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        review = db.scalar(
            select(MonitoringReview)
            .where(
                MonitoringReview.review_id
                == review_id
            )
        )

        if review is None:
            raise MonitoringReviewError(
                "Monitoring review not found."
            )

        return review

    finally:
        if owns_session:
            db.close()