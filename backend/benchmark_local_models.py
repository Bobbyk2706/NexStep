import time
import os
import fitz

from app.services.document_chunker import DocumentChunk
from app.ai.parallel_chunk_extraction import extract_chunk_information

PDF = r"storage\notifications\GATE2027-IB.pdf"

doc = fitz.open(PDF)

text = ""
pages = []

for i, page in enumerate(doc):
    page_text = page.get_text()
    if not page_text:
        continue

    remaining = 16000 - len(text)

    if remaining <= 0:
        break

    text += page_text[:remaining]
    pages.append(i + 1)

    if len(text) >= 16000:
        break

doc.close()

chunk = DocumentChunk(
    chunk_number=1,
    text=text,
    page_numbers=pages,
)

print(f"Benchmark chunk: {len(text)} chars")
print(f"Pages: {pages}")

for model in ["qwen3:1.7b", "gemma3:4b"]:
    print("\n" + "=" * 60)
    print(f"MODEL: {model}")
    print("=" * 60)

    os.environ["LOCAL_AI_MODEL"] = model

    start = time.perf_counter()

    try:
        result = extract_chunk_information(chunk)
        elapsed = time.perf_counter() - start

        print(f"SUCCESS")
        print(f"TIME_SECONDS: {elapsed:.2f}")
        print(f"RESULT_TYPE: {type(result).__name__}")
        print(f"RESULT: {result}")

    except Exception as exc:
        elapsed = time.perf_counter() - start

        print(f"FAILED")
        print(f"TIME_SECONDS: {elapsed:.2f}")
        print(f"ERROR_TYPE: {type(exc).__name__}")
        print(f"ERROR: {exc}")

print("\nBenchmark complete.")
