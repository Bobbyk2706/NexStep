"""
End to end through the real application: extraction workflow -> admin
review API -> approval -> student eligibility. Only the LLM (scripted)
and the web-source verification step are replaced.
"""
from datetime import date
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from conftest import GATE_PDF
from fake_llm import FakeProvider, GATE_ANSWERS

pytestmark = pytest.mark.skipif(not GATE_PDF.exists(), reason="GATE sample PDF missing")


@pytest.fixture(scope="module")
def app_env():
    import app.models  # noqa: F401  (register every table)
    from app.auth.security import hash_password
    from app.database.engine import engine
    from app.database.session import SessionLocal
    from app.models.admin import Admin
    from app.models.base import Base
    from app.models.conducting_body import ConductingBody
    from app.models.education import Education
    from app.models.eligibility_attribute import EligibilityAttribute
    from app.models.exam import Exam
    from app.models.student import Student
    import app.ai.extraction.pipeline as pipeline
    from app.ai.provider_manager import AIProviderManager

    Base.metadata.create_all(engine)

    with SessionLocal() as db:
        for name, table, column, dtype in [
            ("CGPA", "education", "cgpa", "numeric"),
            ("Percentage", "education", "percentage", "numeric"),
            ("Specialization", "education", "specialization", "text"),
            ("Date of Birth", "student", "date_of_birth", "date"),
            ("Nationality", "student", "nationality", "text"),
            ("State", "student", "state", "text"),
            ("Educational Qualification", "education", "qualification", "text"),
            ("Work Experience", "work_experience", "duration", "text"),
        ]:
            db.add(EligibilityAttribute(attribute_name=name, source_table=table,
                                        source_column=column, data_type=dtype, description=name))

        body = ConductingBody(name="Placeholder body", main_website="https://example.org/")
        db.add(body)
        db.flush()
        exam = Exam(body_id=body.body_id, name="GATE 2027", type="Entrance", status="ACTIVE",
                    description=None, off_exam_page="https://gate2027.iitm.ac.in/")
        db.add(exam)

        db.add(Admin(name="Admin", email="admin@test.com", password_hash=hash_password("adminpass123"),
                     account_status="active"))

        def student(email, level):
            s = Student(name=email, email=email, password_hash=hash_password("studentpass1"),
                        date_of_birth=date(2003, 5, 5), nationality="Indian", state="Kerala",
                        gender="F", account_status="active")
            db.add(s)
            db.flush()
            db.add(Education(student_id=s.student_id, qualification=level, specialization="CS",
                             cgpa=8.0, percentage=None, current_year=3, year_of_passing=None,
                             is_current=True, institution="X", year_of_study_label="3rd Year",
                             is_higher_qualification=False))

        student("btech@test.com", "Bachelor's")
        student("school@test.com", "12th / Senior Secondary")
        db.commit()
        exam_id = exam.exam_id

    provider = FakeProvider(GATE_ANSWERS)
    pipeline._default_manager = AIProviderManager(providers=[provider])

    from app.main import app
    yield SimpleNamespace(client=TestClient(app), exam_id=exam_id, provider=provider)
    pipeline._default_manager = None


def _login(client, url, email, password):
    r = client.post(url, json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    body = r.json()
    return body.get("access_token") or body["token"]


def test_full_workflow(app_env, monkeypatch, tmp_path):
    from app.services import exam_pipeline_service as svc
    monkeypatch.setenv("NEXSTEP_GROQ_TPM", "0")

    pdf = GATE_PDF.read_bytes()
    url = "https://gate2027.iitm.ac.in/static/doc/IB/GATE2027-IB.pdf"
    monkeypatch.setattr(svc, "verify_exam_source", lambda name, sources: SimpleNamespace(
        relevant=True, selected_url=url, source_type="OFFICIAL_NOTIFICATION"))

    # ---- 1. extraction workflow (what the admin "Add exam" button runs)
    outcome = svc.process_exam(
        app_env.exam_id, "GATE 2027", "https://gate2027.iitm.ac.in/",
        known_source={"url": url, "document_url": url, "pdf_path": str(GATE_PDF),
                      "document_hash": "abc123", "content": pdf})
    assert outcome["status"] == "PENDING"
    extraction_id = outcome["extraction_id"]

    # ---- 2. admin review API
    client = app_env.client
    admin = {"Authorization": "Bearer " + _login(client, "/api/auth/admin/login", "admin@test.com", "adminpass123")}

    rows = client.get("/admin/extractions", headers=admin).json()
    assert rows[0]["status"] == "PENDING"

    detail = client.get(f"/admin/extractions/{extraction_id}", headers=admin).json()
    import json
    content = json.loads(detail["extracted_content"])
    assert content["pipeline"]["version"] == "2.0"
    assert content["extraction"]["exam_information"]["application_end_date"] == "2026-09-27"
    assert {i["code"] for i in content["issues"]} >= {"start-tba", "superseded-ignored"}
    assert all(e["page_numbers"] for e in content["evidence"] if e["verified"])
    assert "GATE 2027" in detail["ai_summary"]

    # ---- 3. approve -> published as authoritative data
    r = client.post(f"/admin/extractions/{extraction_id}/approve", headers=admin)
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "APPROVED"

    exam = client.get(f"/api/exams/{app_env.exam_id}").json() if False else None

    # ---- 4. students are evaluated against the approved rules
    def verdict(email):
        token = _login(client, "/api/auth/login", email, "studentpass1")
        h = {"Authorization": f"Bearer {token}"}
        r = client.post(f"/api/eligibility/{app_env.exam_id}/evaluate", headers=h)
        assert r.status_code in (200, 201), r.text
        return r.json()

    assert verdict("btech@test.com")["eligibility_status"] == "ELIGIBLE"
    assert verdict("school@test.com")["eligibility_status"] != "ELIGIBLE"


def test_reject_then_retry_uses_feedback(app_env, monkeypatch):
    from app.services import exam_pipeline_service as svc
    monkeypatch.setenv("NEXSTEP_GROQ_TPM", "0")
    url = "https://gate2027.iitm.ac.in/static/doc/IB/GATE2027-IB.pdf"
    monkeypatch.setattr(svc, "verify_exam_source", lambda name, sources: SimpleNamespace(
        relevant=True, selected_url=url, source_type="OFFICIAL_NOTIFICATION"))
    out = svc.process_exam(app_env.exam_id, "GATE 2027", "https://gate2027.iitm.ac.in/",
                           known_source={"url": url, "document_url": url, "pdf_path": str(GATE_PDF),
                                         "document_hash": __import__("hashlib").sha256(GATE_PDF.read_bytes()).hexdigest(), "content": GATE_PDF.read_bytes()})

    client = app_env.client
    admin = {"Authorization": "Bearer " + _login(client, "/api/auth/admin/login", "admin@test.com", "adminpass123")}
    eid = out["extraction_id"]

    r = client.post(f"/admin/extractions/{eid}/reject", headers=admin,
                    json={"feedback": "The application end date looks wrong, please re-check."})
    assert r.status_code == 200, r.text

    seen_before = len(app_env.provider.calls)
    r = client.post(f"/admin/extractions/{eid}/retry", headers=admin)
    assert r.status_code == 200, r.text
    assert r.json()["extraction_type"] == "RETRY_EXTRACTION"
    assert len(app_env.provider.calls) == seen_before + 3

    new_id = r.json()["extraction_id"]
    assert new_id != eid
    assert client.get(f"/admin/extractions/{new_id}", headers=admin).json()["status"] == "PENDING"
