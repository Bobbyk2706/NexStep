from __future__ import annotations

"""
Administrator-entered eligibility.

The AI cannot extract eligibility from every notice (scanned pages, tables
that vary by post, wording it does not understand). This module lets an
administrator enter or correct it on the extraction page, using exactly the
same normalization and validation as AI-extracted rules, so manual rules can
never be less safe than automatic ones.
"""

from pydantic import BaseModel, Field

from app.ai.aggregated_extraction_result import (
    AggregatedExtractionResult,
    ExtractionIssue,
)
from app.ai.complete_extraction_validation import (
    validate_complete_extraction,
)
from app.ai.eligibility_rule_normalizer import (
    normalize_eligibility_rules,
)
from app.ai.eligibility_rule_validation import (
    validate_eligibility_rules,
)
from app.ai.eligibility_schemas import (
    EligibilityRuleGroupData,
    EligibilityRulesData,
)
from app.ai.exam_schemas import EligibilityInformation
from app.ai.extraction_schemas import CompleteExtractionData


# The message validate_eligibility_rules() gives for an empty rule tree.
# An administrator may knowingly approve an exam whose notification states
# no eligibility, so this one message is waived in that case.
NO_RULE_GROUP_MESSAGE = (
    "Eligibility rules must contain at least one rule group."
)

MANUAL_ISSUE_CODE = "eligibility-manual"


class ManualEligibilityError(ValueError):
    """The administrator's eligibility is not valid. Carries every problem."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


class ManualEligibility(BaseModel):
    minimum_age: int | None = Field(default=None, ge=0, le=120)
    maximum_age: int | None = Field(default=None, ge=0, le=120)
    educational_qualification: str | None = None
    nationality: str | None = None
    work_experience: str | None = None
    other_requirements: list[str] = Field(default_factory=list)
    rule_groups: list[EligibilityRuleGroupData] = Field(default_factory=list)

    # True when the notification states no eligibility at all. Students then
    # see "check the official notification" instead of a verdict.
    not_available: bool = False


def _clean(value: str | None) -> str | None:
    value = (value or "").strip()

    return value or None


def _clean_list(values: list[str]) -> list[str]:
    out: list[str] = []

    for value in values:
        value = (value or "").strip()

        if value and value not in out:
            out.append(value)

    return out


def apply_manual_eligibility(
    result: AggregatedExtractionResult,
    manual: ManualEligibility,
) -> AggregatedExtractionResult:
    """
    Return a copy of `result` carrying the administrator's eligibility.

    Raises ManualEligibilityError when the input is not acceptable.
    """

    errors: list[str] = []

    if (
        manual.minimum_age is not None
        and manual.maximum_age is not None
        and manual.minimum_age > manual.maximum_age
    ):
        errors.append("Minimum age cannot be greater than maximum age.")

    try:
        rules = normalize_eligibility_rules(
            EligibilityRulesData(rule_groups=manual.rule_groups)
        )
    except ValueError as error:
        raise ManualEligibilityError(errors + [str(error)]) from error

    if manual.not_available:
        if rules.rule_groups:
            errors.append(
                "Either mark the eligibility as not stated in the "
                "notification, or enter rules - not both."
            )
    else:
        errors.extend(validate_eligibility_rules(rules))

    if errors:
        raise ManualEligibilityError(errors)

    information = EligibilityInformation(
        minimum_age=manual.minimum_age,
        maximum_age=manual.maximum_age,
        educational_qualification=_clean(manual.educational_qualification),
        nationality=_clean(manual.nationality),
        work_experience=_clean(manual.work_experience),
        other_requirements=_clean_list(manual.other_requirements),
    )

    exam_information = result.extraction.exam_information.model_copy(
        update={"eligibility": information}
    )

    extraction = CompleteExtractionData(
        exam_information=exam_information,
        eligibility_rules=rules,
    )

    # Re-run the approval gates on the new content. Errors the pipeline
    # recorded earlier ("validation") are replaced by fresh ones; warnings
    # about what the AI could not read are kept for the reviewer.
    issues = [
        issue
        for issue in result.issues
        if issue.code not in ("validation", MANUAL_ISSUE_CODE)
    ]

    for message in validate_complete_extraction(extraction):
        if manual.not_available and message == NO_RULE_GROUP_MESSAGE:
            continue

        issues.append(
            ExtractionIssue(
                severity="error",
                code="validation",
                message=message,
            )
        )

    issues.append(
        ExtractionIssue(
            severity="info",
            code=MANUAL_ISSUE_CODE,
            message=(
                "Eligibility was entered by an administrator: the "
                "notification states no eligibility."
                if manual.not_available
                else "Eligibility was entered or edited by an administrator."
            ),
        )
    )

    pipeline = dict(result.pipeline)
    pipeline["eligibility_source"] = "ADMIN"
    pipeline["eligibility_not_available"] = manual.not_available

    return AggregatedExtractionResult(
        extraction=extraction,
        evidence=result.evidence,
        conflicts=result.conflicts,
        issues=issues,
        pipeline=pipeline,
    )
