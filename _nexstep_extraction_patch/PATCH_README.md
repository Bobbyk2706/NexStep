# NexStep exam extraction patch

This patch addresses the failure patterns shown in the provided backend logs. It does not include or change API keys, database settings, authentication, frontend code, or deployment environment files.

## Files changed

- `backend/app/ai/extraction/pipeline.py`
  - Makes per-facet output-token limits configurable and raises the starting defaults for identity, dates, and eligibility. The context is reduced accordingly so output reservations remain part of the request budget.
- `backend/app/ai/providers/openrouter_provider.py`
  - Retries intermittent empty OpenRouter responses and includes the selected model and finish reason in the error for easier diagnosis.
- `backend/app/ai/source_verification.py`
  - Asks the model to select a candidate ID (`S1`, `S2`, ...) instead of copying a long URL. Python maps the ID back to the exact URL from the supplied search results; unrecognized IDs are rejected.
- `backend/app/services/ai_exam_discovery_service.py`
  - Rejects PDF link candidates that have no exam identity evidence and strengthens actual PDF text validation so a year or one incidental word cannot make an unrelated PDF pass.

## Apply on Windows PowerShell

1. Stop the backend with `Ctrl+C`.
2. Copy `nexstep_extraction_fix.zip` to the NexStep project root, e.g. `C:\Users\VIVEK\Documents\Projects\NexStep`.
3. From that project root, run:

   ```powershell
   Expand-Archive -LiteralPath .\nexstep_extraction_fix.zip -DestinationPath .\_nexstep_extraction_patch -Force
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\_nexstep_extraction_patch\apply_nexstep_patch.ps1
   ```

4. The script creates a timestamped `_nexstep_extraction_backup_...` folder before replacing the four files. It refuses to apply if an expected project file is missing.
5. Run a syntax check:

   ```powershell
   .\.venv\Scripts\python.exe -m py_compile backend\app\ai\extraction\pipeline.py backend\app\ai\providers\openrouter_provider.py backend\app\ai\source_verification.py backend\app\services\ai_exam_discovery_service.py
   ```

6. Restart the backend:

   ```powershell
   cd backend
   ..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

## OpenRouter configuration

In `backend\.env`, set `OPENROUTER_MODEL` to a model ID currently available to your OpenRouter account that supports the structured JSON output used by this project. The `openrouter/free` alias can route to different models, so a specific available model is easier to debug. Do not paste or commit `OPENROUTER_API_KEY`.

The new output limits can be overridden in `backend\.env` if needed:

```dotenv
NEXSTEP_OUTPUT_TOKENS_IDENTITY=700
NEXSTEP_OUTPUT_TOKENS_DATES=1800
NEXSTEP_OUTPUT_TOKENS_ELIGIBILITY=2200
```

These are starting values, not a guarantee that every provider will return valid JSON. If the provider has a lower maximum output limit, choose smaller values. Larger output reservations can also cause a rate-limited provider to be skipped more often, depending on its token budget.

## Test safely

1. Test one exam with a known current official notification first.
2. Confirm the saved PDF belongs to the exact exam and year.
3. Review dates and eligibility against the source before approving an extraction.
4. If the admin request still returns `422`, open browser Developer Tools → Network → `POST /admin/extractions` → Response and inspect the `detail` field. Save the matching backend log lines too.

## Important limitations

- This patch is based on the uploaded project dump, not a live copy of your working directory. Keep the automatic backup and inspect the diff before deploying.
- The patch does not make an unavailable notification appear. If an official notification has not been published, NexStep should not substitute a prior-year notice.
- Scanned PDFs without a text layer may still require OCR support; this patch does not add OCR.
- The patch can be syntax-checked against the included files here, but runtime behavior still needs to be verified with your actual dependencies, `.env`, provider access, and database.
