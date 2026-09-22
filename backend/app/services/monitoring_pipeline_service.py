from __future__ import annotations

from typing import Any, Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.extraction_serialization import (
    deserialize_aggregated_extraction,
)
from app.database.session import SessionLocal
from app.models.extraction_history import (
    ExtractionHistory,
)
from app.services.change_impact_service import (
    classify_change_impacts,
)
from app.services.exam_monitoring_service import (
    monitor_notification,
)
from app.services.monitoring_extraction_service import (
    extract_new_monitoring_document,
)
from app.services.monitoring_review_service import (
    create_monitoring_review,
)
from app.services.semantic_change_service import (
    analyze_semantic_changes,
)
from app.services.structural_change_detection_service import (
    detect_structural_changes,
)


class MonitoringPipelineError(RuntimeError):
    """
    Raised when the monitoring orchestration pipeline
    cannot complete safely.
    """


def _get_latest_approved_extraction(
    *,
    notification_id: int,
    db: Session,
) -> AggregatedExtractionResult:
    """
    Load the latest extraction for the notification.

    The latest extraction must be APPROVED because the
    monitoring comparison must always use the authoritative
    extraction currently associated with the approved
    notification.
    """

    extraction_history = db.scalar(
        select(ExtractionHistory)
        .where(
            ExtractionHistory.notification_id
            == notification_id
        )
        .order_by(
            ExtractionHistory.extraction_id.desc()
        )
        .limit(1)
    )

    if extraction_history is None:
        raise MonitoringPipelineError(
            "No extraction history exists for the "
            "official notification."
        )

    if (
        extraction_history.extraction_status
        != "APPROVED"
    ):
        raise MonitoringPipelineError(
            "The latest extraction for the official "
            "notification is not APPROVED."
        )

    if not extraction_history.extracted_content:
        raise MonitoringPipelineError(
            "The approved extraction contains no "
            "stored extraction content."
        )

    try:
        extraction_result = (
            deserialize_aggregated_extraction(
                extraction_history.extracted_content
            )
        )

    except Exception as error:
        raise MonitoringPipelineError(
            "The approved extraction could not be "
            "deserialized safely."
        ) from error

    if not isinstance(
        extraction_result,
        AggregatedExtractionResult,
    ):
        raise MonitoringPipelineError(
            "The approved extraction has an invalid "
            "structure."
        )

    return extraction_result


