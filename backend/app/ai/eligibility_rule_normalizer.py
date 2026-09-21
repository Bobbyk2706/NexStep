from datetime import datetime
import re

from app.ai.eligibility_schemas import (
    EligibilityRuleData,
    EligibilityRuleGroupData,
    EligibilityRulesData,
)


# ============================================================
# ATTRIBUTE NORMALIZATION
# ============================================================

ATTRIBUTE_MAP = {
    "cgpa": "CGPA",
    "percentage": "Percentage",
    "specialization": "Specialization",
    "date of birth": "Date of Birth",
    "dob": "Date of Birth",
    "nationality": "Nationality",
    "state": "State",
    "educational qualification": "Educational Qualification",
    "qualification": "Educational Qualification",
    "work experience": "Work Experience",
}


# ============================================================
# OPERATOR NORMALIZATION
# ============================================================

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


# ============================================================
# ATTRIBUTE
# ============================================================

def normalize_attribute(attribute: str) -> str:
    """
    Normalize an extracted eligibility attribute.

    Age is intentionally NOT supported.

    The database eligibility model uses Date of Birth rather
    than Age. Age can only be converted to a DOB rule when
    the exact DOB boundary is explicitly available and has
    already been extracted as such.
    """

    key = attribute.strip().lower()

    if key == "age":
        raise ValueError(
            "Unsupported eligibility attribute: age. "
            "Age must be represented as Date of Birth only "
            "when an exact DOB boundary is explicitly available."
        )

    if key not in ATTRIBUTE_MAP:
        raise ValueError(
            f"Unsupported eligibility attribute: {attribute}"
        )

    return ATTRIBUTE_MAP[key]


# ============================================================
# OPERATOR
# ============================================================

def normalize_operator(value: str) -> str:
    """
    Normalize an eligibility comparison operator.
    """

    value = value.strip()
    normalized_value = value.lower()

    # Normalize repeated equality signs.
    if re.fullmatch(r"=+", normalized_value):
        return "="

    if normalized_value in OPERATOR_MAP:
        return OPERATOR_MAP[normalized_value]

    raise ValueError(
        f"Unsupported eligibility operator: {value}"
    )


# ============================================================
# DATE
# ============================================================

def normalize_date(value: str) -> str:
    """
    Normalize a date into YYYY-MM-DD.

    Supported formats include:

    YYYY-MM-DD
    DD/MM/YYYY
    DD.MM.YYYY
    DD-MM-YYYY
    DD Month YYYY
    DD Month, YYYY
    Month DD YYYY
    Month DD, YYYY

    Ordinal suffixes such as 1st, 2nd, 3rd, 4th are also
    removed before parsing.
    """

    value = value.strip()

    # --------------------------------------------------------
    # Already normalized
    # --------------------------------------------------------

    try:
        parsed_date = datetime.strptime(
            value,
            "%Y-%m-%d",
        )

        return parsed_date.strftime("%Y-%m-%d")

    except ValueError:
        pass

    # --------------------------------------------------------
    # Remove ordinal suffixes
    # --------------------------------------------------------

    cleaned_value = re.sub(
        r"(\d+)(st|nd|rd|th)",
        r"\1",
        value,
        flags=re.IGNORECASE,
    )

    cleaned_value = cleaned_value.strip()

    # --------------------------------------------------------
    # Numeric formats
    # --------------------------------------------------------

    numeric_formats = [
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d.%m.%y",
        "%d-%m-%y",
    ]

    for date_format in numeric_formats:
        try:
            parsed_date = datetime.strptime(
                cleaned_value,
                date_format,
            )

            return parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            continue

    # --------------------------------------------------------
    # Text formats
    # --------------------------------------------------------

    text_formats = [
        "%d %B, %Y",
        "%d %B %Y",
        "%d %b, %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%b %d %Y",
    ]

    for date_format in text_formats:
        try:
            parsed_date = datetime.strptime(
                cleaned_value,
                date_format,
            )

            return parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            continue

    raise ValueError(
        f"Unable to normalize date: {value}"
    )


# ============================================================
# RULE
# ============================================================

def normalize_rule(
    rule: EligibilityRuleData,
) -> EligibilityRuleData:
    """
    Normalize one eligibility rule.
    """

    attribute = normalize_attribute(
        rule.attribute
    )

    operator = normalize_operator(
        rule.operator
    )

    value = rule.value.strip()

    # Date values must be normalized deterministically.
    if attribute == "Date of Birth":
        value = normalize_date(value)

    return EligibilityRuleData(
        attribute=attribute,
        operator=operator,
        value=value,
    )


# ============================================================
# RULE GROUP
# ============================================================

def normalize_rule_group(
    group: EligibilityRuleGroupData,
) -> EligibilityRuleGroupData:
    """
    Recursively normalize one rule group and all child groups.
    """

    logical_operator = (
        group.logical_operator
        .strip()
        .upper()
    )

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
        child_groups=normalized_child_groups,
    )


# ============================================================
# COMPLETE ELIGIBILITY RULES
# ============================================================

def normalize_eligibility_rules(
    data: EligibilityRulesData,
) -> EligibilityRulesData:
    """
    Normalize all eligibility rule groups recursively.
    """

    normalized_groups = [
        normalize_rule_group(group)
        for group in data.rule_groups
    ]

    return EligibilityRulesData(
        rule_groups=normalized_groups,
    )