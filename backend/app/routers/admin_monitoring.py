from __future__ import annotations

import json
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select

from app.auth.dependencies import (
    get_current_admin,
)
from app.database.session import SessionLocal
from app.models.admin import Admin
from app.models.exam import Exam
from app.models.monitoring_review import (
    MonitoringReview,
)
from app.models.official_notification import (
    OfficialNotification,
)
from app.scheduler.monitoring_scheduler import (
    run_monitoring_cycle_now,
)
from app.services.monitoring_review_service import (
    MonitoringReviewError,
    apply_approved_monitoring_review,
    approve_monitoring_review,
    get_monitoring_review,
    reject_monitoring_review,
)


router = APIRouter(
    prefix="/admin/monitoring",
    tags=["Admin Monitoring"],
)


# ============================================================
# REQUEST MODELS
# ============================================================

class MonitoringRejectionRequest(BaseModel):
    reason: str


# ============================================================
# RUN MONITORING
# ============================================================

@router.post("/run")
def run_monitoring(
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    Run one complete monitoring cycle.

    Only authenticated admins may trigger monitoring.
    """

    try:
        result = run_monitoring_cycle_now()

        return {
            "success": True,
            "message": (
                "Monitoring cycle completed."
            ),
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "Monitoring cycle failed: "
                f"{exc}"
            ),
        ) from exc


# ============================================================
# LIST MONITORING REVIEWS
# ============================================================

@router.get("/reviews")
def list_monitoring_reviews(
    status_filter: str | None = None,
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    List monitoring reviews without returning the huge
    extraction payloads.

    Optional:

        /reviews?status_filter=PENDING
        /reviews?status_filter=APPROVED
        /reviews?status_filter=REJECTED
    """

    db = SessionLocal()

    try:
        query = (
            db.query(
                MonitoringReview,
                OfficialNotification,
                Exam,
            )
            .join(
                OfficialNotification,
                MonitoringReview.notification_id
                == OfficialNotification.notification_id,
            )
            .join(
                Exam,
                OfficialNotification.exam_id
                == Exam.exam_id,
            )
        )

        if status_filter:
            query = query.filter(
                MonitoringReview.review_status
                == status_filter
            )

        rows = (
            query
            .order_by(
                MonitoringReview.created_at.desc()
            )
            .all()
        )

        response = []

        for review, notification, exam in rows:

            change_count = None

            try:
                structural = json.loads(
                    review.structural_changes
                )

                if isinstance(
                    structural,
                    dict,
                ):
                    changes = structural.get(
                        "changes"
                    )

                    if isinstance(
                        changes,
                        list,
                    ):
                        change_count = len(
                            changes
                        )

            except Exception:
                change_count = None

            semantic_summary = None

            try:
                semantic = json.loads(
                    review.semantic_analysis
                )

                if isinstance(
                    semantic,
                    dict,
                ):
                    semantic_summary = semantic.get(
                        "overall_summary"
                    )

            except Exception:
                semantic_summary = None

            impact_summary = None
            requires_eligibility = None
            requires_human_review = None

            try:
                impact = json.loads(
                    review.impact_analysis
                )

                if isinstance(
                    impact,
                    dict,
                ):
                    impact_summary = impact.get(
                        "overall_summary"
                    )

                    requires_eligibility = impact.get(
                        "overall_requires_eligibility_re_evaluation"
                    )

                    requires_human_review = impact.get(
                        "overall_requires_human_review"
                    )

            except Exception:
                pass

            response.append(
                {
                    "review_id": review.review_id,
                    "notification_id": (
                        review.notification_id
                    ),
                    "exam_id": exam.exam_id,
                    "exam_name": exam.name,
                    "notification_title": (
                        notification.title
                    ),
                    "review_status": (
                        review.review_status
                    ),
                    "old_document_hash": (
                        review.old_document_hash
                    ),
                    "new_document_hash": (
                        review.new_document_hash
                    ),
                    "change_count": change_count,
                    "semantic_summary": (
                        semantic_summary
                    ),
                    "impact_summary": (
                        impact_summary
                    ),
                    "requires_human_review": (
                        requires_human_review
                    ),
                    "requires_eligibility_re_evaluation": (
                        requires_eligibility
                    ),
                    "created_at": (
                        review.created_at
                    ),
                    "reviewed_at": (
                        review.reviewed_at
                    ),
                    "rejection_reason": (
                        review.rejection_reason
                    ),
                }
            )

        return response

    finally:
        db.close()


# ============================================================
# GET ONE MONITORING REVIEW
# ============================================================

@router.get("/reviews/{review_id}")
def get_monitoring_review_detail(
    review_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    Return the complete monitoring review.

    This endpoint contains the detailed structural,
    semantic and impact analysis.
    """

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Monitoring review not found."
                ),
            )

        notification = db.get(
            OfficialNotification,
            review.notification_id,
        )

        if notification is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Official notification not found."
                ),
            )

        exam = db.get(
            Exam,
            notification.exam_id,
        )

        if exam is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found.",
            )

        def parse_json(value):
            try:
                return json.loads(value)
            except Exception:
                return value

        return {
            "review_id": review.review_id,
            "review_status": (
                review.review_status
            ),
            "notification_id": (
                review.notification_id
            ),
            "exam_id": exam.exam_id,
            "exam_name": exam.name,
            "notification_title": (
                notification.title
            ),
            "official_url": (
                notification.official_url
            ),
            "document_url": (
                notification.document_url
            ),
            "old_document_hash": (
                review.old_document_hash
            ),
            "new_document_hash": (
                review.new_document_hash
            ),
            "old_extraction": parse_json(
                review.old_extraction
            ),
            "new_extraction": parse_json(
                review.new_extraction
            ),
            "structural_changes": parse_json(
                review.structural_changes
            ),
            "semantic_analysis": parse_json(
                review.semantic_analysis
            ),
            "impact_analysis": parse_json(
                review.impact_analysis
            ),
            "reviewed_by": (
                review.reviewed_by
            ),
            "reviewed_at": (
                review.reviewed_at
            ),
            "created_at": (
                review.created_at
            ),
            "rejection_reason": (
                review.rejection_reason
            ),
        }

    finally:
        db.close()


# ============================================================
# APPROVE
# ============================================================

@router.post(
    "/reviews/{review_id}/approve"
)
def approve_review(
    review_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    Record the administrator's approval.

    This does not publish the change yet.
    """

    try:
        approved_id = (
            approve_monitoring_review(
                review_id=review_id,
                admin_id=current_admin.admin_id,
            )
        )

        return {
            "success": True,
            "review_id": approved_id,
            "status": "APPROVED",
            "message": (
                "Monitoring review approved. "
                "The change can now be published."
            ),
        }

    except MonitoringReviewError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


# ============================================================
# REJECT
# ============================================================

@router.post(
    "/reviews/{review_id}/reject"
)
def reject_review(
    review_id: int,
    request: MonitoringRejectionRequest,
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    Reject a monitoring change.
    """

    reason = request.reason.strip()

    if not reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Rejection reason is required."
            ),
        )

    try:
        rejected_id = (
            reject_monitoring_review(
                review_id=review_id,
                admin_id=current_admin.admin_id,
                rejection_reason=reason,
            )
        )

        return {
            "success": True,
            "review_id": rejected_id,
            "status": "REJECTED",
            "message": (
                "Monitoring review rejected."
            ),
        }

    except MonitoringReviewError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


# ============================================================
# APPLY APPROVED REVIEW
# ============================================================

@router.post(
    "/reviews/{review_id}/apply"
)
def apply_review(
    review_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    Publish an already-approved monitoring change into
    the authoritative exam data.
    """

    try:
        applied_id = (
            apply_approved_monitoring_review(
                review_id=review_id
            )
        )

        return {
            "success": True,
            "review_id": applied_id,
            "status": "APPLIED",
            "message": (
                "Approved monitoring change "
                "published successfully."
            ),
        }

    except MonitoringReviewError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


# ============================================================
# NEW MONITORED PDF
# ============================================================

@router.get(
    "/reviews/{review_id}/document/new"
)
def get_new_monitoring_document(
    review_id: int,
    current_admin: Admin = Depends(
        get_current_admin
    ),
):
    """
    Serve the newly detected monitoring PDF.
    """

    db = SessionLocal()

    try:
        review = db.get(
            MonitoringReview,
            review_id,
        )

        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Monitoring review not found."
                ),
            )

        storage_dir = (
            Path(__file__).resolve().parents[2]
            / "storage"
            / "monitoring"
        )

        pdf_path = (
            storage_dir
            / f"{review.new_document_hash}.pdf"
        )

        if not pdf_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    "Monitored PDF was not found."
                ),
            )

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=(
                f"monitoring-{review.review_id}.pdf"
            ),
        )

    finally:
        db.close()