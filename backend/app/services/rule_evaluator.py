import re

# Profile fields are free text ("Indian", "Bachelors"), while extracted
# rules use canonical names ("India", "Bachelor's"). Compare text the way
# a person would: ignoring case, punctuation and common aliases.
_ALIASES = {
    "indian": "india", "nepali": "nepal", "nepalese": "nepal",
    "bhutanese": "bhutan", "bangladeshi": "bangladesh", "sri lankan": "sri lanka",
    "bachelor": "bachelors", "bachelors degree": "bachelors",
    "undergraduate": "bachelors", "graduate": "bachelors",
    "master": "masters", "masters degree": "masters", "postgraduate": "masters",
    "doctorate": "phd", "doctoral": "phd", "ph d": "phd",
    "12th": "12th senior secondary", "12th senior secondary": "12th senior secondary",
    "class 12": "12th senior secondary", "10th": "10th", "class 10": "10th",
}


def normalize_text(value: str) -> str:
    text = re.sub(r"[^a-z0-9 ]+", " ", value.casefold().replace("'", ""))
    text = re.sub(r"\s+", " ", text).strip()
    return _ALIASES.get(text, text)


def _same_text(left, right) -> bool:
    if isinstance(left, str) and isinstance(right, str):
        return normalize_text(left) == normalize_text(right)
    return left == right


def evaluate_rule(student_value, operator, rule_value):

    if operator == "=":
        return _same_text(student_value, rule_value)

    elif operator == "!=":
        return not _same_text(student_value, rule_value)

    elif operator == ">":
        return student_value > rule_value

    elif operator == ">=":
        return student_value >= rule_value

    elif operator == "<":
        return student_value < rule_value

    elif operator == "<=":
        return student_value <= rule_value

    else:
        raise ValueError(f"Unsupported operator: {operator}")