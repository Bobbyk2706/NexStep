from datetime import date
import math

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


ATTRIBUTE_OPERATOR_RULES = {
    "CGPA": {"=", "!=", ">", ">=", "<", "<="},
    "Percentage": {"=", "!=", ">", ">=", "<", "<="},
    "Date of Birth": {"=", "!=", ">", ">=", "<", "<="},
    "Specialization": {"=", "!="},
    "Nationality": {"=", "!="},
    "State": {"=", "!="},
    "Educational Qualification": {"=", "!="},
    "Work Experience": {"=", "!="},
}


SUPPORTED_LOGICAL_OPERATORS = {
    "AND",
    "OR",
}


def validate_rule_group(
    group: EligibilityRuleGroupData,
    path: str,
    errors: list[str],
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
        start=1,
    ):
        rule_path = f"{path}, Rule {rule_index}"

        # Validate attribute
        if rule.attribute not in SUPPORTED_ATTRIBUTES:
            errors.append(
                f"{rule_path}: Unsupported attribute "
                f"'{rule.attribute}'."
            )

        # Validate operator
        if rule.operator not in SUPPORTED_OPERATORS:
            errors.append(
                f"{rule_path}: Unsupported operator "
                f"'{rule.operator}'."
            )

        elif (
            rule.attribute in ATTRIBUTE_OPERATOR_RULES
            and rule.operator
            not in ATTRIBUTE_OPERATOR_RULES[rule.attribute]
        ):
            errors.append(
                f"{rule_path}: Operator '{rule.operator}' "
                f"is not supported for attribute "
                f"'{rule.attribute}'."
            )

        # Validate value
        if not rule.value or not rule.value.strip():
            errors.append(
                f"{rule_path}: Rule value cannot be empty."
            )

        # Numeric validation
        if rule.attribute in {
            "CGPA",
            "Percentage",
        }:
            try:
                numeric_value = float(rule.value)

                # Reject NaN and infinity
                if not math.isfinite(numeric_value):
                    errors.append(
                        f"{rule_path}: {rule.attribute} "
                        "must be a finite number."
                    )

                # CGPA must be between 0 and 10
                if (
                    rule.attribute == "CGPA"
                    and math.isfinite(numeric_value)
                    and not 0 <= numeric_value <= 10
                ):
                    errors.append(
                        f"{rule_path}: CGPA must be between "
                        "0 and 10."
                    )

                # Percentage must be between 0 and 100
                if (
                    rule.attribute == "Percentage"
                    and math.isfinite(numeric_value)
                    and not 0 <= numeric_value <= 100
                ):
                    errors.append(
                        f"{rule_path}: Percentage must be between "
                        "0 and 100."
                    )

            except (ValueError, TypeError):
                errors.append(
                    f"{rule_path}: {rule.attribute} "
                    "must be numeric."
                )

        # Date validation
        if rule.attribute == "Date of Birth":
            try:
                dob_value = date.fromisoformat(rule.value)

                if dob_value > date.today():
                    errors.append(
                        f"{rule_path}: Date of Birth cannot "
                        "be in the future."
                    )

            except (ValueError, TypeError):
                errors.append(
                    f"{rule_path}: Date of Birth must "
                    "use YYYY-MM-DD format."
                )

    # Recursively validate child groups
    for child_index, child_group in enumerate(
        group.child_groups,
        start=1,
    ):
        child_path = (
            f"{path}, Child Group {child_index}"
        )

        validate_rule_group(
            group=child_group,
            path=child_path,
            errors=errors,
        )


def validate_numeric_rule_contradictions(
    group: EligibilityRuleGroupData,
    path: str,
    errors: list[str],
):
    """
    Detect impossible numeric ranges inside an AND rule group.
    """

    numeric_attributes = {
        "CGPA",
        "Percentage",
    }

    rules_by_attribute = {
        attribute: []
        for attribute in numeric_attributes
    }

    # Collect valid numeric rules by attribute
    for rule in group.rules:
        if rule.attribute not in numeric_attributes:
            continue

        try:
            value = float(rule.value)

            if not math.isfinite(value):
                continue

            rules_by_attribute[rule.attribute].append(rule)

        except (ValueError, TypeError):
            continue

    # Contradiction checking only applies to AND groups.
    if group.logical_operator == "AND":

        for attribute, rules in rules_by_attribute.items():

            lower_bounds = []
            upper_bounds = []
            exact_values = []

            for rule in rules:
                value = float(rule.value)

                if rule.operator == ">":
                    lower_bounds.append(
                        (value, False)
                    )

                elif rule.operator == ">=":
                    lower_bounds.append(
                        (value, True)
                    )

                elif rule.operator == "<":
                    upper_bounds.append(
                        (value, False)
                    )

                elif rule.operator == "<=":
                    upper_bounds.append(
                        (value, True)
                    )

                elif rule.operator == "=":
                    exact_values.append(value)

            # Check conflicting equality rules
            if exact_values:

                if len(set(exact_values)) > 1:
                    errors.append(
                        f"{path}: Contradictory {attribute} "
                        "equality rules were found."
                    )

                else:
                    exact_value = exact_values[0]

                    # Equality vs lower bound
                    for lower_value, lower_inclusive in lower_bounds:
                        if (
                            exact_value < lower_value
                            or (
                                exact_value == lower_value
                                and not lower_inclusive
                            )
                        ):
                            errors.append(
                                f"{path}: {attribute} equality "
                                "rule conflicts with a "
                                "lower-bound rule."
                            )

                    # Equality vs upper bound
                    for upper_value, upper_inclusive in upper_bounds:
                        if (
                            exact_value > upper_value
                            or (
                                exact_value == upper_value
                                and not upper_inclusive
                            )
                        ):
                            errors.append(
                                f"{path}: {attribute} equality "
                                "rule conflicts with an "
                                "upper-bound rule."
                            )

            # Check lower-bound / upper-bound conflicts
            if lower_bounds and upper_bounds:

                strongest_lower = max(
                    lower_bounds,
                    key=lambda item: (
                        item[0],
                        item[1],
                    ),
                )

                strongest_upper = min(
                    upper_bounds,
                    key=lambda item: (
                        item[0],
                        not item[1],
                    ),
                )

                lower_value, lower_inclusive = strongest_lower
                upper_value, upper_inclusive = strongest_upper

                if lower_value > upper_value:
                    errors.append(
                        f"{path}: Contradictory {attribute} "
                        "range rules were found."
                    )

                elif lower_value == upper_value:
                    if not (
                        lower_inclusive
                        and upper_inclusive
                    ):
                        errors.append(
                            f"{path}: Contradictory {attribute} "
                            "range rules were found."
                        )

    # Recursively inspect child groups
    for child_index, child_group in enumerate(
        group.child_groups,
        start=1,
    ):
        child_path = (
            f"{path}, Child Group {child_index}"
        )

        validate_numeric_rule_contradictions(
            group=child_group,
            path=child_path,
            errors=errors,
        )


