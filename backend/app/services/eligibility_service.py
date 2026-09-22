from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.session import SessionLocal
from app.models.exam import Exam
from app.models.official_notification import OfficialNotification
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.eligibility_rule import EligibilityRule
from app.services.rule_evaluator import evaluate_rule


# ============================================================
# EVALUATION RESULT
# ============================================================


@dataclass(frozen=True)
class EligibilityEvaluation:
    """
    Result of evaluating an exam's eligibility rules.
    """

    eligible: bool
    reasons: list[str]


# ============================================================
# ATTRIBUTE HELPERS
# ============================================================


def _normalize_attribute_name(
    attribute_name: str,
) -> str:
    """
    Normalize eligibility attribute names.

    Examples:

        "Date of Birth" -> "date of birth"
        "CGPA"          -> "cgpa"
    """

    return " ".join(
        attribute_name.strip().lower().split()
    )


def get_student_value(
    student,
    attribute_name: str,
):
    """
    Get a value from the Student model.
    """

    attribute = _normalize_attribute_name(
        attribute_name
    )

    if attribute == "nationality":
        return student.nationality

    if attribute == "state":
        return student.state

    if attribute == "gender":
        return student.gender

    if attribute == "date of birth":
        return student.date_of_birth

    raise ValueError(
        f"Unsupported student attribute: {attribute_name}"
    )


def get_current_education(student):
    """
    Return the student's current education record.
    """

    education = next(
        (
            edu
            for edu in student.educations
            if edu.is_current
        ),
        None,
    )

    if education is None:
        raise ValueError(
            "Student has no current education."
        )

    return education


def get_education_value(
    student,
    attribute_name: str,
):
    """
    Get a value from the student's current education.
    """

    education = get_current_education(
        student
    )

    attribute = _normalize_attribute_name(
        attribute_name
    )

    if attribute == "cgpa":
        return education.cgpa

    if attribute == "percentage":
        return education.percentage

    if attribute in {
        "qualification",
        "educational qualification",
    }:
        return education.qualification

    if attribute == "specialization":
        return education.specialization

    if attribute == "current year":
        return education.current_year

    if attribute == "year of passing":
        return education.year_of_passing

    raise ValueError(
        f"Unsupported education attribute: {attribute_name}"
    )


def get_work_experience_values(
    student,
) -> list[str]:
    """
    Return non-empty work-experience duration values.

    WorkExperience.duration is currently stored as text.
    """

    return [
        work.duration
        for work in student.work_experiences
        if work.duration
        and work.duration.strip()
    ]


# ============================================================
# RULE GROUP LOADING
# ============================================================


def _get_latest_approved_notification(
    exam: Exam,
):
    """
    Select the latest approved official notification.

    Pending/rejected notifications must never be used as the
    source of truth for student eligibility.
    """

    approved_notifications = [
        notification
        for notification
        in exam.official_notifications
        if notification.approval_status == "APPROVED"
    ]

    if not approved_notifications:
        raise ValueError(
            "No approved official notification found."
        )

    notifications_with_dates = [
        notification
        for notification
        in approved_notifications
        if notification.release_date is not None
    ]

    if not notifications_with_dates:
        raise ValueError(
            "No approved official notification has a release date."
        )

    return max(
        notifications_with_dates,
        key=lambda notification: notification.release_date,
    )


@dataclass
class _RuleGroupNode:
    """
    In-memory representation of the complete recursive
    eligibility rule tree.

    This avoids relying on detached SQLAlchemy relationships
    after the database session closes.
    """

    logical_operator: str
    rules: list
    child_groups: list["_RuleGroupNode"]


