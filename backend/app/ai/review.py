from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.extraction_history import ExtractionHistory

from app.ai.llm_client import extract_exam_information
from app.ai.validation import validate_exam_information

from app.services.exam_discovery_service import (
    fetch_website,
    is_pdf,
    download_pdf,
    extract_pdf_text,
    crawl_exam_sources,
)


def create_pending_extraction(
    notification_id,
    source_pdf_path,
    extracted_content,
    ai_summary
):
    db = SessionLocal()

    extraction = ExtractionHistory(
        notification_id=notification_id,
        extraction_type="EXAM_INFORMATION",
        source_pdf_path=source_pdf_path,
        extracted_content=extracted_content,
        ai_summary=ai_summary,
        change_detected=False,
        change_details=None,
        extraction_status="PENDING",
        created_at=datetime.now()
    )

    db.add(extraction)
    db.commit()
    db.refresh(extraction)

    db.close()

    return extraction


def approve_extraction(extraction_id):
    db = SessionLocal()

    extraction = db.get(
        ExtractionHistory,
        extraction_id
    )

    if extraction is None:
        db.close()
        raise ValueError("Extraction not found.")

    extraction.extraction_status = "APPROVED"

    notification = db.get(
        OfficialNotification,
        extraction.notification_id
    )

    if notification is None:
        db.close()
        raise ValueError("Official notification not found.")

    notification.approval_status = "APPROVED"

    db.commit()
    db.refresh(extraction)

    db.close()

    return extraction


def reject_extraction(extraction_id, feedback):
    db = SessionLocal()

    extraction = db.get(
        ExtractionHistory,
        extraction_id
    )

    if extraction is None:
        db.close()
        raise ValueError("Extraction not found.")

    extraction.extraction_status = "REJECTED"
    extraction.change_details = feedback

    notification = db.get(
        OfficialNotification,
        extraction.notification_id
    )

    if notification is None:
        db.close()
        raise ValueError("Official notification not found.")

    notification.approval_status = "REJECTED"
    notification.rejection_reason = feedback

    db.commit()
    db.refresh(extraction)

    db.close()

    return extraction


def load_original_document(
    extraction,
    notification
):
    """
    Retrieve the original official document.

    First try an existing local PDF path.
    If it does not exist, retrieve the document from
    the official source.
    """

    # --------------------------------------------------
    # 1. Try the extraction's stored PDF path
    # --------------------------------------------------

    extraction_path = Path(
        extraction.source_pdf_path
    )

    if extraction_path.is_file():
        with open(
            extraction_path,
            "rb"
        ) as file:
            pdf_content = file.read()

        return extract_pdf_text(pdf_content)


    # --------------------------------------------------
    # 2. Try the notification's stored PDF path
    # --------------------------------------------------

    notification_path = Path(
        notification.pdf_path
    )

    if notification_path.is_file():
        with open(
            notification_path,
            "rb"
        ) as file:
            pdf_content = file.read()

        return extract_pdf_text(pdf_content)


    # --------------------------------------------------
    # 3. Try the official URL directly
    # --------------------------------------------------

    official_url = notification.official_url

    if not official_url:
        raise ValueError(
            "No official URL is available."
        )

    response, content_type = fetch_website(
        official_url
    )

    if is_pdf(
        content_type,
        official_url
    ):
        pdf_content = download_pdf(
            official_url
        )

        return extract_pdf_text(
            pdf_content
        )


    # --------------------------------------------------
    # 4. Official URL is a webpage.
    #    Crawl it and look for the original PDF.
    # --------------------------------------------------

    discovered_sources = crawl_exam_sources(
        official_url
    )

    stored_filename = Path(
        notification.pdf_path
    ).name

    for source in discovered_sources:

        source_url = source.get("url")

        if not source_url:
            continue

        source_filename = Path(
            urlparse(source_url).path
        ).name

        if (
            stored_filename
            and source_filename == stored_filename
            and source.get("text")
        ):
            return source["text"]


    raise ValueError(
        "Original PDF could not be located."
    )


def retry_extraction(extraction_id):
    db = SessionLocal()

    # --------------------------------------------------
    # Find rejected extraction
    # --------------------------------------------------

    extraction = db.get(
        ExtractionHistory,
        extraction_id
    )

    if extraction is None:
        db.close()
        raise ValueError(
            "Extraction not found."
        )

    if extraction.extraction_status != "REJECTED":
        db.close()
        raise ValueError(
            "Only rejected extractions can be retried."
        )


    # --------------------------------------------------
    # Find related notification
    # --------------------------------------------------

    notification = db.get(
        OfficialNotification,
        extraction.notification_id
    )

    if notification is None:
        db.close()
        raise ValueError(
            "Official notification not found."
        )


    # --------------------------------------------------
    # Get admin feedback
    # --------------------------------------------------

    feedback = extraction.change_details

    if not feedback:
        db.close()
        raise ValueError(
            "No rejection feedback found."
        )

    db.close()


    # --------------------------------------------------
    # Retrieve ORIGINAL document
    # --------------------------------------------------

    original_document = load_original_document(
        extraction,
        notification
    )


    # --------------------------------------------------
    # Ask Gemini to extract again
    # --------------------------------------------------

    retry_prompt = f"""
The previous AI extraction from this official
exam document was rejected by an administrator.

Administrator feedback:
{feedback}

Re-examine the ORIGINAL official document carefully.

Correct the previous extraction according to the
administrator's feedback.

Rules:
- Use only information explicitly present in
  the original document.
- Do not invent or assume information.
- Pay particular attention to the administrator's
  feedback.
- Return the information using the required
  structured format.

ORIGINAL OFFICIAL DOCUMENT:

{original_document}
"""


    exam = extract_exam_information(
        retry_prompt
    )


    # --------------------------------------------------
    # Validate the new extraction
    # --------------------------------------------------

    errors = validate_exam_information(
        exam
    )

    if errors:
        raise ValueError(
            f"Retry extraction failed validation: {errors}"
        )


    # --------------------------------------------------
    # Create NEW extraction history record
    # --------------------------------------------------

    db = SessionLocal()

    new_extraction = ExtractionHistory(
        notification_id=extraction.notification_id,
        extraction_type="RETRY_EXTRACTION",
        source_pdf_path=extraction.source_pdf_path,
        extracted_content=exam.model_dump_json(),
        ai_summary=(
            "Retry extraction generated after "
            "admin feedback."
        ),
        change_detected=False,
        change_details=None,
        extraction_status="PENDING",
        created_at=datetime.now()
    )

    db.add(new_extraction)

    db.commit()

    db.refresh(
        new_extraction
    )

    db.close()

    return new_extraction