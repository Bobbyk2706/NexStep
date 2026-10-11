from __future__ import annotations

import json
import logging

from sqlalchemy import select

from app.ai.extraction.pipeline import summarize
from app.ai.extraction_serialization import (
    deserialize_aggregated_extraction,
    serialize_aggregated_extraction,
)
from app.ai.manual_eligibility import (
    ManualEligibility,
    apply_manual_eligibility,
)
from app.database.session import SessionLocal
from app.models.extraction_history import ExtractionHistory
from app.services.approved_extraction_service import (
    _ensure_latest_extraction,
)
from app.services.audit_log_service import create_audit_log

logger = logging.getLogger(__name__)


def save_extraction_eligibility(
    extraction_id: int,
    manual: ManualEligibility,
    admin_id: int | None = None,
) -> dict:
    """
    Store administrator-entered eligibility on a PENDING extraction.

    Only the newest extraction of a notification can be edited, the same
    rule approval applies. The stored extraction is replaced in place; the
    administrator then approves it as usual.

    Raises ValueError (not found / not editable) or ManualEligibilityError
    (invalid eligibility).
    """

    with SessionLocal() as session:
        try:
            extraction = session.scalar(
                select(ExtractionHistory)
                .where(ExtractionHistory.extraction_id == extraction_id)
                .with_for_update()
            )

            if extraction is None:
                raise ValueError("Extraction not found.")

            if extraction.extraction_status != "PENDING":
                raise ValueError(
                    "Eligibility can only be edited while the extraction "
                    "is pending review."
                )

            _ensure_latest_extraction(session, extraction)

            if not extraction.extracted_content:
                raise ValueError("Extraction content is empty.")

            previous = deserialize_aggregated_extraction(
                extraction.extracted_content
            )

            updated = apply_manual_eligibility(previous, manual)

            extraction.extracted_content = serialize_aggregated_extraction(
                updated
            )

            extraction.ai_summary = (
                summarize(updated)
                + " Eligibility entered by an administrator."
            )

            session.commit()

            old_rules = previous.extraction.eligibility_rules.model_dump()
            new_rules = updated.extraction.eligibility_rules.model_dump()

        except Exception:
            session.rollback()
            raise

    # The audit trail is best-effort: a logging problem must not undo the
    # administrator's work.
    try:
        create_audit_log(
            admin_id=admin_id,
            action_type="EDIT_ELIGIBILITY",
            entity_type="ExtractionHistory",
            entity_id=extraction_id,
            description="Administrator entered or edited eligibility.",
            old_value=json.dumps(old_rules, ensure_ascii=False)[:8000],
            new_value=json.dumps(new_rules, ensure_ascii=False)[:8000],
        )
    except Exception:
        logger.exception(
            "Could not write the audit log for extraction %s", extraction_id
        )

    return {
        "extraction_id": extraction_id,
        "eligibility_source": "ADMIN",
        "not_available": manual.not_available,
    }
