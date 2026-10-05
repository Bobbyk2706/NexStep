from datetime import date

import pytest

from app.services.rule_evaluator import evaluate_rule


@pytest.mark.parametrize("student,rule", [
    ("Indian", "India"), ("india", "India"), (" INDIA ", "India"),
    ("Bachelors", "Bachelor's"), ("Bachelor's degree", "Bachelor's"),
    ("Master's", "Masters"), ("12th / Senior Secondary", "12th / Senior Secondary"),
])
def test_text_equality_is_forgiving(student, rule):
    assert evaluate_rule(student, "=", rule)
    assert not evaluate_rule(student, "!=", rule)


def test_different_values_still_differ():
    assert not evaluate_rule("Nepali", "=", "India")
    assert not evaluate_rule("Master's", "=", "Bachelor's")
    assert evaluate_rule("Master's", "!=", "Bachelor's")


def test_numbers_and_dates_unchanged():
    assert evaluate_rule(8.5, ">=", 7.0)
    assert not evaluate_rule(6.0, ">=", 7.0)
    assert evaluate_rule(date(2000, 1, 1), ">=", date(1995, 1, 1))
    assert evaluate_rule(60.0, "=", 60.0)
