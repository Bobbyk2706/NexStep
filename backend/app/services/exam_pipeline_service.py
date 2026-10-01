from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.ai.extraction.pipeline import (
    ensure_usable,
    run_extraction,
    summarize,
)
from app.ai.extraction_serialization import (
    serialize_aggregated_extraction,
)
from app.ai.source_verification import (
    verify_exam_source,
)
from app.database.session import SessionLocal
from app.services.exam_discovery_service import (
    crawl_exam_sources,
)
from app.services.extraction_history_service import (
    create_extraction_history,
)
from app.services.official_notification_service import (
    off_not,
)


def parse_date(value):
    if not value:
        return None

    return date.fromisoformat(value)


def process_exam(
    exam_id,
    exam_name,
    official_url,
    known_source=None,
):
    # ========================================================
    # 1. SOURCE DISCOVERY
    # ========================================================

    if known_source is not None:
        pdf_sources = [known_source]

    else:
        sources = crawl_exam_sources(
            official_url
        )

        pdf_sources = [
            source
            for source in sources
            if source.get("pdf_path")
        ]

        if not pdf_sources:
            raise ValueError(
                "No valid PDF source was found."
            )

    # ========================================================
    # 2. SOURCE VERIFICATION
    # ========================================================

    verification = verify_exam_source(
        exam_name,
        pdf_sources,
    )

    if not verification.relevant:
        raise ValueError(
            "No relevant official source was found."
        )

    selected_source = next(
        (
            source
            for source in pdf_sources
            if source["url"]
            == verification.selected_url
        ),
        None,
    )

    if selected_source is None:
        raise ValueError(
            "AI selected a source that was not found "
            "among the discovered sources."
        )

    # ========================================================
    # 3. REQUIRED DOCUMENT ARTIFACTS
    # ========================================================

    pdf_path = selected_source.get(
        "pdf_path"
    )

    document_url = selected_source.get(
        "document_url",
        selected_source.get("url"),
    )

    document_hash = selected_source.get(
        "document_hash"
    )

    pdf_content = selected_source.get(
        "content"
    )

    if not pdf_path:
        raise ValueError(
            "Selected source has no PDF path."
        )

    if not document_url:
        raise ValueError(
            "Selected source has no document URL."
        )

    if not document_hash:
        raise ValueError(
            "Selected source has no document hash."
        )

    if not pdf_content:
        raise ValueError(
            "Selected source has no PDF content."
        )

    # ========================================================
    # 4-9. AI EXTRACTION (pipeline v2)
    # ========================================================
    #
    # parse -> passages -> targeted retrieval -> LLM facts
    #       -> grounding in the source -> rule compilation
    #       -> normalization -> validation
    #
    # Problems found on the way are recorded as issues on the
    # result and shown to the reviewer, instead of aborting.

    try:
        normalized_result = run_extraction(
            pdf_content,
            exam_name_hint=exam_name,
            source_url=document_url,
            document_hash=document_hash,
        )
        ensure_usable(normalized_result)

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            f"AI extraction failed: {error}"
        ) from error

    # ========================================================
    # 10. EXAM INFORMATION
    # ========================================================

    exam_information = (
        normalized_result
        .extraction
        .exam_information
    )

    # ========================================================
    # 11 + 12. ATOMIC DATABASE TRANSACTION
    # ========================================================
    #
    # Notification and extraction history are created
    # inside ONE transaction.
    #
    # If either operation fails:
    #     notification -> rolled back
    #     extraction   -> rolled back
    #
    # Nothing is persisted partially.
    # ========================================================

    with SessionLocal() as db:
        try:
            # ------------------------------------------------
            # Create pending notification
            # ------------------------------------------------

            notification_id = off_not(
                exam_id=exam_id,
                title=(
                    exam_information.exam_name
                    or exam_name
                ),
                notification_type="EXAM_NOTIFICATION",
                release_date=parse_date(
                    exam_information.release_date
                ),
                application_start_date=parse_date(
                    exam_information.application_start_date
                ),
                application_end_date=parse_date(
                    exam_information.application_end_date
                ),
                exam_dates=[
                    {
                        "start_date": parse_date(
                            exam_date.start_date
                        ),
                        "end_date": parse_date(
                            exam_date.end_date
                        ),
                    }
                    for exam_date
                    in exam_information.exam_dates
                ],
                official_url=official_url,
                document_url=document_url,
                pdf_path=pdf_path,
                document_hash=document_hash,
                ai_summary=None,
                ai_change_summary=None,
                approval_status="PENDING",
                rejection_reason=None,
                db=db,
            )

            # ------------------------------------------------
            # Create extraction history
            # ------------------------------------------------

            extraction_id = (
                create_extraction_history(
                    notification_id=notification_id,
                    extraction_type="COMPLETE_EXTRACTION",
                    source_pdf_path=pdf_path,
                    extracted_content=(
                        serialize_aggregated_extraction(
                            normalized_result
                        )
                    ),
                    ai_summary=summarize(normalized_result),
                    change_detected=False,
                    change_details=None,
                    extraction_status="PENDING",
                    db=db,
                )
            )

            # ------------------------------------------------
            # Commit BOTH records together
            # ------------------------------------------------

            db.commit()

        except Exception:
            db.rollback()
            raise

    # ========================================================
    # 13. RETURN
    # ========================================================

    return {
        "notification_id": notification_id,
        "extraction_id": extraction_id,
        "pdf_path": pdf_path,
        "document_url": document_url,
        "document_hash": document_hash,
        "selected_source": selected_source["url"],
        "source_type": verification.source_type,
        "status": "PENDING",
    }