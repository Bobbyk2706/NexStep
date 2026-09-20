from __future__ import annotations

from pathlib import Path

import pymupdf

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
from app.services.document_chunker import (
    chunk_document_pages,
)


BASE_DIR = Path(__file__).resolve().parents[2]

MONITORING_STORAGE_DIR = (
    BASE_DIR
    / "storage"
    / "monitoring"
)

MONITORING_STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# PDF PAGE EXTRACTION
# ============================================================


def extract_monitoring_pdf_pages(
    pdf_content: bytes,
) -> list[str]:
    """
    Extract text from every page of a newly detected PDF.

    No page filtering is performed.
    """

    if not pdf_content:
        raise ValueError(
            "Monitoring PDF content is empty."
        )

    try:
        document = pymupdf.open(
            stream=pdf_content,
            filetype="pdf",
        )

    except Exception as error:
        raise ValueError(
            "Failed to open monitoring PDF."
        ) from error

    try:
        pages = [
            page.get_text()
            for page in document
        ]

    finally:
        document.close()

    if not pages:
        raise ValueError(
            "Monitoring PDF contains no pages."
        )

    if not any(
        page.strip()
        for page in pages
    ):
        raise ValueError(
            "Monitoring PDF contains no "
            "extractable text."
        )

    return pages


# ============================================================
# PDF STORAGE
# ============================================================


def save_monitoring_document(
    pdf_content: bytes,
    document_hash: str,
) -> str:
    """
    Save a newly detected document under a hash-based
    filename.

    The approved notification PDF is never overwritten.
    """

    if not pdf_content:
        raise ValueError(
            "Cannot save empty monitoring document."
        )

    if not document_hash:
        raise ValueError(
            "Document hash is required."
        )

    file_path = (
        MONITORING_STORAGE_DIR
        / f"{document_hash}.pdf"
    )

    if not file_path.exists():
        with open(
            file_path,
            "wb",
        ) as file:
            file.write(
                pdf_content
            )

    return str(file_path)


# ============================================================
# NEW DOCUMENT EXTRACTION
# ============================================================


def extract_new_monitoring_document(
    pdf_content: bytes,
    document_hash: str,
) -> dict:
    """
    Run the existing NexStep extraction pipeline against
    a newly detected monitoring document.

    This function performs:

        PDF page extraction
        -> lossless chunking
        -> Gemini extraction
        -> conservative aggregation
        -> normalization
        -> validation

    It does NOT:

        - modify the approved notification
        - create an ExtractionHistory record
        - approve the new extraction
        - reject the new extraction
        - update eligibility
        - send notifications
    """

    # --------------------------------------------------------
    # 1. Save new document separately
    # --------------------------------------------------------

    pdf_path = save_monitoring_document(
        pdf_content=pdf_content,
        document_hash=document_hash,
    )

    # --------------------------------------------------------
    # 2. Extract every PDF page
    # --------------------------------------------------------

    pages = extract_monitoring_pdf_pages(
        pdf_content
    )

    # --------------------------------------------------------
    # 3. Lossless chunking
    # --------------------------------------------------------

    chunks = chunk_document_pages(
        pages,
        chunk_size=30000,
    )

    if not chunks:
        raise ValueError(
            "No document chunks were produced."
        )

    # --------------------------------------------------------
    # 4. AI extraction for every chunk
    # --------------------------------------------------------

    chunk_results = []

    for chunk in chunks:

        result = extract_chunk_information(
            chunk
        )

        chunk_results.append(
            result
        )

    if not chunk_results:
        raise ValueError(
            "No chunk extraction results were produced."
        )

    # --------------------------------------------------------
    # 5. Conservative aggregation
    # --------------------------------------------------------

    try:
        aggregated_result = (
            aggregate_chunk_extractions(
                chunk_results
            )
        )

    except ValueError as error:
        raise ValueError(
            "Monitoring extraction could not be safely "
            f"aggregated: {error}"
        ) from error

    # --------------------------------------------------------
    # 6. Normalization
    # --------------------------------------------------------

    normalized_extraction = (
        normalize_complete_extraction(
            aggregated_result.extraction
        )
    )

    normalized_result = (
        AggregatedExtractionResult(
            extraction=normalized_extraction,
            evidence=aggregated_result.evidence,
        )
    )

    # --------------------------------------------------------
    # 7. Validation
    # --------------------------------------------------------

    validation_errors = (
        validate_complete_extraction(
            normalized_extraction
        )
    )

    if validation_errors:
        raise ValueError(
            "Monitoring extraction failed validation: "
            f"{validation_errors}"
        )

    # --------------------------------------------------------
    # 8. Return new validated version
    # --------------------------------------------------------

    return {
        "pdf_path": pdf_path,
        "document_hash": document_hash,
        "extraction": normalized_result,
        "status": "VALIDATED",
    }