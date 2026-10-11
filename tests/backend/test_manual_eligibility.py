"""
Administrator-entered eligibility: the same normalization and validation as
AI-extracted rules, and the approval gates are re-run on the new content.
"""

import pytest

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
    ExtractionIssue,
)
from app.ai.eligibility_schemas import (
    EligibilityRuleData,
    EligibilityRuleGroupData,
    EligibilityRulesData,
)
from app.ai.exam_schemas import EligibilityInformation, ExamInformation
from app.ai.extraction_schemas import CompleteExtractionData
from app.ai.manual_eligibility import (
    MANUAL_ISSUE_CODE,
    NO_RULE_GROUP_MESSAGE,
    ManualEligibility,
    ManualEligibilityError,
    apply_manual_eligibility,
)


def _empty_result() -> AggregatedExtractionResult:
    """What discovery stores when the AI found no eligibility at all."""

    information = ExamInformation(
        exam_name="Junior Engineer Examination, 2026",
        conducting_body="Staff Selection Commission",
        eligibility=EligibilityInformation(),
    )

    return AggregatedExtractionResult(
        extraction=CompleteExtractionData(
            exam_information=information,
            eligibility_rules=EligibilityRulesData(),
        ),
        evidence=[],
        issues=[
            ExtractionIssue(
                severity="error",
                code="validation",
                message=NO_RULE_GROUP_MESSAGE,
            ),
            ExtractionIssue(
                severity="warning",
                code="no-eligibility-section",
                message="No eligibility section found.",
            ),
        ],
    )


def _group(*rules, operator="AND"):
    return EligibilityRuleGroupData(
        logical_operator=operator,
        rules=[
            EligibilityRuleData(attribute=a, operator=o, value=v)
            for a, o, v in rules
        ],
    )


def test_manual_rules_clear_the_blocking_error():
    manual = ManualEligibility(
        minimum_age=21,
        maximum_age=31,
        educational_qualification="Bachelor's degree",
        nationality="India",
        other_requirements=["  Medical standards apply  ", ""],
        rule_groups=[
            _group(
                ("Date of Birth", "<=", "2004-08-01"),
                ("Date of Birth", ">=", "1993-08-02"),
                ("Nationality", "=", "India"),
            )
        ],
    )

    updated = apply_manual_eligibility(_empty_result(), manual)

    assert updated.blocking_issues == []
    assert updated.pipeline["eligibility_source"] == "ADMIN"
    assert updated.pipeline["eligibility_not_available"] is False

    codes = [issue.code for issue in updated.issues]
    assert MANUAL_ISSUE_CODE in codes
    # Warnings about what the AI could not read stay for the reviewer.
    assert "no-eligibility-section" in codes

    eligibility = updated.extraction.exam_information.eligibility
    assert eligibility.minimum_age == 21
    assert eligibility.other_requirements == ["Medical standards apply"]


def test_invalid_rule_is_rejected_with_the_reason():
    manual = ManualEligibility(
        rule_groups=[_group(("Date of Birth", "LIKE", "2004-08-01"))]
    )

    with pytest.raises(ManualEligibilityError):
        apply_manual_eligibility(_empty_result(), manual)


def test_unsupported_attribute_is_rejected():
    manual = ManualEligibility(
        rule_groups=[_group(("Age", ">=", "21"))]
    )

    with pytest.raises(ManualEligibilityError):
        apply_manual_eligibility(_empty_result(), manual)


def test_nothing_entered_is_not_accepted_silently():
    with pytest.raises(ManualEligibilityError) as caught:
        apply_manual_eligibility(_empty_result(), ManualEligibility())

    assert NO_RULE_GROUP_MESSAGE in caught.value.errors


def test_not_stated_in_notification_is_allowed_without_rules():
    updated = apply_manual_eligibility(
        _empty_result(),
        ManualEligibility(not_available=True),
    )

    assert updated.blocking_issues == []
    assert updated.pipeline["eligibility_not_available"] is True


def test_not_stated_cannot_be_combined_with_rules():
    manual = ManualEligibility(
        not_available=True,
        rule_groups=[_group(("Nationality", "=", "India"))],
    )

    with pytest.raises(ManualEligibilityError):
        apply_manual_eligibility(_empty_result(), manual)


def test_minimum_age_cannot_exceed_maximum_age():
    manual = ManualEligibility(
        minimum_age=40,
        maximum_age=30,
        rule_groups=[_group(("Nationality", "=", "India"))],
    )

    with pytest.raises(ManualEligibilityError) as caught:
        apply_manual_eligibility(_empty_result(), manual)

    assert any("Minimum age" in error for error in caught.value.errors)


def test_editing_twice_does_not_pile_up_notes():
    manual = ManualEligibility(
        rule_groups=[_group(("Nationality", "=", "India"))]
    )

    once = apply_manual_eligibility(_empty_result(), manual)
    twice = apply_manual_eligibility(once, manual)

    assert [i.code for i in twice.issues].count(MANUAL_ISSUE_CODE) == 1
