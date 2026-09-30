# AI extraction pipeline (v2)

One entry point serves all four workflows (admin "Add exam", admin retry
with feedback, monitoring, AI discovery):

```python
from app.ai.extraction.pipeline import run_extraction, ensure_usable, summarize
result = run_extraction(pdf_bytes_or_path, exam_name_hint="GATE 2027", admin_feedback=None)
```

## Stages

| # | Stage | Module | Uses LLM |
|---|-------|--------|----------|
| 1 | **Parse** - clean text per page; removes struck-through (superseded) text, running headers/footers, fixes ligatures, detects headings by font; tables are rebuilt only for pages that matter | `parsing.py` | no |
| 2 | **Structure** - passages that keep section title + page numbers; contents pages skipped | `structure.py` | no |
| 3 | **Retrieve** - per topic (identity, dates, eligibility) BM25 + structural/date-density signals, fitted to the provider token budget | `retrieval.py` | no |
| 4 | **Extract** - one small call per topic asking for simple *facts*, each with passage id + verbatim quote | `facts.py`, `llm.py` | yes |
| 5 | **Ground** - every quote is located in the source; every date must occur in the document, otherwise it is dropped and flagged | `grounding.py` | no |
| 6 | **Compile** - facts become eligibility rules in Python (age limit + "as on" date -> Date of Birth bounds; qualification alternatives -> OR group) | `compiler.py` | no |
| 7 | **Normalize + validate** - same gates the approval step uses | existing modules | no |

## Why not chunk the whole document?

The GATE 2027 brochure is 143 pages (~100K tokens). Sending it in chunks
cost ~14 requests of ~9K tokens against an 8K tokens-per-minute limit.
The v2 pipeline sends 3 requests totalling ~12K tokens, and every value
is traceable to a page.

## Token budget

`app/ai/token_budget.py` keeps a shared bucket per provider. The provider
manager reserves `input + max_output` tokens before each call; if the wait
would be too long the request moves to the next provider, and providers
skipped only for a wait are retried as a last resort. A real 429 drains
the bucket by the `Retry-After` the provider sent.

## What the reviewer sees

The stored extraction JSON now also carries `issues` (error / warning /
info), `conflicts`, per-field `evidence` (page, section, verified flag)
and `pipeline` metadata. The admin review screen displays them.
`error` issues block approval, because approval re-runs the same validation.

## Tests

`pytest tests/backend` - runs the whole flow (extraction, admin review API,
approval, student eligibility) against the real GATE PDF with a scripted
LLM. Real-model quality can only be checked with your API keys.
