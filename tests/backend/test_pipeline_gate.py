from datetime import date

import pytest

from app.ai.provider_manager import AIProviderManager
from app.ai.extraction.pipeline import run_extraction
from conftest import GATE_PDF
from fake_llm import ScriptedProvider

pytestmark = pytest.mark.skipif(not GATE_PDF.exists(), reason="GATE sample PDF missing")


@pytest.fixture(scope="module")
def result():
    provider = ScriptedProvider()
    r = run_extraction(GATE_PDF, exam_name_hint="GATE", manager=AIProviderManager(providers=[provider]))
    r._provider = provider
    return r


def test_three_small_calls_not_fourteen_huge_ones(result):
    assert sorted(result._provider.calls) == ["dates", "eligibility", "identity"]
    total = sum(t["context_tokens"] for t in result.pipeline["topics"].values())
    assert total < 15000         # the old pipeline sent ~100K tokens


def test_exam_information(result):
    info = result.extraction.exam_information
    assert info.exam_name == "GATE 2027"
    assert info.conducting_body == "IIT Madras"
    assert info.release_date == "2026-08-27"
    assert info.application_start_date is None            # "To be Announced"
    assert info.application_end_date == "2026-09-27"      # not the struck-out 09-21
    assert [(d.start_date, d.end_date) for d in info.exam_dates] == [
        ("2027-02-06", "2027-02-07"), ("2027-02-13", "2027-02-14"), ("2027-02-20", "2027-02-21")]


def test_superseded_dates_reported(result):
    assert any(i.code == "superseded-ignored" for i in result.issues)


def test_rules_and_no_blocking_issues(result):
    groups = result.extraction.eligibility_rules.rule_groups
    assert groups
    text = result.model_dump_json()
    assert "Educational Qualification" in text and "Bachelor's" in text
    assert not result.blocking_issues, [i.message for i in result.blocking_issues]


def test_every_field_has_verified_evidence(result):
    verified = [e for e in result.evidence if e.verified]
    assert len(verified) >= 6 and all(e.page_numbers for e in verified)
