import json
from datetime import date

import pytest

from app.ai.extraction.parsing import parse_text_pages
from app.ai.extraction.pipeline import run_extraction, ExtractionError
from app.ai.provider_manager import AIProviderManager
from app.ai.token_budget import TokenBucket, BudgetExceededError
from fake_llm import ScriptedProvider, fact, passage_id, EMPTY

DOC = parse_text_pages([
    "Staff Selection Notification 2026\nIssued by Example Recruitment Board\nNotification date: 1 June 2026",
    "Important Dates\nOnline applications open on 10 June 2026\nLast date to apply: 30 June 2026\n"
    "Written examination on 15 and 16 August 2026",
    "Eligibility Criteria\nNationality: Candidates must be citizens of India.\n"
    "Age limit: 18 to 27 years as on 1 January 2026.\n"
    "Qualification: A Bachelor's degree from a recognised university with at least 60% marks.",
])


def script(overrides=None):
    def fn(task, c):
        if task == "identity":
            out = {"exam_name": fact(c, "Staff Selection 2026", "Staff Selection Notification 2026"),
                   "conducting_body": fact(c, "Example Recruitment Board", "Example Recruitment Board"),
                   "release_date": fact(c, "2026-06-01", "1 June 2026")}
        elif task == "dates":
            out = {"application_start_date": fact(c, "2026-06-10", "10 June 2026"),
                   "application_end_date": fact(c, "2026-06-30", "30 June 2026"),
                   "late_fee_end_date": EMPTY,
                   "exam_dates": [{"label": None, "start_date": "2026-08-15", "end_date": "2026-08-16",
                                   "quote": "15 and 16 August 2026", "passage": passage_id(c, "15 and 16 August")}]}
        else:
            out = {"has_no_age_limit": False,
                   "age_limits": [
                       {"kind": "minimum", "years": 18, "applies_to": "all candidates", "as_on_date": "2026-01-01",
                        "quote": "18 to 27 years as on 1 January 2026", "passage": passage_id(c, "18 to 27")},
                       {"kind": "maximum", "years": 27, "applies_to": "all candidates", "as_on_date": "2026-01-01",
                        "quote": "18 to 27 years as on 1 January 2026", "passage": passage_id(c, "18 to 27")}],
                   "qualifications": [{"level": "Bachelor's", "field": None, "quote": "A Bachelor's degree",
                                       "passage": passage_id(c, "Bachelor's degree")}],
                   "minimum_percentage": 60.0, "minimum_cgpa": None,
                   "score_quote": "at least 60% marks", "score_passage": passage_id(c, "60% marks"),
                   "nationalities": ["India"], "nationality_quote": "citizens of India",
                   "nationality_passage": passage_id(c, "citizens of India"),
                   "work_experience": EMPTY, "other_requirements": []}
        if overrides:
            out = overrides(task, out, c) or out
        return out
    return fn


def run(overrides=None, providers=None):
    p = providers or [ScriptedProvider(script(overrides))]
    return run_extraction(DOC, manager=AIProviderManager(providers=p))


def rules_of(r):
    def walk(g):
        for x in g.rules:
            yield (x.attribute, x.operator, x.value)
        for c in g.child_groups:
            yield from walk(c)
    return {x for g in r.extraction.eligibility_rules.rule_groups for x in walk(g)}


def test_age_limit_becomes_date_of_birth_rules_in_python():
    rules = rules_of(run())
    # 18..27 as on 2026-01-01  =>  born on/before 2008-01-01 and on/after 1998-01-02
    assert ("Date of Birth", "<=", "2008-01-01") in rules
    assert ("Date of Birth", ">=", "1998-01-02") in rules
    assert ("Percentage", ">=", "60") in rules or ("Percentage", ">=", "60.0") in rules
    assert ("Nationality", "=", "India") in rules
    assert ("Educational Qualification", "=", "Bachelor's") in rules


def test_hallucinated_date_is_dropped_not_stored():
    def bad(task, out, c):
        if task == "dates":
            out["application_end_date"] = {"value": "2026-07-31", "quote": "31 July 2026", "passage": None}
            return out
    r = run(bad)
    assert r.extraction.exam_information.application_end_date is None
    assert any(i.code == "date-not-in-document" for i in r.issues)


def test_age_without_reference_date_creates_no_guessed_rule():
    def no_ref(task, out, c):
        if task == "eligibility":
            for a in out["age_limits"]:
                a["as_on_date"] = None
            return out
    r = run(no_ref)
    assert not [x for x in rules_of(r) if x[0] == "Date of Birth"]
    assert any("reference date" in i.message.lower() or "as on" in i.message.lower() for i in r.issues)


def test_unsupported_output_falls_back_and_retries():
    calls = {"n": 0}

    def sometimes_garbage(task, c):
        calls["n"] += 1
        return "sorry, here you go: {not json" if calls["n"] == 1 else script()(task, c)

    r = run(providers=[ScriptedProvider(sometimes_garbage)])
    assert r.extraction.exam_information.exam_name
    assert any(c.get("corrective_retry") for c in r.pipeline["calls"])


def test_markdown_fenced_json_is_accepted():
    p = ScriptedProvider(lambda t, c: "```json\n" + json.dumps(script()(t, c)) + "\n```")
    assert run(providers=[p]).extraction.exam_information.exam_name == "Staff Selection 2026"


def test_token_budget_routes_to_next_provider(monkeypatch):
    from app.ai import token_budget as tb

    class Limited(ScriptedProvider):
        name = "groq"

    monkeypatch.setattr(tb, "_limiters", {"groq": TokenBucket(600, safety=1.0, name="groq")})
    monkeypatch.setattr(tb, "_PROVIDER_TPM", {"groq": ("X", 600)})
    limited, backup = Limited(script()), ScriptedProvider(script())
    r = run(providers=[limited, backup])
    assert limited.calls == []                 # request never fit the bucket
    assert backup.calls                        # so it was routed on, no 429 storm
    assert r.extraction.exam_information.exam_name


def test_all_providers_failing_raises_cleanly():
    class Broken(ScriptedProvider):
        def generate(self, **kw):
            from app.ai.providers.base import AIProviderUnavailableError
            raise AIProviderUnavailableError("down")
    with pytest.raises(ExtractionError):
        run(providers=[Broken()])
