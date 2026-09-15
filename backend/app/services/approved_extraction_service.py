from __future__ import annotations

from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
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
from app.database.session import SessionLocal
from app.models.eligibility_rule import EligibilityRule
from app.models.eligibility_rule_group import (
    EligibilityRuleGroup,
)
from app.models.exam_date import ExamDate
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification
from app.services.eligibility_rule_service import (
    _create_rule_group_recursive,
)


def _parse_date(
    value: str | None,
) -> date | None:
    """
    Convert an ISO date string into a Python date.

    None remains None.
    Invalid ISO dates raise ValueError.
    """

    if value is None:
        return None

    return date.fromisoformat(value)


def _get_locked_extraction(
    session: Session,
    extraction_id: int,
) -> ExtractionHistory:
    """
    Load the extraction and lock its row for this transaction.
    """

    extraction = session.scalar(
        select(ExtractionHistory)
        .where(
            ExtractionHistory.extraction_id
            == extraction_id
        )
        .with_for_update()
    )

    if extraction is None:
        raise ValueError(
            "Extraction not found."
        )

    return extraction


def _get_locked_notification(
    session: Session,
    notification_id: int,
) -> OfficialNotification:
    """
    Load the notification and lock its row.

    Locking the notification gives us a stable parent row
    while checking which extraction version is latest.
    """

    notification = session.scalar(
        select(OfficialNotification)
        .where(
            OfficialNotification.notification_id
            == notification_id
        )
        .with_for_update()
    )

    if notification is None:
        raise ValueError(
            "Official notification not found."
        )

    return notification


def _ensure_latest_extraction(
    session: Session,
    extraction: ExtractionHistory,
) -> None:
    """
    Ensure that the extraction being approved is the
    newest extraction for its notification.

    The newest extraction is determined by the highest
    extraction_id.

    An older extraction must never be approved.
    """

    latest_extraction_id = session.scalar(
        select(
            ExtractionHistory.extraction_id
        )
        .where(
            ExtractionHistory.notification_id
            == extraction.notification_id
        )
        .order_by(
            ExtractionHistory.extraction_id.desc()
        )
        .limit(1)
    )

    if latest_extraction_id is None:
        raise ValueError(
            "No extraction history found for notification."
        )

    if (
        latest_extraction_id
        != extraction.extraction_id
    ):
        raise ValueError(
            "This extraction is no longer the latest "
            "extraction for the notification."
        )


def _delete_existing_eligibility_tree(
    session: Session,
    notification_id: int,
) -> None:
    """
    Delete the existing eligibility-rule tree for a
    notification.

    Rules are deleted before groups because rules reference
    their groups.
    """

    group_ids = session.scalars(
        select(EligibilityRuleGroup.group_id)
        .where(
            EligibilityRuleGroup.notification_id
            == notification_id
        )
    ).all()

    if not group_ids:
        return

    session.execute(
        delete(EligibilityRule).where(
            EligibilityRule.group_id.in_(
                group_ids
            )
        )
    )

    session.execute(
        delete(EligibilityRuleGroup).where(
            EligibilityRuleGroup.group_id.in_(
                group_ids
            )
        )
    )

    session.flush()


def _replace_exam_dates(
    session: Session,
    notification: OfficialNotification,
    extraction_result: AggregatedExtractionResult,
) -> None:
    """
    Replace the notification's existing exam dates with
    the approved extraction's exam dates.
    """

    notification.exam_dates.clear()

    session.flush()

    exam_dates = (
        extraction_result
        .extraction
        .exam_information
        .exam_dates
    )

    for exam_date_data in exam_dates:
        start_date = _parse_date(
            exam_date_data.start_date
        )

        end_date = _parse_date(
            exam_date_data.end_date
        )

        if start_date is None:
            raise ValueError(
                "Exam date range cannot contain "
                "a null start date."
            )

        if end_date is None:
            raise ValueError(
                "Exam date range cannot contain "
                "a null end date."
            )

        exam_date = ExamDate(
            start_date=start_date,
            end_date=end_date,
        )

        notification.exam_dates.append(
            exam_date
        )

    session.flush()


def _persist_eligibility_tree(
    session: Session,
    notification_id: int,
    extraction_result: AggregatedExtractionResult,
) -> None:
    """
    Replace the notification's existing eligibility tree
    with the recursively extracted tree.
    """

    _delete_existing_eligibility_tree(
        session=session,
        notification_id=notification_id,
    )

    rule_groups = (
        extraction_result
        .extraction
        .eligibility_rules
        .rule_groups
    )

    for group_number, group_data in enumerate(
        rule_groups,
        start=1,
    ):
        _create_rule_group_recursive(
            session=session,
            notification_id=notification_id,
            group_data=group_data,
            group_number=group_number,
            parent_group_id=None,
        )

    session.flush()


