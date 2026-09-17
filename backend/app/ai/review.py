from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

import pymupdf
from sqlalchemy import select

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
)
from app.ai.chunk_aggregator import (
    aggregate_chunk_extractions,
)
from app.ai.chunk_extractor import (
    extract_chunk_information,
)
from app.ai.complete_extraction_normalizer import (
    normalize_complete_extraction,
)
from app.ai.complete_extraction_validation import (
    validate_complete_extraction,
)
from app.ai.extraction_serialization import (
    deserialize_aggregated_extraction,
    serialize_aggregated_extraction,
)
from app.database.session import SessionLocal
from app.models.extraction_history import ExtractionHistory
from app.models.official_notification import OfficialNotification
from app.services.approved_extraction_service import (
    approve_extraction_transaction,
)
from app.services.document_chunker import (
    chunk_document_pages,
)
from app.services.exam_discovery_service import (
    download_pdf,
)


# ============================================================
# CREATE PENDING EXTRACTION
# ============================================================

def create_pending_extraction(
    notification_id: int,
    source_pdf_path: str,
    result: AggregatedExtractionResult,
    ai_summary: str | None = None,
):
    """
    Create a new pending extraction history record.

    The complete aggregated extraction, including evidence,
    is serialized for persistent storage.
    """

    with SessionLocal() as db:
        try:
            extracted_content = (
                serialize_aggregated_extraction(
                    result
                )
            )

            extraction = ExtractionHistory(
                notification_id=notification_id,
                extraction_type="COMPLETE_EXTRACTION",
                source_pdf_path=source_pdf_path,
                extracted_content=extracted_content,
                ai_summary=ai_summary,
                change_detected=False,
                change_details=None,
                extraction_status="PENDING",
                created_at=datetime.now(),
            )

            db.add(extraction)
            db.commit()
            db.refresh(extraction)

            return extraction

        except Exception:
            db.rollback()
            raise


# ============================================================
# APPROVE
# ============================================================

def approve_extraction(
    extraction_id: int,
):
    return approve_extraction_transaction(
        extraction_id
    )


# ============================================================
# REJECT
# ============================================================

def reject_extraction(
    extraction_id: int,
    feedback: str,
):
    """
    Reject a pending extraction and preserve
    administrator feedback.
    """

    feedback = feedback.strip()

    if not feedback:
        raise ValueError(
            "Rejection feedback cannot be empty."
        )

    with SessionLocal() as db:
        try:
            extraction = db.get(
                ExtractionHistory,
                extraction_id,
            )

            if extraction is None:
                raise ValueError(
                    "Extraction not found."
                )

            if extraction.extraction_status != "PENDING":
                raise ValueError(
                    "Only pending extractions can be rejected."
                )

            notification = db.get(
                OfficialNotification,
                extraction.notification_id,
            )

            if notification is None:
                raise ValueError(
                    "Official notification not found."
                )

            extraction.extraction_status = "REJECTED"

            # Preserve the exact admin feedback with
            # the rejected extraction.
            extraction.change_details = feedback

            notification.approval_status = "REJECTED"
            notification.rejection_reason = feedback

            db.commit()
            db.refresh(extraction)

            return extraction

        except Exception:
            db.rollback()
            raise


# ============================================================
# PDF PAGE EXTRACTION
# ============================================================

def _extract_pdf_pages(
    pdf_content: bytes,
) -> list[tuple[int, str]]:
    """
    Extract every PDF page while preserving page numbers.

    Returns:

        [
            (1, "page one text"),
            (2, "page two text"),
            ...
        ]

    Page numbers are 1-based.
    """

    if not pdf_content:
        raise ValueError(
            "PDF content is empty."
        )

    try:
        document = pymupdf.open(
            stream=pdf_content,
            filetype="pdf",
        )
    except Exception as error:
        raise ValueError(
            "Unable to open the original PDF."
        ) from error

    try:
        pages: list[tuple[int, str]] = []

        for page_number, page in enumerate(
            document,
            start=1,
        ):
            text = page.get_text()

            pages.append(
                (
                    page_number,
                    text,
                )
            )

    finally:
        document.close()

    if not pages:
        raise ValueError(
            "The original PDF contains no pages."
        )

    if not any(
        text.strip()
        for _, text in pages
    ):
        raise ValueError(
            "The original PDF contains no extractable text."
        )

    return pages


# ============================================================
# DOCUMENT HASH VERIFICATION
# ============================================================

def _verify_document_hash(
    pdf_content: bytes,
    expected_hash: str | None,
):
    """
    Verify that the document being processed is the
    same document that was originally stored.

    If an original hash exists, a mismatch stops the
    retry immediately.
    """

    if not expected_hash:
        return

    actual_hash = hashlib.sha256(
        pdf_content
    ).hexdigest()

    if actual_hash != expected_hash:
        raise ValueError(
            "The original document has changed since "
            "the extraction was created. "
            "Retry was stopped for safety."
        )


