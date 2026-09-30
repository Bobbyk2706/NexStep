"""
Tolerant comparison of free-text eligibility values.

Rules extracted from a notification say `Nationality = India` or
`Educational Qualification = Bachelor's`, while students type whatever
they like ("Indian", "bachelors", "B.Tech"). Comparing raw strings would
mark eligible students as ineligible, so both sides are reduced to a
canonical form first.
"""

from __future__ import annotations

import re

_DEMONYMS = {
    "indian": "india", "nepali": "nepal", "nepalese": "nepal",
    "bhutanese": "bhutan", "bangladeshi": "bangladesh",
    "sri lankan": "sri lanka", "pakistani": "pakistan",
}

_LEVELS = {
    "10th": "10th", "tenth": "10th", "secondary": "10th", "ssc": "10th", "matriculation": "10th",
    "12th": "12th / senior secondary", "twelfth": "12th / senior secondary",
    "12th / senior secondary": "12th / senior secondary", "senior secondary": "12th / senior secondary",
    "hsc": "12th / senior secondary", "intermediate": "12th / senior secondary",
    "diploma": "diploma",
    "bachelor's": "bachelor's", "bachelors": "bachelor's", "bachelor": "bachelor's",
    "graduate": "bachelor's", "graduation": "bachelor's", "undergraduate": "bachelor's",
    "b.e": "bachelor's", "b.tech": "bachelor's", "btech": "bachelor's", "be": "bachelor's",
    "b.sc": "bachelor's", "bsc": "bachelor's", "b.a": "bachelor's", "b.com": "bachelor's",
    "bca": "bachelor's", "b.arch": "bachelor's",
    "master's": "master's", "masters": "master's", "master": "master's",
    "postgraduate": "master's", "post graduate": "master's",
    "m.e": "master's", "m.tech": "master's", "mtech": "master's", "m.sc": "master's",
    "msc": "master's", "mca": "master's", "m.a": "master's", "mba": "master's",
    "phd": "phd", "ph.d": "phd", "doctorate": "phd", "doctoral": "phd",
}


def canonical_text(value: str) -> str:
    text = re.sub(r"[\u2018\u2019`]", "'", str(value)).strip().casefold()
    text = re.sub(r"\s+", " ", text).rstrip(".").strip()

    if text in _DEMONYMS:
        return _DEMONYMS[text]

    # "Bachelor's degree", "B.Tech." ...
    stripped = re.sub(r"\s+(degree|program(me)?|course)$", "", text)
    for candidate in (text, stripped, stripped.rstrip(".")):
        if candidate in _LEVELS:
            return _LEVELS[candidate]

    return text


def texts_equal(a: str, b: str) -> bool:
    return canonical_text(a) == canonical_text(b)
