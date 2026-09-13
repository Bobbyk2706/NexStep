from datetime import datetime
import re

from app.ai.eligibility_schemas import (
    EligibilityRuleData,
    EligibilityRuleGroupData,
    EligibilityRulesData,
)


ATTRIBUTE_MAP = {
    "cgpa": "CGPA",
    "percentage": "Percentage",
    "specialization": "Specialization",
    "date of birth": "Date of Birth",
    "nationality": "Nationality",
    "state": "State",
    "educational qualification": "Educational Qualification",
    "work experience": "Work Experience",
}


OPERATOR_MAP = {
    "=": "=",
    "==": "=",
    "equal": "=",
    "equals": "=",
    "equal to": "=",

    "!=": "!=",
    "not equal": "!=",
    "not equal to": "!=",

    ">": ">",
    "greater than": ">",
    "above": ">",

    ">=": ">=",
    "greater than or equal to": ">=",
    "at least": ">=",
    "minimum": ">=",

    "<": "<",
    "less than": "<",
    "below": "<",

    "<=": "<=",
    "less than or equal to": "<=",
    "at most": "<=",
    "maximum": "<=",
}


def normalize_attribute(attribute: str) -> str:
    key = attribute.strip().lower()

    if key not in ATTRIBUTE_MAP:
        raise ValueError(
            f"Unsupported eligibility attribute: {attribute}"
        )

    return ATTRIBUTE_MAP[key]


def normalize_operator(value: str) -> str:
    value = value.strip()

    normalized_value = value.lower()

    if normalized_value in OPERATOR_MAP:
        return OPERATOR_MAP[normalized_value]

    raise ValueError(
        f"Unsupported eligibility operator: {value}"
    )


def normalize_date(value: str) -> str:
    value = value.strip()

    # Already normalized
    try:
        parsed_date = datetime.strptime(
            value,
            "%Y-%m-%d"
        )
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    cleaned_value = re.sub(
        r"(\d+)(st|nd|rd|th)",
        r"\1",
        value,
        flags=re.IGNORECASE
    )

    formats = [
        "%d %B, %Y",
        "%d %B %Y",
        "%B %d, %Y",
        "%B %d %Y",
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(
                cleaned_value,
                date_format
            )
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(
        f"Unable to normalize date: {value}"
    )


def normalize_rule(
    rule: EligibilityRuleData
) -> EligibilityRuleData:

    attribute = normalize_attribute(
        rule.attribute
    )

    operator = normalize_operator(
        rule.operator
    )

    value = rule.value.strip()

    if attribute == "Date of Birth":
        value = normalize_date(value)

    return EligibilityRuleData(
        attribute=attribute,
        operator=operator,
        value=value
    )


def normalize_rule_group(
    group: EligibilityRuleGroupData
) -> EligibilityRuleGroupData:

    logical_operator = group.logical_operator.strip().upper()

    normalized_rules = [
        normalize_rule(rule)
        for rule in group.rules
    ]

    normalized_child_groups = [
        normalize_rule_group(child_group)
        for child_group in group.child_groups
    ]

    return EligibilityRuleGroupData(
        logical_operator=logical_operator,
        rules=normalized_rules,
        child_groups=normalized_child_groups
    )


def normalize_eligibility_rules(
    data: EligibilityRulesData
) -> EligibilityRulesData:

    normalized_groups = [
        normalize_rule_group(group)
        for group in data.rule_groups
    ]

    return EligibilityRulesData(
        rule_groups=normalized_groups
    )