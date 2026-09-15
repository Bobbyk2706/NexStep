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
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.exam_date import ExamDate
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification
from app.services.eligibility_rule_service import (
    _create_rule_group_recursive,
)


PENDING_STATUS = "PENDING"
APPROVED_STATUS = "APPROVED"


def _parse_date(
    value: str | None,
) -> date | None:
    """
    Convert a normalized YYYY-MM-DD string into a
    Python date object.

    None remains None.
    """

    if value is None:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid date value: {value}"
        ) from exc


def _delete_existing_eligibility_tree(
    session: Session,
    notification_id: int,
) -> None:
    """
    Delete the existing eligibility tree belonging to
    a notification.

    Rules are deleted first.

    Groups are then deleted from deepest/child groups
    toward root groups so the self-referencing
    parent_group_id foreign key is never violated.

    The caller owns the transaction.
    """

    groups = session.scalars(
        select(EligibilityRuleGroup).where(
            EligibilityRuleGroup.notification_id
            == notification_id
        )
    ).all()

    if not groups:
        return

    group_ids = {
        group.group_id
        for group in groups
    }

    # ---------------------------------------------------------
    # DELETE RULES FIRST
    # ---------------------------------------------------------

    session.execute(
        delete(EligibilityRule).where(
            EligibilityRule.group_id.in_(group_ids)
        )
    )

    session.flush()

    # ---------------------------------------------------------
    # BUILD CHILD-FIRST DELETE ORDER
    # ---------------------------------------------------------

    children_by_parent: dict[
        int | None,
        list[EligibilityRuleGroup],
    ] = {}

    for group in groups:
        children_by_parent.setdefault(
            group.parent_group_id,
            [],
        ).append(group)

    ordered_groups: list[EligibilityRuleGroup] = []

    def collect_children(
        parent_group_id: int | None,
    ) -> None:
        for group in children_by_parent.get(
            parent_group_id,
            [],
        ):
            collect_children(group.group_id)
            ordered_groups.append(group)

    collect_children(None)

    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------

    if len(ordered_groups) != len(groups):
        raise ValueError(
            "Eligibility rule group tree is invalid: "
            "unable to determine a complete hierarchy."
        )

    # ---------------------------------------------------------
    # DELETE CHILD GROUPS BEFORE PARENTS
    # ---------------------------------------------------------

    for group in ordered_groups:
        session.delete(group)

    session.flush()


