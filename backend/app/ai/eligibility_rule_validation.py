from datetime import date

from app.ai.eligibility_schemas import (
    EligibilityRuleData,
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
    "IN",
}


SUPPORTED_LOGICAL_OPERATORS = {
    "AND",
    "OR",
}


def validate_eligibility_rules(
    data: EligibilityRulesData,
) -> list[str]:

    errors = []

    for group_index, group in enumerate(
        data.rule_groups,
        start=1
    ):

        # -----------------------------------------
        # Validate logical operator
        # -----------------------------------------

        if group.logical_operator not in SUPPORTED_LOGICAL_OPERATORS:
            errors.append(
                f"Group {group_index}: "
                f"Unsupported logical operator "
                f"'{group.logical_operator}'."
            )

        # -----------------------------------------
        # Validate rules
        # -----------------------------------------

        for rule_index, rule in enumerate(
            group.rules,
            start=1
        ):

            if rule.attribute not in SUPPORTED_ATTRIBUTES:
                errors.append(
                    f"Group {group_index}, Rule {rule_index}: "
                    f"Unsupported attribute "
                    f"'{rule.attribute}'."
                )

            if rule.operator not in SUPPORTED_OPERATORS:
                errors.append(
                    f"Group {group_index}, Rule {rule_index}: "
                    f"Unsupported operator "
                    f"'{rule.operator}'."
                )

            if not rule.value.strip():
                errors.append(
                    f"Group {group_index}, Rule {rule_index}: "
                    "Rule value cannot be empty."
                )

            # -------------------------------------
            # Numeric validation
            # -------------------------------------

            if rule.attribute in {
                "CGPA",
                "Percentage",
            }:
                try:
                    float(rule.value)
                except ValueError:
                    errors.append(
                        f"Group {group_index}, Rule {rule_index}: "
                        f"{rule.attribute} must be numeric."
                    )

            # -------------------------------------
            # Date validation
            # -------------------------------------

            if rule.attribute == "Date of Birth":

                try:
                    date.fromisoformat(
                        rule.value
                    )
                except ValueError:
                    errors.append(
                        f"Group {group_index}, Rule {rule_index}: "
                        "Date of Birth must use YYYY-MM-DD format."
                    )

    return errors