def run_monitoring_pipeline(
    *,
    notification_id: int,
    analyzer: Callable[[str], Any],
    db: Session | None = None,
) -> dict[str, Any]:
    """
    Run the complete NexStep monitoring orchestration.

    Pipeline:

        approved notification
                ↓
        deterministic hash monitoring
                ↓
            NO_CHANGE
                ↓
             return

        CHANGE_DETECTED
                ↓
        extract new document
                ↓
        load latest approved extraction
                ↓
        deterministic structural comparison
                ↓
        semantic AI interpretation
                ↓
        deterministic impact classification
                ↓
        create PENDING monitoring review

    IMPORTANT:

        This function never approves a monitoring review.

        It never directly modifies the authoritative
        notification.

        Human approval and publication are handled later by
        monitoring_review_service.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        # ====================================================
        # 1. CHECK THE OFFICIAL DOCUMENT
        # ====================================================

        monitoring_result = monitor_notification(
            notification_id=notification_id,
            db=db,
        )

        # ====================================================
        # 2. NO CHANGE
        # ====================================================

        if monitoring_result["status"] == "NO_CHANGE":

            return {
                "notification_id": notification_id,
                "status": "NO_CHANGE",
                "changed": False,
                "previous_hash": (
                    monitoring_result[
                        "previous_hash"
                    ]
                ),
                "current_hash": (
                    monitoring_result[
                        "current_hash"
                    ]
                ),
            }

        # ====================================================
        # 3. EXPECT A CHANGE RESULT
        # ====================================================

        if (
            monitoring_result["status"]
            != "CHANGE_DETECTED"
        ):
            raise MonitoringPipelineError(
                "Unexpected monitoring result status: "
                f"{monitoring_result['status']}"
            )

        new_document_hash = (
            monitoring_result["current_hash"]
        )

        new_document_content = (
            monitoring_result.get("content")
        )

        if not new_document_content:
            raise MonitoringPipelineError(
                "Changed monitoring document contains "
                "no PDF content."
            )

        # ====================================================
        # 4. EXTRACT THE NEW DOCUMENT
        # ====================================================

        extraction_result = (
            extract_new_monitoring_document(
                pdf_content=new_document_content,
                document_hash=new_document_hash,
            )
        )

        if (
            extraction_result.get("status")
            != "VALIDATED"
        ):
            raise MonitoringPipelineError(
                "New monitoring extraction was not "
                "validated successfully."
            )

        new_aggregated_extraction = (
            extraction_result.get("extraction")
        )

        if not isinstance(
            new_aggregated_extraction,
            AggregatedExtractionResult,
        ):
            raise MonitoringPipelineError(
                "New monitoring extraction has an "
                "invalid structure."
            )

        # ====================================================
        # 5. LOAD AUTHORITATIVE APPROVED EXTRACTION
        # ====================================================

        old_aggregated_extraction = (
            _get_latest_approved_extraction(
                notification_id=notification_id,
                db=db,
            )
        )

        # ====================================================
        # 6. DETERMINISTIC STRUCTURAL COMPARISON
        # ====================================================

        structural_report = (
            detect_structural_changes(
                approved_extraction=(
                    old_aggregated_extraction.extraction
                ),
                new_extraction=(
                    new_aggregated_extraction.extraction
                ),
            )
        )

        # ====================================================
        # 7. SAFETY CHECK
        # ====================================================

        if not structural_report.change_detected:
            raise MonitoringPipelineError(
                "Document hash changed but no structural "
                "change was detected."
            )

        # ====================================================
        # 8. SEMANTIC AI ANALYSIS
        # ====================================================

        semantic_analysis = (
            analyze_semantic_changes(
                report=structural_report,
                analyzer=analyzer,
            )
        )

        # ====================================================
        # 9. DETERMINISTIC IMPACT CLASSIFICATION
        # ====================================================

        impact_analysis = (
            classify_change_impacts(
                structural_report=structural_report,
                semantic_analysis=semantic_analysis,
            )
        )

        # ====================================================
        # 10. CREATE HITL REVIEW
        # ====================================================

        review_id = create_monitoring_review(
            notification_id=notification_id,
            old_document_hash=(
                monitoring_result[
                    "previous_hash"
                ]
            ),
            new_document_hash=new_document_hash,
            old_extraction=old_aggregated_extraction,
            new_extraction=new_aggregated_extraction,
            structural_report=structural_report,
            semantic_analysis=semantic_analysis,
            impact_analysis=impact_analysis,
            db=db,
        )

        # ====================================================
        # 11. COMMIT ONLY THE REVIEW CREATION
        # ====================================================

        if owns_session:
            db.commit()

        # ====================================================
        # 12. RETURN
        # ====================================================

        return {
            "notification_id": notification_id,
            "status": "REVIEW_CREATED",
            "changed": True,
            "review_id": review_id,
            "previous_hash": (
                monitoring_result[
                    "previous_hash"
                ]
            ),
            "current_hash": new_document_hash,
            "change_count": (
                structural_report.change_count
            ),
            "requires_human_review": (
                impact_analysis
                .overall_requires_human_review
            ),
            "requires_eligibility_re_evaluation": (
                impact_analysis
                .overall_requires_eligibility_re_evaluation
            ),
        }

    except MonitoringPipelineError:
        if owns_session:
            db.rollback()

        raise

    except Exception as error:
        if owns_session:
            db.rollback()

        raise MonitoringPipelineError(
            "Monitoring pipeline failed safely."
        ) from error

    finally:
        if owns_session:
            db.close()