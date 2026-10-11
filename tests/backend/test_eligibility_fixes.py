"""
Tests for the eligibility-rule fixes:

  * age limits -> date-of-birth rules ("must not have attained 32")
  * category concessions are not competing age limits
  * quotes recovered from the document when the model gives none
  * free-text nationality conditions are not rules
  * rule-tree tidying in the normalizer
  * evaluation: release date, reasons, empty groups, qualification levels
"""

from datetime import date
from types import SimpleNamespace as NS

from app.ai.eligibility_rule_normalizer import normalize_eligibility_rules
from app.ai.eligibility_schemas import (
    EligibilityRuleData,
    EligibilityRuleGroupData,
    EligibilityRulesData,
)
from app.ai.extraction import compiler, facts
from app.ai.extraction.age_rules import (
    dob_boundary,
    find_age_reference_date,
    is_exclusive,
    parse_explicit_dob_limits,
)
from app.ai.extraction.dates import date_set
from app.ai.extraction.grounding import Grounder, document_dates
from app.ai.extraction.structure import Passage
from app.services.eligibility_service import (
    _RuleGroupNode,
    _evaluate_rule_group,
    _get_latest_approved_notification,
    check_rule,
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _passage(number: int, text: str) -> Passage:
    return Passage(
        id=f"P{number}",
        index=number - 1,
        page_start=1,
        page_end=1,
        section="Eligibility",
        text=text,
        tokens=0,
    )


def _compile(draft, *passages):
    by_id = {p.id: p for p in passages}

    grounder = Grounder(
        passages=by_id,
        doc_dates=document_dates([p.text for p in passages]),
    )

    context = "\n\n".join(p.tagged() for p in passages)

    info, rules = compiler.compile_eligibility(draft, grounder, context)

    return info, rules, grounder


def _dob_rules(rules):
    return sorted(
        (r.operator, r.value)
        for g in rules.rule_groups
        for r in g.rules
        if r.attribute == "Date of Birth"
    )


UPSC_AGE = (
    "A candidate must have attained the age of 21 years and must not have "
    "attained the age of 32 years on the 1st of August, 2025."
)

UPSC_RELAXATION = (
    "The upper age limit prescribed above will be relaxable up to a maximum "
    "of five years if a candidate belongs to a Scheduled Caste or a "
    "Scheduled Tribe.\n"
    "Up to a maximum of three years in the case of candidates belonging to "
    "Other Backward Classes."
)

UPSC_NATIONALITY = (
    "A candidate must be: (a) a citizen of India, or (b) a subject of Nepal, "
    "or (c) a subject of Bhutan, or (d) a person of Indian origin who has "
    "migrated from Pakistan, Burma, Sri Lanka."
)

UPSC_DEGREE = (
    "A candidate must hold a degree of any of the Universities incorporated "
    "by an Act of the Central or State Legislature in India."
)


def _upsc_draft(**overrides):
    quote = (
        "must have attained the age of 21 years and must not have attained "
        "the age of 32 years on the 1st of August, 2025"
    )

    values = dict(
        age_limits=[
            facts.AgeLimit(kind="minimum", years=21, as_on_date="2025-08-01",
                           quote=quote, passage="P1"),
            facts.AgeLimit(kind="maximum", years=32, as_on_date="2025-08-01",
                           quote=quote, passage="P1"),
            facts.AgeLimit(
                kind="maximum", years=37, as_on_date="2025-08-01",
                quote="up to a maximum of five years if a candidate belongs "
                      "to a Scheduled Caste or a Scheduled Tribe",
                passage="P2"),
            facts.AgeLimit(
                kind="maximum", years=35, as_on_date="2025-08-01",
                quote="in the case of candidates belonging to Other "
                      "Backward Classes",
                passage="P2"),
        ],
        qualifications=[facts.QualificationFact(level="Bachelor's")],
        nationalities=[
            "India", "Nepal", "Bhutan",
            "Indian origin (from Pakistan, Burma, Sri Lanka)",
        ],
        nationality_quote=(
            "A candidate must be: (a) a citizen of India, or (b) a subject "
            "of Nepal, or (c) a subject of Bhutan"
        ),
        nationality_passage="P3",
        work_experience=facts.Fact(),
    )

    values.update(overrides)

    return facts.EligibilityDraft(**values)


# ---------------------------------------------------------------------------
# age arithmetic
# ---------------------------------------------------------------------------

def test_not_attained_is_exclusive():
    assert is_exclusive("maximum", "must not have attained the age of 32 years")
    assert is_exclusive("maximum", "below 32 years")
    assert not is_exclusive("maximum", "must not exceed 32 years")
    assert not is_exclusive("maximum", "up to 32 years of age")
    assert not is_exclusive("minimum", "must have attained the age of 21")


def test_dob_boundaries_for_upsc_2025():
    reference = date(2025, 8, 1)

    assert dob_boundary("minimum", 21, reference) == ("<=", date(2004, 8, 1))
    assert dob_boundary("maximum", 32, reference, exclusive=True) == (
        ">=", date(1993, 8, 2)
    )
    # inclusive wording gives the older boundary
    assert dob_boundary("maximum", 32, reference) == (">=", date(1992, 8, 2))


def test_day_with_of_is_a_date():
    assert date_set("on the 1st of August, 2025") == {date(2025, 8, 1)}


def test_explicit_birth_dates_are_parsed():
    found = parse_explicit_dob_limits(
        "born not earlier than 2nd August, 1993 and not later than "
        "1st August, 2004"
    )

    assert found["earliest"][0] == date(1993, 8, 2)
    assert found["latest"][0] == date(2004, 8, 1)


def test_application_deadline_is_not_a_birth_limit():
    found = parse_explicit_dob_limits(
        "Last date for receipt of applications: not later than 11.02.2025."
    )

    assert found["earliest"] is None
    assert found["latest"] is None


def test_reference_date_needs_to_be_unambiguous():
    assert find_age_reference_date(UPSC_AGE) == date(2025, 8, 1)
    assert find_age_reference_date(
        "Age as on 01.08.2025 for posts A. Age as on 01.01.2026 for posts B."
    ) is None


# ---------------------------------------------------------------------------
# compiler
# ---------------------------------------------------------------------------

def test_upsc_age_limits_and_concessions():
    info, rules, grounder = _compile(
        _upsc_draft(),
        _passage(1, UPSC_AGE),
        _passage(2, UPSC_RELAXATION),
        _passage(3, UPSC_NATIONALITY),
        _passage(4, UPSC_DEGREE),
    )

    assert _dob_rules(rules) == [
        ("<=", "2004-08-01"),
        (">=", "1993-08-02"),
    ]

    assert info.minimum_age == 21
    assert info.maximum_age == 31

    # SC/ST and OBC concessions are not competing values of the same limit
    assert grounder.conflicts == []
    assert any("Age maximum 37" in text for text in info.other_requirements)
    assert any("Age maximum 35" in text for text in info.other_requirements)


def test_missing_qualification_quote_is_recovered():
    info, rules, grounder = _compile(
        _upsc_draft(),
        _passage(1, UPSC_AGE),
        _passage(2, UPSC_RELAXATION),
        _passage(3, UPSC_NATIONALITY),
        _passage(4, UPSC_DEGREE),
    )

    levels = [
        r.value
        for g in rules.rule_groups
        for child in g.child_groups
        for r in child.rules
        if r.attribute == "Educational Qualification"
    ]

    assert levels == ["Bachelor's"]
    assert any(i.code == "quote-recovered" for i in grounder.issues)


def test_free_text_nationality_is_not_a_rule():
    info, rules, _ = _compile(
        _upsc_draft(),
        _passage(1, UPSC_AGE),
        _passage(2, UPSC_RELAXATION),
        _passage(3, UPSC_NATIONALITY),
        _passage(4, UPSC_DEGREE),
    )

    countries = [
        r.value
        for g in rules.rule_groups
        for child in g.child_groups
        for r in child.rules
        if r.attribute == "Nationality"
    ]

    assert countries == ["India", "Nepal", "Bhutan"]
    assert info.nationality == "India, Nepal, Bhutan"
    assert any(
        text.startswith("Nationality: Indian origin")
        for text in info.other_requirements
    )


def test_notice_birth_dates_replace_calculated_ones():
    explicit = (
        "Candidates must have been born not earlier than 2nd August, 1993 "
        "and not later than 1st August, 2004."
    )

    _, rules, _ = _compile(
        _upsc_draft(),
        _passage(1, UPSC_AGE + " " + explicit),
        _passage(2, UPSC_RELAXATION),
        _passage(3, UPSC_NATIONALITY),
        _passage(4, UPSC_DEGREE),
    )

    assert _dob_rules(rules) == [
        ("<=", "2004-08-01"),
        (">=", "1993-08-02"),
    ]


def test_age_range_quote_and_reference_date_from_notice():
    text = "Age limit: 18-27 years (as on 01-08-2026)."

    draft = facts.EligibilityDraft(
        age_limits=[
            facts.AgeLimit(kind="minimum", years=18,
                           quote="Age limit: 18-27 years (as on 01-08-2026)",
                           passage="P1"),
            facts.AgeLimit(kind="maximum", years=27,
                           quote="Age limit: 18-27 years (as on 01-08-2026)",
                           passage="P1"),
        ],
        work_experience=facts.Fact(),
    )

    _, rules, _ = _compile(draft, _passage(1, text))

    assert _dob_rules(rules) == [
        ("<=", "2008-08-01"),
        (">=", "1998-08-02"),
    ]


def test_paraphrased_requirement_is_kept_when_numbers_match():
    text = "Candidates must have been born not earlier than 02.08.1996."

    draft = facts.EligibilityDraft(
        other_requirements=[
            facts.TextItem(
                text="Born on or after 2 August 1996",
                quote="born not earlier than 02.08.1996",
                passage="P1",
            ),
            facts.TextItem(
                text="Born on or after 2 August 1990",
                quote="born not earlier than 02.08.1996",
                passage="P1",
            ),
        ],
        work_experience=facts.Fact(),
    )

    info, _, _ = _compile(draft, _passage(1, text))

    assert info.other_requirements == ["Born on or after 2 August 1996"]


def test_no_nationality_means_no_nationality_warning():
    draft = facts.EligibilityDraft(work_experience=facts.Fact())

    _, _, grounder = _compile(draft, _passage(1, "Eligibility."))

    assert not any(i.field == "Nationality" for i in grounder.issues)


# ---------------------------------------------------------------------------
# normalizer
# ---------------------------------------------------------------------------

def test_wrapper_groups_are_flattened_and_free_text_dropped():
    tree = EligibilityRulesData(rule_groups=[
        EligibilityRuleGroupData(
            logical_operator="AND",
            rules=[],
            child_groups=[
                EligibilityRuleGroupData(
                    logical_operator="AND",
                    rules=[
                        EligibilityRuleData(attribute="Date of Birth",
                                            operator="<=", value="2004-08-01"),
                    ],
                    child_groups=[
                        EligibilityRuleGroupData(
                            logical_operator="OR",
                            rules=[
                                EligibilityRuleData(
                                    attribute="Nationality", operator="=",
                                    value="India"),
                                EligibilityRuleData(
                                    attribute="Nationality", operator="=",
                                    value="Indian origin (from Pakistan, "
                                          "Burma)"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ])

    result = normalize_eligibility_rules(tree)

    assert len(result.rule_groups) == 1

    top = result.rule_groups[0]

    assert top.logical_operator == "AND"
    assert [r.attribute for r in top.rules] == ["Date of Birth"]
    assert len(top.child_groups) == 1
    assert [r.value for r in top.child_groups[0].rules] == ["India"]


def test_group_with_nothing_left_is_dropped():
    tree = EligibilityRulesData(rule_groups=[
        EligibilityRuleGroupData(
            logical_operator="OR",
            rules=[
                EligibilityRuleData(attribute="Nationality", operator="=",
                                    value="Indian origin (from Pakistan)"),
            ],
        ),
    ])

    assert normalize_eligibility_rules(tree).rule_groups == []


# ---------------------------------------------------------------------------
# evaluation
# ---------------------------------------------------------------------------

def _rule(attribute, operator, value, data_type="text"):
    return NS(
        attribute=NS(attribute_name=attribute, data_type=data_type),
        operator=operator,
        value=value,
    )


def _student(nationality="Indian", dob=date(1990, 1, 1), qualification="B.Tech"):
    return NS(
        nationality=nationality,
        state=None,
        gender=None,
        date_of_birth=dob,
        educations=[NS(is_current=True, qualification=qualification,
                       cgpa=None, percentage=None, specialization=None,
                       current_year=None, year_of_passing=None)],
        work_experiences=[],
    )


def _nationality_group():
    return _RuleGroupNode(
        "OR",
        [_rule("Nationality", "=", c) for c in ("India", "Nepal", "Bhutan")],
        [],
    )


def test_satisfied_or_group_does_not_list_unmet_alternatives():
    group = _RuleGroupNode(
        "AND",
        [_rule("Date of Birth", ">=", "1993-08-02", "date")],
        [_nationality_group()],
    )

    result = _evaluate_rule_group(_student(), group)

    assert result.eligible is False
    assert len(result.reasons) == 1
    assert "Date of Birth" in result.reasons[0]
    assert not any("Nepal" in r or "Bhutan" in r for r in result.reasons)


def test_empty_wrapper_group_is_ignored():
    group = _RuleGroupNode(
        "AND",
        [],
        [
            _RuleGroupNode("AND", [], []),
            _nationality_group(),
        ],
    )

    assert _evaluate_rule_group(_student(), group).eligible is True


def test_higher_qualification_meets_a_bachelors_requirement():
    rule = _rule("Educational Qualification", "=", "Bachelor's")

    assert check_rule(_student(qualification="B.Tech"), rule) is True
    assert check_rule(_student(qualification="Master's"), rule) is True
    assert check_rule(_student(qualification="PhD"), rule) is True
    assert check_rule(_student(qualification="12th"), rule) is False


def test_notice_without_release_date_can_still_be_used():
    exam = NS(official_notifications=[
        NS(approval_status="APPROVED", release_date=None, notification_id=3),
        NS(approval_status="APPROVED", release_date=None, notification_id=4),
        NS(approval_status="PENDING", release_date=date(2026, 1, 1),
           notification_id=5),
    ])

    assert _get_latest_approved_notification(exam).notification_id == 4


def test_dated_notice_still_beats_newer_undated_one():
    exam = NS(official_notifications=[
        NS(approval_status="APPROVED", release_date=date(2025, 1, 22),
           notification_id=1),
        NS(approval_status="APPROVED", release_date=None, notification_id=2),
    ])

    assert _get_latest_approved_notification(exam).notification_id == 1


# ---------------------------------------------------------------------------
# SSC JE style notice: limits differ by post, nationality sentence
# ---------------------------------------------------------------------------

SSC_AGE = (
    "For the posts for which the age limit is up to 30 years | Candidate "
    "must have been born not earlier than 02.08.1996 and not later than "
    "01.08.2008. For the posts for which the age limit is up to 32 years | "
    "Candidate must have been born not earlier than 02.08.1994 and not "
    "later than 01.08.2008."
)

SSC_NATIONALITY = (
    "6.1 A candidate must be either: (a) a citizen of India, or (b) a "
    "subject of Nepal, or (c) a subject of Bhutan, or (d) a person of "
    "Indian origin who has migrated from Pakistan, Burma, Sri Lanka, East "
    "African countries of Kenya, Uganda, the United Republic of Tanzania, "
    "Zambia, Malawi, Zaire, Ethiopia, and Vietnam with the intention of "
    "permanently settling in India."
)


def test_post_wise_birth_dates_use_the_most_generous_limit():
    found = parse_explicit_dob_limits(SSC_AGE)

    assert found["earliest"][0] == date(1994, 8, 2)
    assert found["latest"][0] == date(2008, 8, 1)
    assert found["varies"] is True


def test_post_wise_birth_dates_are_reported_by_the_compiler():
    draft = facts.EligibilityDraft(work_experience=facts.Fact())

    _, rules, grounder = _compile(draft, _passage(1, SSC_AGE))

    assert _dob_rules(rules) == [
        ("<=", "2008-08-01"),
        (">=", "1994-08-02"),
    ]
    assert any(i.code == "dob-varies-by-post" for i in grounder.issues)


def test_countries_people_migrated_from_are_not_nationalities():
    draft = facts.EligibilityDraft(
        nationalities=[
            "India", "Nepal", "Bhutan", "Pakistan", "Burma", "Sri Lanka",
            "Kenya", "Uganda", "Tanzania", "Zambia", "Malawi", "Zaire",
            "Ethiopia", "Vietnam",
        ],
        nationality_quote=SSC_NATIONALITY[:300],
        nationality_passage="P1",
        work_experience=facts.Fact(),
    )

    info, rules, _ = _compile(draft, _passage(1, SSC_NATIONALITY))

    countries = [
        r.value
        for g in rules.rule_groups
        for child in g.child_groups
        for r in child.rules
        if r.attribute == "Nationality"
    ]

    assert countries == ["India", "Nepal", "Bhutan"]
    assert info.nationality == "India, Nepal, Bhutan"
    assert any(
        "migrated from Pakistan" in text for text in info.other_requirements
    )