def get_exam_rule_groups(
    exam_id: int,
    db: Session | None = None,
) -> list[_RuleGroupNode]:
    """
    Load the complete eligibility rule tree for the latest
    approved notification.

    If db is supplied, the caller's session is reused.
    Otherwise a temporary session is created.
    """

    owns_session = db is None

    if owns_session:
        db = SessionLocal()

    try:
        exam = db.scalar(
            select(Exam)
            .options(
                selectinload(
                    Exam.official_notifications
                )
            )
            .where(
                Exam.exam_id == exam_id
            )
        )

        if exam is None:
            raise ValueError(
                "Exam not found."
            )

        notification = (
            _get_latest_approved_notification(
                exam
            )
        )

        groups = db.scalars(
            select(EligibilityRuleGroup)
            .options(
                selectinload(
                    EligibilityRuleGroup.rules
                ).selectinload(
                    EligibilityRule.attribute
                )
            )
            .where(
                EligibilityRuleGroup.notification_id
                == notification.notification_id
            )
            .order_by(
                EligibilityRuleGroup.group_id
            )
        ).all()

        if not groups:
            raise ValueError(
                "No eligibility rule groups found."
            )

        group_by_id = {
            group.group_id: group
            for group in groups
        }

        children_by_parent: dict[
            int,
            list[EligibilityRuleGroup],
        ] = {}

        top_level_groups = []

        for group in groups:

            if group.parent_group_id is None:
                top_level_groups.append(group)

            else:
                if (
                    group.parent_group_id
                    not in group_by_id
                ):
                    raise ValueError(
                        "Eligibility rule group references "
                        "a missing parent group."
                    )

                children_by_parent.setdefault(
                    group.parent_group_id,
                    [],
                ).append(group)

        def build_node(
            group: EligibilityRuleGroup,
        ) -> _RuleGroupNode:

            logical_operator = (
                group.logical_operator
                .strip()
                .upper()
            )

            if logical_operator not in {
                "AND",
                "OR",
            }:
                raise ValueError(
                    "Unsupported logical operator: "
                    f"{group.logical_operator}"
                )

            children = sorted(
                children_by_parent.get(
                    group.group_id,
                    [],
                ),
                key=lambda child: (
                    child.group_number,
                    child.group_id,
                ),
            )

            return _RuleGroupNode(
                logical_operator=logical_operator,
                rules=list(group.rules),
                child_groups=[
                    build_node(child)
                    for child in children
                ],
            )

        top_level_groups = sorted(
            top_level_groups,
            key=lambda group: (
                group.group_number,
                group.group_id,
            ),
        )

        return [
            build_node(group)
            for group in top_level_groups
        ]

    finally:
        if owns_session:
            db.close()


# ============================================================
# VALUE CONVERSION
# ============================================================


def _parse_rule_date(
    value: str,
) -> date:
    """
    Parse an ISO date from an eligibility rule.
    """

    try:
        return date.fromisoformat(
            value.strip()
        )
    except ValueError as error:
        raise ValueError(
            f"Invalid eligibility date: {value}"
        ) from error


def _convert_rule_value(
    rule,
    student_value,
):
    """
    Convert the extracted rule value according to the
    EligibilityAttribute data type.
    """

    if rule.attribute.data_type == "numeric":

        try:
            return float(
                rule.value
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                "Invalid numeric eligibility value: "
                f"{rule.value}"
            ) from error

    if rule.attribute.data_type == "date":

        rule_value = _parse_rule_date(
            rule.value
        )

        if not isinstance(
            student_value,
            date,
        ):
            raise ValueError(
                "Student date-of-birth value is not "
                "a valid date."
            )

        return rule_value

    return rule.value


# ============================================================
# WORK EXPERIENCE
# ============================================================


def _evaluate_work_experience_rule(
    student,
    operator: str,
    rule_value: str,
) -> bool:
    """
    Evaluate Work Experience conservatively.

    WorkExperience.duration is currently text, so only exact
    text equality/inequality is supported.

    Numeric ordering is rejected rather than interpreted.
    """

    durations = get_work_experience_values(
        student
    )

    normalized_rule_value = (
        rule_value.strip().lower()
    )

    normalized_durations = [
        duration.strip().lower()
        for duration in durations
    ]

    if operator == "=":
        return any(
            duration == normalized_rule_value
            for duration in normalized_durations
        )

    if operator == "!=":
        return all(
            duration != normalized_rule_value
            for duration in normalized_durations
        )

    raise ValueError(
        "Ordering operators are not supported for "
        "Work Experience because duration is currently "
        "stored as text."
    )


# ============================================================
# SINGLE RULE
# ============================================================


def _rule_description(
    rule,
) -> str:
    """
    Produce a human-readable description of a rule.
    """

    return (
        f"{rule.attribute.attribute_name} "
        f"{rule.operator} "
        f"{rule.value}"
    )


