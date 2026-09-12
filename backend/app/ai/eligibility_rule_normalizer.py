from datetime import datetime
import re
from app.ai.eligibility_schemas import (
    EligibilityRuleData,
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
    "!=": "!=",
    ">": ">",
    ">=": ">=",
    "<": "<",
    "<=": "<=",
    "in": "IN",
    "IN": "IN",
}


def normalize_attribute(attribute: str) -> str:
    key = attribute.strip().lower()

    if key not in ATTRIBUTE_MAP:
        raise ValueError(
            f"Unsupported eligibility attribute: {attribute}"
        )

    return ATTRIBUTE_MAP[key]


def normalize_operator(operator: str) -> str:
    key = operator.strip()

    if key not in OPERATOR_MAP:
        raise ValueError(
            f"Unsupported eligibility operator: {operator}"
        )

    return OPERATOR_MAP[key]


import re
from datetime import datetime


def normalize_date(value: str) -> str:
    value = value.strip()

    # Remove ordinal suffixes:
    # 1st → 1
    # 2nd → 2
    # 3rd → 3
    # 4th → 4
    cleaned_value = re.sub(
        r"(\d+)(st|nd|rd|th)",
        r"\1",
        value,
        flags=re.IGNORECASE
    )

    formats = [
        "%d %B, %Y",
        "%d %B %Y",
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(
                cleaned_value,
                date_format
            )

            return parsed_date.strftime(
                "%Y-%m-%d"
            )

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


def normalize_eligibility_rules(
    data: EligibilityRulesData
) -> EligibilityRulesData:

    normalized_groups = []

    for group in data.rule_groups:

        normalized_rules = [
            normalize_rule(rule)
            for rule in group.rules
        ]

        normalized_groups.append({
            "logical_operator": group.logical_operator.upper(),
            "rules": normalized_rules
        })

    return EligibilityRulesData(
        rule_groups=normalized_groups
    )