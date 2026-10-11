"""
Bulk exam discovery.

Runs the same AI discovery pipeline as the admin "Add Examination" page
for every exam name in a text file, one after another. Each success
becomes a PENDING extraction that you still review and approve in the
admin UI. Nothing is approved automatically.

Run from the backend folder:

    python -m scripts.bulk_discover exams.txt
    python -m scripts.bulk_discover exams.txt --delay 30

The file has one exam name per line. Blank lines and lines starting
with # are ignored.

Results are appended to storage/bulk_discovery_results.csv. If you
stop it (Ctrl+C) or run it again, exams that already succeeded are
skipped, so it is safe to re-run.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from datetime import datetime
from pathlib import Path

from app.logging_config import setup_logging

RESULTS_FILE = (
    Path(__file__).resolve().parents[1]
    / "storage"
    / "bulk_discovery_results.csv"
)

FIELDS = ["timestamp", "exam_name", "status", "extraction_id", "detail"]


def _read_names(path: Path) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        name = line.strip()

        if not name or name.startswith("#"):
            continue

        key = " ".join(name.casefold().split())

        if key in seen:
            continue

        seen.add(key)
        names.append(name)

    return names


def _already_succeeded() -> set[str]:
    if not RESULTS_FILE.exists():
        return set()

    done: set[str] = set()

    with RESULTS_FILE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("status") == "OK":
                done.add(" ".join((row.get("exam_name") or "").casefold().split()))

    return done


def _append_result(row: dict) -> None:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    new_file = not RESULTS_FILE.exists()

    with RESULTS_FILE.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)

        if new_file:
            writer.writeheader()

        writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk exam discovery")
    parser.add_argument("names_file", help="Text file with one exam name per line")
    parser.add_argument(
        "--delay",
        type=int,
        default=20,
        help="Seconds to wait between exams (default 20), to stay within AI/search rate limits",
    )
    args = parser.parse_args()

    names_path = Path(args.names_file)

    if not names_path.is_file():
        print(f"File not found: {names_path}")
        return 1

    setup_logging()

    from app.services.ai_exam_discovery_service import (
        ExamDiscoveryError,
        NoNotificationFoundError,
        discover_exam,
    )

    done = _already_succeeded()
    todo = [
        name
        for name in _read_names(names_path)
        if " ".join(name.casefold().split()) not in done
    ]

    if not todo:
        print("Nothing to do: every exam in the file already succeeded.")
        return 0

    print(f"{len(todo)} exam(s) to process. Results: {RESULTS_FILE}")

    counts = {"OK": 0, "NOT_FOUND": 0, "FAILED": 0}

    try:
        for index, name in enumerate(todo, start=1):
            print(f"\n[{index}/{len(todo)}] {name}")

            extraction_id = ""
            detail = ""

            try:
                result = discover_exam(name)
                status = "OK"
                extraction_id = result.get("extraction_id", "")
                detail = result.get("official_url", "")

            except NoNotificationFoundError as exc:
                status = "NOT_FOUND"
                detail = exc.official_url or ""

            except (ExamDiscoveryError, ValueError) as exc:
                status = "FAILED"
                detail = str(exc)[:300]

            except Exception as exc:  # keep the batch going
                status = "FAILED"
                detail = f"{type(exc).__name__}: {exc}"[:300]

            counts[status] += 1
            print(f"    -> {status} {extraction_id} {detail}")

            _append_result(
                {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "exam_name": name,
                    "status": status,
                    "extraction_id": extraction_id,
                    "detail": detail,
                }
            )

            if index < len(todo):
                time.sleep(max(0, args.delay))

    except KeyboardInterrupt:
        print("\nStopped. Run the same command again to resume.")

    print(
        f"\nDone. OK: {counts['OK']}  NOT_FOUND: {counts['NOT_FOUND']}  "
        f"FAILED: {counts['FAILED']}"
    )
    print("Review the OK ones in the admin Extraction History page.")

    return 0


if __name__ == "__main__":
    sys.exit(main())