def check_rule(
    student,
    rule,
) -> bool:
    """
    Evaluate one eligibility rule.
    """

    attribute_name = (
        rule.attribute.attribute_name
    )

    attribute = _normalize_attribute_name(
        attribute_name
    )

    operator = rule.operator.strip()

    # --------------------------------------------------------
    # Work Experience
    # --------------------------------------------------------

    if attribute == "work experience":
        return _evaluate_work_experience_rule(
            student,
            operator,
            rule.value,
        )

    # --------------------------------------------------------
    # Student-level attributes
    # --------------------------------------------------------

    if attribute in {
        "nationality",
        "state",
        "gender",
        "date of birth",
    }:

        student_value = get_student_value(
            student,
            attribute,
        )

    # --------------------------------------------------------
    # Education-level attributes
    # --------------------------------------------------------

    elif attribute in {
        "cgpa",
        "percentage",
        "qualification",
        "educational qualification",
        "specialization",
        "current year",
        "year of passing",
    }:

        student_value = get_education_value(
            student,
            attribute,
        )

    else:
        raise ValueError(
            f"Unsupported eligibility attribute: "
            f"{attribute_name}"
        )

    if student_value is None:
        raise ValueError(
            "Student information required for eligibility "
            f"rule '{attribute_name}' is missing."
        )

    rule_value = _convert_rule_value(
        rule,
        student_value,
    )

    try:
        return evaluate_rule(
            student_value,
            operator,
            rule_value,
        )
    except TypeError as error:
        raise ValueError(
            "Eligibility rule value is incompatible with "
            f"student value for attribute '{attribute_name}'."
        ) from error


# ============================================================
# RECURSIVE RULE GROUP EVALUATION
# ============================================================


def _evaluate_rule_group(
    student,
    group: _RuleGroupNode,
) -> EligibilityEvaluation:
    """
    Recursively evaluate a rule group and all child groups.
    """

    child_evaluations = []

    # --------------------------------------------------------
    # Direct rules
    # --------------------------------------------------------

    for rule in group.rules:

        result = check_rule(
            student,
            rule,
        )

        child_evaluations.append(
            (
                result,
                _rule_description(rule),
            )
        )

    # --------------------------------------------------------
    # Child groups
    # --------------------------------------------------------

    for child_group in group.child_groups:

        child_result = _evaluate_rule_group(
            student,
            child_group,
        )

        child_evaluations.append(
            (
                child_result.eligible,
                child_result.reasons,
            )
        )

    if not child_evaluations:
        raise ValueError(
            "Eligibility rule group contains no rules "
            "or child groups."
        )

    # --------------------------------------------------------
    # Logical evaluation
    # --------------------------------------------------------

    if group.logical_operator == "AND":

        eligible = all(
            result
            for result, _ in child_evaluations
        )

    elif group.logical_operator == "OR":

        eligible = any(
            result
            for result, _ in child_evaluations
        )

    else:
        raise ValueError(
            "Unsupported logical operator: "
            f"{group.logical_operator}"
        )

    # --------------------------------------------------------
    # Build reasons.
    # --------------------------------------------------------

    reasons: list[str] = []

    for result, detail in child_evaluations:

        if isinstance(detail, list):
            reasons.extend(detail)

        elif not result:
            reasons.append(
                f"Requirement not satisfied: {detail}"
            )

    return EligibilityEvaluation(
        eligible=eligible,
        reasons=reasons,
    )


# ============================================================
# PUBLIC ELIGIBILITY API
# ============================================================


def evaluate_eligibility(
    student,
    exam_id: int,
    db: Session | None = None,
) -> EligibilityEvaluation:
    """
    Evaluate a student against the latest approved rules.

    All top-level groups retain the existing NexStep
    semantics: top-level groups are combined using AND.
    """

    groups = get_exam_rule_groups(
        exam_id,
        db=db,
    )

    evaluations = [
        _evaluate_rule_group(
            student,
            group,
        )
        for group in groups
    ]

    eligible = all(
        evaluation.eligible
        for evaluation in evaluations
    )

    reasons: list[str] = []

    for evaluation in evaluations:
        reasons.extend(
            evaluation.reasons
        )

    if eligible:
        reasons = [
            "All applicable eligibility requirements "
            "were satisfied."
        ]

    elif not reasons:
        reasons = [
            "One or more eligibility requirements "
            "were not satisfied."
        ]

    return EligibilityEvaluation(
        eligible=eligible,
        reasons=reasons,
    )


def check_rule_group(
    student,
    group,
) -> bool:
    """
    Backward-compatible public wrapper.

    Returns only True/False.
    """

    result = _evaluate_rule_group(
        student,
        group,
    )

    return result.eligible


def check_eligibility(
    student,
    exam_id: int,
    db: Session | None = None,
) -> bool:
    """
    Backward-compatible eligibility API.

    Returns only True/False.
    """

    result = evaluate_eligibility(
        student,
        exam_id,
        db=db,
    )

    return result.eligible