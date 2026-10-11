from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.extraction_history import ExtractionHistory


def _text(value) -> str | None:
    value = (str(value).strip() if value is not None else "")

    return value or None


def get_eligibility_info(
    notification_id: int,
    db: Session | None = None,
) -> dict | None:
    """
    The eligibility summary an administrator approved for a notification
    (age, qualification, nationality, other requirements), for display to
    students next to their eligibility result.

    Read from the newest APPROVED extraction, so it is exactly what the
    administrator reviewed. Returns None when there is nothing to show.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        content = db.scalar(
            select(ExtractionHistory.extracted_content)
            .where(
                ExtractionHistory.notification_id == notification_id,
                ExtractionHistory.extraction_status == "APPROVED",
            )
            .order_by(ExtractionHistory.extraction_id.desc())
            .limit(1)
        )

    finally:
        if owns_session:
            db.close()

    if not content:
        return None

    try:
        data = json.loads(content)
    except ValueError:
        return None

    eligibility = (
        (data.get("extraction") or {})
        .get("exam_information", {})
        .get("eligibility")
        or {}
    )

    pipeline = data.get("pipeline") or {}

    other = [
        text
        for text in (_text(item) for item in eligibility.get("other_requirements") or [])
        if text
    ]

    info = {
        "minimum_age": eligibility.get("minimum_age"),
        "maximum_age": eligibility.get("maximum_age"),
        "educational_qualification": _text(
            eligibility.get("educational_qualification")
        ),
        "nationality": _text(eligibility.get("nationality")),
        "work_experience": _text(eligibility.get("work_experience")),
        "other_requirements": other,
        "source": (
            "ADMIN"
            if pipeline.get("eligibility_source") == "ADMIN"
            else "AI"
        ),
        "not_available": bool(pipeline.get("eligibility_not_available")),
    }

    has_content = (
        info["not_available"]
        or any(
            info[key] is not None
            for key in (
                "minimum_age",
                "maximum_age",
                "educational_qualification",
                "nationality",
                "work_experience",
            )
        )
        or bool(info["other_requirements"])
    )

    return info if has_content else None
