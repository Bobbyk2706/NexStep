from datetime import date

import pytest

from app.ai.aggregated_extraction_result import ExtractionIssue
from app.ai.extraction import compiler
from app.ai.extraction.dates import find_dates
from app.ai.extraction.facts import AgeLimit, DatesDraft, EligibilityDraft, Fact, QualificationFact
from app.ai.extraction.grounding import Grounder, locate_quote
from app.ai.extraction.llm import parse_model_json
from app.ai.extraction.structure import Passage
from app.ai.provider_manager import AIProviderManager, AllAIProvidersFailedError
from app.ai.providers.base import AIProvider, AIProviderRateLimitError
from app.ai.token_budget import TokenBucket, BudgetExceededError, reset_limiters_for_tests, get_limiter
from app.services.text_matching import canonical_text, texts_equal


def grounder(dates=()):
    return Grounder(passages={}, doc_dates=set(dates))


# ---------------------------------------------------------------- dates
def test_date_forms():
    got = {m.value for m in find_dates("February 6 & 7, 2027 | 6th-9th March 2027 | Sep 22 – Sep 30, 2026 | 01/02/2027")}
    assert {date(2027, 2, 6), date(2027, 2, 7), date(2027, 3, 6), date(2027, 3, 9),
            date(2026, 9, 22), date(2026, 9, 30), date(2027, 2, 1)} <= got


def test_invalid_dates_ignored():
    assert find_dates("February 30, 2027") == []


# ------------------------------------------------- age -> date of birth
@pytest.mark.parametrize("kind,years,ref,op,expected", [
    ("maximum", 30, "2026-08-01", ">=", "1995-08-02"),   # aged <=30 on 1 Aug 2026 => born after 1 Aug 1995
    ("minimum", 18, "2026-08-01", "<=", "2008-08-01"),
    ("maximum", 25, "2028-02-29", ">=", "2002-03-01"),   # leap-day reference
])
def test_age_becomes_dob_rule(kind, years, ref, op, expected):
    g = grounder([date.fromisoformat(ref)])
    draft = EligibilityDraft(
        age_limits=[AgeLimit(kind=kind, years=years, as_on_date=ref, quote=None, passage=None)],
        work_experience=Fact(),
    )
    _, rules = compiler.compile_eligibility(draft, g, "")
    rule = rules.rule_groups[0].rules[0]
    assert (rule.attribute, rule.operator, rule.value) == ("Date of Birth", op, expected)


def test_age_without_reference_date_creates_no_rule_but_warns():
    g = grounder()
    draft = EligibilityDraft(age_limits=[AgeLimit(kind="maximum", years=30)], work_experience=Fact())
    info, rules = compiler.compile_eligibility(draft, g, "")
    assert info.maximum_age == 30 and rules.rule_groups == []
    assert any(i.code == "age-no-reference-date" for i in g.issues)


def test_category_age_relaxation_is_not_a_general_rule():
    g = grounder([date(2026, 8, 1)])
    draft = EligibilityDraft(age_limits=[
        AgeLimit(kind="maximum", years=30, as_on_date="2026-08-01"),
        AgeLimit(kind="maximum", years=33, applies_to="OBC", as_on_date="2026-08-01"),
    ], work_experience=Fact())
    info, rules = compiler.compile_eligibility(draft, g, "")
    assert info.maximum_age == 30
    assert any("OBC" in text for text in info.other_requirements)
    assert not g.conflicts


def test_conflicting_general_limits_are_reported_not_fatal():
    g = grounder([date(2026, 8, 1)])
    draft = EligibilityDraft(age_limits=[
        AgeLimit(kind="maximum", years=30, as_on_date="2026-08-01"),
        AgeLimit(kind="maximum", years=32, as_on_date="2026-08-01"),
    ], work_experience=Fact())
    compiler.compile_eligibility(draft, g, "")
    assert len(g.conflicts) == 1 and len(g.conflicts[0].options) == 2


def test_alternatives_become_or_group_and_nationality_is_canonical():
    g = grounder()
    draft = EligibilityDraft(
        qualifications=[QualificationFact(level="Bachelor's"), QualificationFact(level="Master's")],
        nationalities=["Indian", "Nepali", "India"],
        minimum_percentage=55.0,
        work_experience=Fact(),
    )
    info, rules = compiler.compile_eligibility(draft, g, "")
    top = rules.rule_groups[0]
    assert top.logical_operator == "AND"
    assert [(r.attribute, r.operator, r.value) for r in top.rules] == [("Percentage", ">=", "55")]
    assert [r.value for r in top.child_groups[0].rules] == ["Bachelor's", "Master's"]
    assert [r.value for r in top.child_groups[1].rules] == ["India", "Nepal"]


