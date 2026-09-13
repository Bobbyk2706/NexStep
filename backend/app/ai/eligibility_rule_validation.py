from datetime import date

from app.ai.eligibility_schemas import (
    EligibilityRuleGroupData,
    EligibilityRulesData,
)


SUPPORTED_ATTRIBUTES = {
    "CGPA",
    "Percentage",
    "Specialization",
    "Date of Birth",
    "Nationality",
    "State",
    "Educational Qualification",
    "Work Experience",
}

SUPPORTED_OPERATORS = {
    "=",
    "!=",
    ">",
    ">=",
    "<",
    "<=",
}

SUPPORTED_LOGICAL_OPERATORS = {
    "AND",
    "OR",
}


def validate_rule_group(
    group: EligibilityRuleGroupData,
    path: str,
    errors: list[str]
):
    # Validate logical operator
    if group.logical_operator not in SUPPORTED_LOGICAL_OPERATORS:
        errors.append(
            f"{path}: Unsupported logical operator "
            f"'{group.logical_operator}'."
        )

    # A group must contain at least one rule or child group
    if not group.rules and not group.child_groups:
        errors.append(
            f"{path}: Rule group cannot be empty."
        )

    # Validate rules
    for rule_index, rule in enumerate(
        group.rules,
        start=1
    ):
        rule_path = f"{path}, Rule {rule_index}"

        if rule.attribute not in SUPPORTED_ATTRIBUTES:
            errors.append(
                f"{rule_path}: Unsupported attribute "
                f"'{rule.attribute}'."
            )

        if rule.operator not in SUPPORTED_OPERATORS:
            errors.append(
                f"{rule_path}: Unsupported operator "
                f"'{rule.operator}'."
            )

        if not rule.value.strip():
            errors.append(
                f"{rule_path}: Rule value cannot be empty."
            )

        # Numeric validation
        if rule.attribute in {
            "CGPA",
            "Percentage"
        }:
            try:
                float(rule.value)
            except ValueError:
                errors.append(
                    f"{rule_path}: {rule.attribute} "
                    "must be numeric."
                )

        # Date validation
        if rule.attribute == "Date of Birth":
            try:
                date.fromisoformat(rule.value)
            except ValueError:
                errors.append(
                    f"{rule_path}: Date of Birth must "
                    "use YYYY-MM-DD format."
                )

    # Recursively validate child groups
    for child_index, child_group in enumerate(
        group.child_groups,
        start=1
    ):
        child_path = (
            f"{path}, Child Group {child_index}"
        )

        validate_rule_group(
            group=child_group,
            path=child_path,
            errors=errors
        )


def validate_eligibility_rules(
    data: EligibilityRulesData,
) -> list[str]:

    errors = []

    if not data.rule_groups:
        errors.append(
            "Eligibility rules must contain at least "
            "one rule group."
        )

    for group_index, group in enumerate(
        data.rule_groups,
        start=1
    ):
        validate_rule_group(
            group=group,
            path=f"Group {group_index}",
            errors=errors
        )

    return errors