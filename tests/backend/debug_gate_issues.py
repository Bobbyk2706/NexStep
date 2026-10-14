r"""
Prints what the extraction pipeline kept and dropped for the GATE sample PDF.

Run from the backend folder:

    python ..\tests\backend\debug_gate_issues.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from app.ai.extraction.pipeline import run_extraction  # noqa: E402
from app.ai.provider_manager import AIProviderManager  # noqa: E402
from conftest import GATE_PDF  # noqa: E402
from fake_llm import ScriptedProvider  # noqa: E402

result = run_extraction(
    GATE_PDF,
    exam_name_hint="GATE",
    manager=AIProviderManager(providers=[ScriptedProvider()]),
)

info = result.extraction.exam_information

print("release_date        =", info.release_date)
print("application_end_date =", info.application_end_date)
print()
print("ISSUES")
for issue in result.issues:
    print(f"  [{issue.severity}] {issue.code}: {issue.message}")

print()
print("EVIDENCE for the two dates")
for item in result.evidence:
    if "elease" in item.field or "end date" in item.field.lower():
        for e in item.entries if hasattr(item, "entries") else [item]:
            print("  ", item.field, "->", getattr(e, "verified", None), repr(getattr(e, "quote", ""))[:140])


# ---------------------------------------------------------------------------
# Are the two dates in the document as far as the date finder can tell?
# ---------------------------------------------------------------------------
import re  # noqa: E402
from datetime import date  # noqa: E402

from app.ai.extraction.dates import date_set  # noqa: E402
from app.ai.extraction.parsing import parse_pdf  # noqa: E402

document = parse_pdf(GATE_PDF)
pages = [getattr(page, "text", "") or "" for page in document.pages]
text = "\n".join(pages)
found = date_set(text)

print()
for wanted in (date(2026, 8, 27), date(2026, 9, 27)):
    print(wanted, "found by date_set over the whole document:", wanted in found)

print()
print("Lines in the parsed document that mention a date in Aug/Sep/Oct 2026")
print("(struck-out text has already been removed by the parser):")

pattern = re.compile(
    r"(?:aug|sep|oct)\w*\.?\s+\d{1,2}|\d{1,2}\s*(?:st|nd|rd|th)?\s+(?:aug|sep|oct)",
    re.IGNORECASE,
)

shown = 0
for number, page_text in enumerate(pages, start=1):
    for line in page_text.splitlines():
        if "2026" in line and pattern.search(line):
            print(f"  p.{number}: {' '.join(line.split())[:220]}")
            shown += 1
            if shown >= 40:
                break
    if shown >= 40:
        break

if shown == 0:
    print("  (none)")