def persist_approved_extraction(
    session: Session,
    extraction_history: ExtractionHistory,
    extraction_result: AggregatedExtractionResult,
) -> None:
    """
    Persist a validated extraction into the authoritative
    notification and eligibility tables.

    This function assumes validation has already succeeded.
    """

    notification = _get_locked_notification(
        session=session,
        notification_id=(
            extraction_history.notification_id
        ),
    )

    exam_information = (
        extraction_result
        .extraction
        .exam_information
    )

    notification.release_date = _parse_date(
        exam_information.release_date
    )

    notification.application_start_date = (
        _parse_date(
            exam_information.application_start_date
        )
    )

    notification.application_end_date = (
        _parse_date(
            exam_information.application_end_date
        )
    )

    notification.ai_summary = (
        extraction_history.ai_summary
    )

    notification.approval_status = "APPROVED"

    notification.rejection_reason = None

    _replace_exam_dates(
        session=session,
        notification=notification,
        extraction_result=extraction_result,
    )

    _persist_eligibility_tree(
        session=session,
        notification_id=(
            notification.notification_id
        ),
        extraction_result=extraction_result,
    )

    extraction_history.extraction_status = (
        "APPROVED"
    )

    session.flush()


def approve_extraction_with_session(
    session: Session,
    extraction_id: int,
) -> ExtractionHistory:
    """
    Approve an extraction inside an existing transaction.

    Order:

        1. Load and lock extraction.
        2. Ensure extraction is PENDING.
        3. Lock its notification.
        4. Verify this extraction is latest.
        5. Deserialize extraction.
        6. Normalize extraction.
        7. Validate normalized extraction.
        8. Persist approved data.
        9. Return without committing.

    The caller owns the transaction commit/rollback.
    """

    # ---------------------------------------------------------
    # 1. Lock extraction
    # ---------------------------------------------------------

    extraction = _get_locked_extraction(
        session=session,
        extraction_id=extraction_id,
    )

    # ---------------------------------------------------------
    # 2. Only PENDING extractions may be approved
    # ---------------------------------------------------------

    if extraction.extraction_status != "PENDING":
        raise ValueError(
            "Only pending extractions can be approved."
        )

    # ---------------------------------------------------------
    # 3. Lock the parent notification
    # ---------------------------------------------------------

    _get_locked_notification(
        session=session,
        notification_id=extraction.notification_id,
    )

    # ---------------------------------------------------------
    # 4. Verify this is still the latest extraction
    # ---------------------------------------------------------

    _ensure_latest_extraction(
        session=session,
        extraction=extraction,
    )

    # ---------------------------------------------------------
    # 5. Extraction content must exist
    # ---------------------------------------------------------

    if not extraction.extracted_content:
        raise ValueError(
            "Extraction content is empty."
        )

    # ---------------------------------------------------------
    # 6. Deserialize
    # ---------------------------------------------------------

    extraction_result = (
        deserialize_aggregated_extraction(
            extraction.extracted_content
        )
    )

    # ---------------------------------------------------------
    # 7. Normalize ONLY the CompleteExtractionData
    # ---------------------------------------------------------

    normalized_extraction = (
        normalize_complete_extraction(
            extraction_result.extraction
        )
    )

    # Preserve the evidence/provenance while replacing
    # the extraction with its normalized representation.
    normalized_result = AggregatedExtractionResult(
        extraction=normalized_extraction,
        evidence=extraction_result.evidence,
    )

    # ---------------------------------------------------------
    # 8. Validate normalized extraction
    # ---------------------------------------------------------

    validation_errors = (
        validate_complete_extraction(
            normalized_extraction
        )
    )

    if validation_errors:
        raise ValueError(
            "Extraction failed validation: "
            f"{validation_errors}"
        )

    # ---------------------------------------------------------
    # 9. Persist ONLY after all validation succeeds
    # ---------------------------------------------------------

    persist_approved_extraction(
        session=session,
        extraction_history=extraction,
        extraction_result=normalized_result,
    )

    return extraction


def approve_extraction_transaction(
    extraction_id: int,
) -> ExtractionHistory:
    """
    Public transaction boundary for approving an extraction.

    A successful approval commits all changes atomically.

    Any failure rolls back everything performed during
    this approval transaction.
    """

    with SessionLocal() as session:
        try:
            extraction = approve_extraction_with_session(
                session=session,
                extraction_id=extraction_id,
            )

            session.commit()

            session.refresh(extraction)

            return extraction

        except Exception:
            session.rollback()
            raise