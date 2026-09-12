from datetime import date

from app.services.exam_discovery_service import crawl_exam_sources
from app.services.official_notification_service import off_not
from app.services.extraction_history_service import create_extraction_history
from app.ai.llm_client import extract_exam_information
from app.ai.validation import validate_exam_information
from app.ai.source_verification import verify_exam_source


def parse_date(value):
    if not value:
        return None

    return date.fromisoformat(value)


def process_exam(
    exam_id,
    exam_name,
    official_url,
    known_source=None
):
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

    verification = verify_exam_source(
        exam_name,
        pdf_sources
    )

    if not verification.relevant:
        raise ValueError(
            "No relevant official source was found."
        )

    selected_source = next(
        (
            source
            for source in pdf_sources
            if source["url"] == verification.selected_url
        ),
        None
    )

    if selected_source is None:
        raise ValueError(
            "AI selected a source that was not found "
            "among the discovered sources."
        )

    pdf_path = selected_source["pdf_path"]
    document_text = selected_source["text"]

    exam_information = extract_exam_information(
        document_text
    )

    validation_errors = validate_exam_information(
        exam_information
    )

    if validation_errors:
        raise ValueError(
            validation_errors
        )

    application_start_date = parse_date(
        exam_information.application_start_date
    )

    application_end_date = parse_date(
        exam_information.application_end_date
    )

    exam_dates = [
    {
        "start_date": parse_date(
            exam_date.start_date
        ),
        "end_date": parse_date(
            exam_date.end_date
        )
    }
    for exam_date in exam_information.exam_dates
    ]

    release_date = parse_date(
        exam_information.release_date
    )

    notification_id = off_not(
        exam_id=exam_id,
        title=exam_information.exam_name or exam_name,
        notification_type="EXAM_NOTIFICATION",
        release_date=release_date,
        application_start_date=application_start_date,
        application_end_date=application_end_date,
        exam_dates=exam_dates,
        official_url=selected_source["url"],
        pdf_path=pdf_path,
        ai_summary=exam_information.model_dump_json(),
        ai_change_summary=None,
        approval_status="PENDING",
        rejection_reason=None 
    )

    extraction_id = create_extraction_history(
        notification_id=notification_id,
        extraction_type="EXAM_INFORMATION",
        source_pdf_path=pdf_path,
        extracted_content=exam_information.model_dump_json(),
        ai_summary=exam_information.model_dump_json(),
        change_detected=False,
        change_details=None,
        extraction_status="PENDING"
    )

    return {
        "notification_id": notification_id,
        "extraction_id": extraction_id,
        "pdf_path": pdf_path,
        "selected_source": selected_source["url"],
        "source_type": verification.source_type,
        "status": "PENDING"
    }