def _replace_exam_dates(
    session: Session,
    notification: OfficialNotification,
    extraction_result: AggregatedExtractionResult,
) -> None:
    """
    Replace the authoritative examination dates with
    the dates from the approved extraction.

    The caller owns the transaction.
    """

    # ---------------------------------------------------------
    # REMOVE EXISTING DATES
    # ---------------------------------------------------------

    notification.exam_dates.clear()

    session.flush()

    # ---------------------------------------------------------
    # ADD APPROVED DATES
    # ---------------------------------------------------------

    for exam_date_data in (
        extraction_result.extraction
        .exam_information
        .exam_dates
    ):
        start_date = _parse_date(
            exam_date_data.start_date
        )

        end_date = _parse_date(
            exam_date_data.end_date
        )

        if start_date is None or end_date is None:
            raise ValueError(
                "Exam date range cannot contain null dates."
            )

        if start_date > end_date:
            raise ValueError(
                "Exam date range start_date cannot be "
                "after end_date."
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
    Replace the authoritative eligibility tree with
    the approved extraction's recursive tree.

    The logical structure is preserved exactly.
    """

    _delete_existing_eligibility_tree(
        session=session,
        notification_id=notification_id,
    )

    for group_number, group_data in enumerate(
        extraction_result.extraction
        .eligibility_rules
        .rule_groups,
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
    database structures.

    IMPORTANT:

    This function does NOT commit.

    The caller owns the transaction.
    """

    notification = session.get(
        OfficialNotification,
        extraction_history.notification_id,
    )

    if notification is None:
        raise ValueError(
            "Official notification not found."
        )

    exam_information = (
        extraction_result.extraction.exam_information
    )

    # ---------------------------------------------------------
    # UPDATE NOTIFICATION INFORMATION
    # ---------------------------------------------------------

    notification.release_date = _parse_date(
        exam_information.release_date
    )

    notification.application_start_date = _parse_date(
        exam_information.application_start_date
    )

    notification.application_end_date = _parse_date(
        exam_information.application_end_date
    )

    notification.ai_summary = (
        extraction_history.ai_summary
    )

    notification.approval_status = APPROVED_STATUS

    notification.rejection_reason = None

    # ---------------------------------------------------------
    # REPLACE EXAM DATES
    # ---------------------------------------------------------

    _replace_exam_dates(
        session=session,
        notification=notification,
        extraction_result=extraction_result,
    )

    # ---------------------------------------------------------
    # REPLACE ELIGIBILITY TREE
    # ---------------------------------------------------------

    _persist_eligibility_tree(
        session=session,
        notification_id=notification.notification_id,
        extraction_result=extraction_result,
    )

    # ---------------------------------------------------------
    # MARK EXTRACTION APPROVED
    # ---------------------------------------------------------

    extraction_history.extraction_status = (
        APPROVED_STATUS
    )

    session.flush()


def approve_extraction_with_session(
    session: Session,
    extraction_id: int,
) -> ExtractionHistory:
    """
    Approve one pending extraction using the supplied
    SQLAlchemy session.

    This function does NOT commit.

    The caller owns the transaction.

    This design makes the operation both:
    - transaction-safe in production
    - directly testable
    """

    # ---------------------------------------------------------
    # LOAD EXTRACTION WITH ROW LOCK
    # ---------------------------------------------------------

    extraction_history = session.scalar(
        select(ExtractionHistory)
        .where(
            ExtractionHistory.extraction_id
            == extraction_id
        )
        .with_for_update()
    )

    if extraction_history is None:
        raise ValueError(
            "Extraction not found."
        )

    # ---------------------------------------------------------
    # VERIFY EXTRACTION STATUS
    # ---------------------------------------------------------

    if (
        extraction_history.extraction_status
        != PENDING_STATUS
    ):
        raise ValueError(
            "Only pending extractions can be approved."
        )

    # ---------------------------------------------------------
    # VERIFY EXTRACTION CONTENT
    # ---------------------------------------------------------

    if not extraction_history.extracted_content:
        raise ValueError(
            "Extraction content is empty."
        )

    # ---------------------------------------------------------
    # LOAD AND DESERIALIZE EXTRACTION
    # ---------------------------------------------------------

    extraction_result = (
        deserialize_aggregated_extraction(
            extraction_history.extracted_content
        )
    )

    # ---------------------------------------------------------
    # NORMALIZE
    # ---------------------------------------------------------

    normalized_extraction = (
        normalize_complete_extraction(
            extraction_result.extraction
        )
    )

    normalized_result = AggregatedExtractionResult(
        extraction=normalized_extraction,
        evidence=extraction_result.evidence,
    )

    # ---------------------------------------------------------
    # VALIDATE
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
    # LOCK RELATED NOTIFICATION
    # ---------------------------------------------------------

    notification = session.scalar(
        select(OfficialNotification)
        .where(
            OfficialNotification.notification_id
            == extraction_history.notification_id
        )
        .with_for_update()
    )

    if notification is None:
        raise ValueError(
            "Official notification not found."
        )

    # ---------------------------------------------------------
    # PERSIST APPROVED DATA
    # ---------------------------------------------------------

    persist_approved_extraction(
        session=session,
        extraction_history=extraction_history,
        extraction_result=normalized_result,
    )

    return extraction_history


def approve_extraction_transaction(
    extraction_id: int,
) -> ExtractionHistory:
    """
    Production entry point for approving an extraction.

    Creates one database session and one transaction.

    On success:
        COMMIT

    On failure:
        ROLLBACK
    """

    with SessionLocal() as session:

        try:
            extraction_history = (
                approve_extraction_with_session(
                    session=session,
                    extraction_id=extraction_id,
                )
            )

            session.commit()

            session.refresh(
                extraction_history
            )

            return extraction_history

        except Exception:
            session.rollback()
            raise
def _ensure_latest_extraction(
    session,
    extraction,
):
    session.flush()

    latest_extraction_id = session.scalar(
        select(ExtractionHistory.extraction_id)
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

    if latest_extraction_id != extraction.extraction_id:
        raise ValueError(
            "This extraction is no longer the latest "
            "extraction for the notification."
        )