def test_output_passes_the_existing_approval_gate():
    from app.ai.complete_extraction_normalizer import normalize_complete_extraction
    from app.ai.complete_extraction_validation import validate_complete_extraction
    from app.ai.exam_schemas import ExamInformation
    from app.ai.extraction_schemas import CompleteExtractionData
    g = grounder([date(2026, 8, 1)])
    draft = EligibilityDraft(
        age_limits=[AgeLimit(kind="maximum", years=30, as_on_date="2026-08-01")],
        qualifications=[QualificationFact(level="Bachelor's")], nationalities=["India"], work_experience=Fact())
    info, rules = compiler.compile_eligibility(draft, g, "")
    data = CompleteExtractionData(
        exam_information=ExamInformation(exam_name="X", conducting_body="Y", eligibility=info),
        eligibility_rules=rules)
    data = normalize_complete_extraction(data)
    assert validate_complete_extraction(data) == []


# ------------------------------------------------------------ grounding
def test_quote_location_exact_and_fuzzy():
    p = Passage("P1", 0, 3, 3, "Dates", "Application Portal closing | Sunday, September 27, 2026", tokens=10)
    assert locate_quote("Sunday, September 27, 2026", "P1", {"P1": p}).exact
    assert locate_quote("Application Portal closing Sunday September 27 2026", "P1", {"P1": p}) is not None
    assert locate_quote("Applications close on 5 November", "P1", {"P1": p}) is None


def test_parse_model_json_tolerates_fences_and_thinking():
    from app.ai.extraction.facts import Fact
    assert parse_model_json('<think>hmm</think>```json\n{"value": "a"}\n```', Fact).value == "a"
    assert parse_model_json('Sure! {"value": "b"} Done.', Fact).value == "b"
    with pytest.raises(Exception):
        parse_model_json("no json here", Fact)


# ---------------------------------------------------- text matching
def test_tolerant_text_matching():
    assert texts_equal("Indian", "India")
    assert texts_equal("bachelors", "Bachelor's")
    assert texts_equal("B.Tech.", "Bachelor's")
    assert texts_equal("12th", "12th / Senior Secondary")
    assert not texts_equal("Master's", "Bachelor's")
    assert canonical_text("  Computer   Science ") == "computer science"


# ------------------------------------------------- token budget + manager
class Boom(AIProvider):
    name = "groq"
    def __init__(self, exc): self.exc, self.calls = exc, 0
    def generate(self, **kw):
        self.calls += 1
        raise self.exc

class Ok(AIProvider):
    name = "openrouter"
    def __init__(self): self.calls = 0
    def generate(self, **kw):
        self.calls += 1
        return "{}"


def test_bucket_queues_then_refuses_long_waits():
    b = TokenBucket(600, safety=1.0, name="t")            # 10 tokens/s
    assert b.acquire(500, max_wait=1) == 0
    with pytest.raises(BudgetExceededError) as e:
        b.acquire(400, max_wait=1)
    assert e.value.wait_seconds > 1
    with pytest.raises(BudgetExceededError):
        b.acquire(10_000, max_wait=99)                    # can never fit


def test_manager_routes_to_next_provider_instead_of_hitting_429(monkeypatch):
    monkeypatch.setenv("NEXSTEP_GROQ_TPM", "1000")        # tiny budget
    reset_limiters_for_tests()
    groq, other = Boom(RuntimeError("must not be called")), Ok()
    m = AIProviderManager(providers=[groq, other])
    out = m.generate(messages=[{"role": "user", "content": "x" * 6000}], max_tokens=500)
    assert out == "{}" and groq.calls == 0 and other.calls == 1
    assert "Token budget" in m.last_attempts[0].error


def test_real_429_penalizes_bucket_and_falls_through(monkeypatch):
    monkeypatch.setenv("NEXSTEP_GROQ_TPM", "8000")
    reset_limiters_for_tests()
    groq, other = Boom(AIProviderRateLimitError("429", retry_after=20)), Ok()
    m = AIProviderManager(providers=[groq, other])
    assert m.generate(messages=[{"role": "user", "content": "hi"}], max_tokens=100) == "{}"
    assert get_limiter("groq")._tokens < 0                # bucket drained by Retry-After


def test_validation_failure_is_flagged_for_corrective_retry(monkeypatch):
    monkeypatch.setenv("NEXSTEP_GROQ_TPM", "0")
    reset_limiters_for_tests()
    m = AIProviderManager(providers=[Ok()])
    with pytest.raises(AllAIProvidersFailedError) as e:
        m.generate(messages=[{"role": "user", "content": "hi"}], validator=lambda s: 1 / 0)
    assert e.value.validation_failed
