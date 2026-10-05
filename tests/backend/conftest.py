import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))
import tempfile

# A file database (not :memory:) so the app's worker threads and the
# test share the same data.
_DB_DIR = tempfile.mkdtemp(prefix="nexstep-test-")
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_DIR}/test.db"
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("NEXSTEP_GROQ_TPM", "0")          # no real limiter in tests
os.environ.setdefault("NEXSTEP_TOKENIZER", "chars")

GATE_PDF = ROOT / "backend" / "storage" / "notifications" / "GATE2027-IB.pdf"