# ============================================================
# LOAD ORIGINAL DOCUMENT
# ============================================================

def _load_original_document_pages(
    extraction: ExtractionHistory,
    notification: OfficialNotification,
) -> tuple[list[tuple[int, str]], str]:
    """
    Load the exact original document.

    Retrieval order:

    1. Extraction history PDF path
    2. Notification PDF path
    3. Exact stored document URL

    No broad website crawling is performed.

    The document hash is verified whenever an original
    hash is available.
    """

    # --------------------------------------------------------
    # 1. Extraction history PDF
    # --------------------------------------------------------

    if extraction.source_pdf_path:
        extraction_path = Path(
            extraction.source_pdf_path
        )

        if extraction_path.is_file():
            pdf_content = extraction_path.read_bytes()

            if not pdf_content:
                raise ValueError(
                    "The stored extraction PDF is empty."
                )

            _verify_document_hash(
                pdf_content,
                notification.document_hash,
            )

            return (
                _extract_pdf_pages(
                    pdf_content
                ),
                str(extraction_path),
            )

    # --------------------------------------------------------
    # 2. Notification PDF
    # --------------------------------------------------------

    if notification.pdf_path:
        notification_path = Path(
            notification.pdf_path
        )

        if notification_path.is_file():
            pdf_content = notification_path.read_bytes()

            if not pdf_content:
                raise ValueError(
                    "The stored notification PDF is empty."
                )

            _verify_document_hash(
                pdf_content,
                notification.document_hash,
            )

            return (
                _extract_pdf_pages(
                    pdf_content
                ),
                str(notification_path),
            )

    # --------------------------------------------------------
    # 3. Exact stored document URL
    # --------------------------------------------------------

    if not notification.document_url:
        raise ValueError(
            "The original document cannot be located. "
            "No stored PDF path or document URL is available."
        )

    try:
        downloaded_pdf = download_pdf(
            notification.document_url
        )
    except Exception as error:
        raise ValueError(
            "The original document could not be downloaded "
            "from the stored document URL."
        ) from error

    pdf_content = downloaded_pdf["content"]

    if not pdf_content:
        raise ValueError(
            "The downloaded original document is empty."
        )

    _verify_document_hash(
        pdf_content,
        notification.document_hash,
    )

    return (
        _extract_pdf_pages(
            pdf_content
        ),
        downloaded_pdf["path"],
    )


# ============================================================
# CHECK FOR PENDING EXTRACTION
# ============================================================

def _get_pending_extraction(
    db,
    notification_id: int,
):
    """
    Return the latest pending extraction for a notification,
    if one exists.
    """

    return db.scalar(
        select(ExtractionHistory)
        .where(
            ExtractionHistory.notification_id
            == notification_id,
            ExtractionHistory.extraction_status
            == "PENDING",
        )
        .order_by(
            ExtractionHistory.extraction_id.desc()
        )
        .limit(1)
    )


# ============================================================
# RETRY EXTRACTION
# ============================================================