def validate_dob_rule_contradictions(
    group: EligibilityRuleGroupData,
    path: str,
    errors: list[str],
):
    """
    Detect impossible Date of Birth combinations
    inside an AND rule group.

    Examples:

        Date of Birth >= 2020-01-01
        Date of Birth <= 1990-01-01

    or:

        Date of Birth = 2000-01-01
        Date of Birth < 1990-01-01
    """

    dob_rules = []

    for rule in group.rules:
        if rule.attribute != "Date of Birth":
            continue

        try:
            dob_value = date.fromisoformat(rule.value)

            if dob_value > date.today():
                continue

            dob_rules.append(
                (rule, dob_value)
            )

        except (ValueError, TypeError):
            continue

    # DOB contradiction checking only applies to AND groups.
    if group.logical_operator == "AND":

        lower_bounds = []
        upper_bounds = []
        exact_values = []

        for rule, value in dob_rules:

            if rule.operator == ">":
                lower_bounds.append(
                    (value, False)
                )

            elif rule.operator == ">=":
                lower_bounds.append(
                    (value, True)
                )

            elif rule.operator == "<":
                upper_bounds.append(
                    (value, False)
                )

            elif rule.operator == "<=":
                upper_bounds.append(
                    (value, True)
                )

            elif rule.operator == "=":
                exact_values.append(value)

        # Check conflicting exact DOB values
        if exact_values:

            if len(set(exact_values)) > 1:
                errors.append(
                    f"{path}: Contradictory Date of Birth "
                    "equality rules were found."
                )

            else:
                exact_value = exact_values[0]

                # Equality vs lower bound
                for lower_value, lower_inclusive in lower_bounds:
                    if (
                        exact_value < lower_value
                        or (
                            exact_value == lower_value
                            and not lower_inclusive
                        )
                    ):
                        errors.append(
                            f"{path}: Date of Birth equality "
                            "rule conflicts with a "
                            "lower-bound rule."
                        )

                # Equality vs upper bound
                for upper_value, upper_inclusive in upper_bounds:
                    if (
                        exact_value > upper_value
                        or (
                            exact_value == upper_value
                            and not upper_inclusive
                        )
                    ):
                        errors.append(
                            f"{path}: Date of Birth equality "
                            "rule conflicts with an "
                            "upper-bound rule."
                        )

        # Check lower-bound / upper-bound conflicts
        if lower_bounds and upper_bounds:

            strongest_lower = max(
                lower_bounds,
                key=lambda item: (
                    item[0],
                    item[1],
                ),
            )

            strongest_upper = min(
                upper_bounds,
                key=lambda item: (
                    item[0],
                    not item[1],
                ),
            )

            lower_value, lower_inclusive = strongest_lower
            upper_value, upper_inclusive = strongest_upper

            if lower_value > upper_value:
                errors.append(
                    f"{path}: Contradictory Date of Birth "
                    "range rules were found."
                )

            elif lower_value == upper_value:
                if not (
                    lower_inclusive
                    and upper_inclusive
                ):
                    errors.append(
                        f"{path}: Contradictory Date of Birth "
                        "range rules were found."
                    )

    # Recursively inspect child groups
    for child_index, child_group in enumerate(
        group.child_groups,
        start=1,
    ):
        child_path = (
            f"{path}, Child Group {child_index}"
        )

        validate_dob_rule_contradictions(
            group=child_group,
            path=child_path,
            errors=errors,
        )


def validate_eligibility_rules(
    data: EligibilityRulesData,
) -> list[str]:

    errors = []

    # At least one rule group is required
    if not data.rule_groups:
        errors.append(
            "Eligibility rules must contain at least "
            "one rule group."
        )

    # Validate each rule group
    for group_index, group in enumerate(
        data.rule_groups,
        start=1,
    ):
        group_path = f"Group {group_index}"

        # Structural validation
        validate_rule_group(
            group=group,
            path=group_path,
            errors=errors,
        )

        # Numeric contradiction validation
        validate_numeric_rule_contradictions(
            group=group,
            path=group_path,
            errors=errors,
        )

        # Date-of-birth contradiction validation
        validate_dob_rule_contradictions(
            group=group,
            path=group_path,
            errors=errors,
        )

    return errors