from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.ai.chunk_extraction_result import ChunkExtractionResult
from app.ai.chunk_extractor import extract_chunk_information
from app.services.document_chunker import DocumentChunk

# ============================================================
# SHARED PARALLEL CHUNK EXTRACTION
# ============================================================
#
# extract_chunk_information() makes one LLM call per chunk and
# processes each chunk completely independently (no shared state,
# no cross-chunk context). That independence is exactly what makes
# it safe to run several chunks concurrently: this is an I/O-bound
# operation (waiting on the AI provider's HTTP response), so
# concurrency gives a large wall-clock speedup on multi-chunk PDFs
# without changing what gets extracted or in what order results
# are combined.
#
# This module centralizes that concurrency so every pipeline that
# extracts chunks (the main admin extraction pipeline, the AI
# discovery pipeline, the monitoring/change-detection pipeline, and
# the admin retry-with-feedback workflow) behaves the same way and
# only needs to be tuned in one place.

_DEFAULT_MAX_WORKERS = max(
    1,
    int(
        os.environ.get(
            "NEXSTEP_CHUNK_EXTRACTION_WORKERS",
            "4",
        )
    ),
)


def extract_chunks_in_parallel(
    chunks: list[DocumentChunk],
    *,
    admin_feedback: str | None = None,
    max_workers: int | None = None,
) -> list[ChunkExtractionResult]:

    total = len(chunks)

    if total == 0:
        return []

    results: list[Any] = [None] * total

    workers = min(
        max_workers or _DEFAULT_MAX_WORKERS,
        total,
    )

    print(
        f"[AI PARALLEL] START "
        f"chunks={total} workers={workers}",
        flush=True,
    )

    def extract_one(
        index: int,
        chunk: DocumentChunk,
    ):
        print(
            f"[AI PARALLEL] CHUNK {index + 1}/{total} START "
            f"chars={len(chunk.text)} "
            f"pages={chunk.page_numbers}",
            flush=True,
        )

        try:
            result = extract_chunk_information(
                chunk,
                admin_feedback,
            )

            print(
                f"[AI PARALLEL] CHUNK {index + 1}/{total} COMPLETE",
                flush=True,
            )

            return result

        except Exception as error:

            print(
                f"[AI PARALLEL] CHUNK {index + 1}/{total} FAILED "
                f"{type(error).__name__}: {error}",
                flush=True,
            )

            raise

    with ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        future_to_index = {
            executor.submit(
                extract_one,
                index,
                chunk,
            ): index
            for index, chunk in enumerate(chunks)
        }

        first_error: Exception | None = None

        for future in as_completed(
            future_to_index
        ):

            index = future_to_index[future]

            try:
                results[index] = future.result()

                print(
                    f"[AI PARALLEL] RESULT RECEIVED "
                    f"chunk={index + 1}/{total}",
                    flush=True,
                )

            except Exception as error:

                print(
                    f"[AI PARALLEL] RESULT FAILED "
                    f"chunk={index + 1}/{total} "
                    f"{type(error).__name__}: {error}",
                    flush=True,
                )

                if first_error is None:
                    first_error = error

        if first_error is not None:
            raise first_error

    print(
        f"[AI PARALLEL] ALL CHUNKS COMPLETE "
        f"total={total}",
        flush=True,
    )

    return results