def retry_extraction(
    extraction_id: int,
):
    """
    Retry a rejected extraction using administrator feedback.

    Pipeline:

        REJECTED extraction
                ↓
        administrator feedback
                ↓
        exact original PDF
                ↓
        page extraction
                ↓
        lossless chunking
                ↓
        Gemini per chunk
                ↓
        conservative aggregation
                ↓
        normalization
                ↓
        validation
                ↓
        NEW PENDING extraction
                ↓
        administrator review

    The original rejected extraction is never modified.
    """

    # ========================================================
    # PHASE 1 — READ AND VALIDATE ORIGINAL EXTRACTION
    # ========================================================

    with SessionLocal() as db:

        extraction = db.get(
            ExtractionHistory,
            extraction_id,
        )

        if extraction is None:
            raise ValueError(
                "Extraction not found."
            )

        if extraction.extraction_status != "REJECTED":
            raise ValueError(
                "Only rejected extractions can be retried."
            )

        feedback = (
            extraction.change_details or ""
        ).strip()

        if not feedback:
            raise ValueError(
                "No rejection feedback found."
            )

        notification = db.get(
            OfficialNotification,
            extraction.notification_id,
        )

        if notification is None:
            raise ValueError(
                "Official notification not found."
            )

        existing_pending = _get_pending_extraction(
            db,
            notification.notification_id,
        )

        if existing_pending is not None:
            raise ValueError(
                "A pending extraction already exists "
                "for this notification."
            )

        # Store only primitive values before closing
        # the session. Do not use detached ORM objects.
        notification_id = (
            notification.notification_id
        )

        document_url = notification.document_url
        document_hash = notification.document_hash
        notification_pdf_path = notification.pdf_path

        source_pdf_path = (
            extraction.source_pdf_path
        )

    # ========================================================
    # PHASE 2 — LOAD EXACT ORIGINAL DOCUMENT
    # ========================================================

    # Create lightweight objects containing only the values
    # required by the document loader.
    #
    # No database relationship is accessed after the session
    # is closed.

    class _DocumentExtraction:
        def __init__(self, source_pdf_path):
            self.source_pdf_path = source_pdf_path

    class _DocumentNotification:
        def __init__(
            self,
            pdf_path,
            document_url,
            document_hash,
        ):
            self.pdf_path = pdf_path
            self.document_url = document_url
            self.document_hash = document_hash

    document_extraction = _DocumentExtraction(
        source_pdf_path
    )

    document_notification = _DocumentNotification(
        notification_pdf_path,
        document_url,
        document_hash,
    )

    pages, actual_pdf_path = (
        _load_original_document_pages(
            document_extraction,
            document_notification,
        )
    )

    # ========================================================
    # PHASE 3 — LOSSLESS CHUNKING
    # ========================================================

    chunks = chunk_document_pages(
        pages,
        chunk_size=30000,
    )

    if not chunks:
        raise ValueError(
            "The original document produced no "
            "extractable chunks."
        )

    # ========================================================
    # PHASE 4 — AI EXTRACTION
    # ========================================================

    chunk_results = []

    for chunk in chunks:

        result = extract_chunk_information(
            chunk,
            admin_feedback=feedback,
        )

        chunk_results.append(result)

    if not chunk_results:
        raise ValueError(
            "No chunk extraction results were produced."
        )

    # ========================================================
    # PHASE 5 — CONSERVATIVE AGGREGATION
    # ========================================================

    try:
        aggregated_result = (
            aggregate_chunk_extractions(
                chunk_results
            )
        )

    except ValueError as error:
        raise ValueError(
            "Retry extraction could not be safely "
            f"aggregated: {error}"
        ) from error

    # ========================================================
    # PHASE 6 — NORMALIZATION
    # ========================================================

    normalized_extraction = (
        normalize_complete_extraction(
            aggregated_result.extraction
        )
    )

    normalized_result = AggregatedExtractionResult(
        extraction=normalized_extraction,
        evidence=aggregated_result.evidence,
    )

    # ========================================================
    # PHASE 7 — VALIDATION
    # ========================================================

    validation_errors = (
        validate_complete_extraction(
            normalized_extraction
        )
    )

    if validation_errors:
        raise ValueError(
            "Retry extraction failed validation: "
            f"{validation_errors}"
        )

    # ========================================================
    # PHASE 8 — CREATE NEW PENDING EXTRACTION
    # ========================================================

    with SessionLocal() as db:

        try:
            # Re-read the original extraction because the
            # previous database session is already closed.
            original_extraction = db.get(
                ExtractionHistory,
                extraction_id,
            )

            if original_extraction is None:
                raise ValueError(
                    "Original extraction no longer exists."
                )

            if (
                original_extraction.extraction_status
                != "REJECTED"
            ):
                raise ValueError(
                    "The original extraction is no longer "
                    "in REJECTED status."
                )

            notification = db.get(
                OfficialNotification,
                notification_id,
            )

            if notification is None:
                raise ValueError(
                    "Official notification no longer exists."
                )

            # Re-check immediately before writing.
            existing_pending = _get_pending_extraction(
                db,
                notification_id,
            )

            if existing_pending is not None:
                raise ValueError(
                    "A pending extraction already exists "
                    "for this notification."
                )

            new_extraction = ExtractionHistory(
                notification_id=notification_id,
                extraction_type="RETRY_EXTRACTION",
                source_pdf_path=actual_pdf_path,
                extracted_content=(
                    serialize_aggregated_extraction(
                        normalized_result
                    )
                ),
                ai_summary=(
                    "Retry extraction generated using the "
                    "complete chunked extraction pipeline "
                    "after administrator feedback."
                ),
                change_detected=False,
                change_details=None,
                extraction_status="PENDING",
                created_at=datetime.now(),
            )

            db.add(new_extraction)

            # The new extraction is now awaiting HITL review.
            notification.approval_status = "PENDING"
            notification.rejection_reason = None

            db.commit()
            db.refresh(new_extraction)

            return new_extraction

        except Exception:
            db.rollback()
            raise


# ============================================================
# LOAD STORED EXTRACTION
# ============================================================

def load_extraction_result(
    extraction_id: int,
) -> AggregatedExtractionResult:
    """
    Load and deserialize a stored extraction result.
    """

    with SessionLocal() as db:

        extraction = db.get(
            ExtractionHistory,
            extraction_id,
        )

        if extraction is None:
            raise ValueError(
                "Extraction not found."
            )

        if not extraction.extracted_content:
            raise ValueError(
                "Extraction content is empty."
            )

        return deserialize_aggregated_extraction(
            extraction.extracted_content
        )