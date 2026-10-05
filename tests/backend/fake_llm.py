"""Scripted stand-in for a real LLM: reads the passages it is given and
answers like a competent model would, citing real passage ids/quotes."""
from __future__ import annotations

import json
import re

from app.ai.providers.base import AIProvider


def passage_id(context: str, needle: str) -> str | None:
    for block in re.split(r"\n\n(?=\[P\d+ \|)", context):
        if needle in block:
            m = re.match(r"\[(P\d+) \|", block)
            if m:
                return m.group(1)
    return None


def fact(context: str, value, needle: str):
    return {"value": value, "quote": needle, "passage": passage_id(context, needle)}


EMPTY = {"value": None, "quote": None, "passage": None}


class ScriptedProvider(AIProvider):
    name = "scripted"

    def __init__(self, script=None):
        self.calls: list[str] = []
        self.script = script  # optional override: fn(task, context) -> dict|str

    def generate(self, *, messages, response_schema=None, model=None,
                 temperature=0.0, max_tokens=None):
        user = next(m["content"] for m in messages if m["role"] == "user")
        context = user.split("PASSAGES:\n", 1)[-1]
        task = ("identity" if "identify the examination" in user else
                "dates" if "extract the schedule" in user else "eligibility")
        self.calls.append(task)
        if self.script:
            out = self.script(task, context)
            return out if isinstance(out, str) else json.dumps(out)
        return json.dumps(getattr(self, f"_{task}")(context))

    def _identity(self, c):
        return {"exam_name": fact(c, "GATE 2027", "GATE 2027"),
                "conducting_body": fact(c, "IIT Madras", "IIT Madras"),
                "release_date": fact(c, "2026-08-27", "27th August 2026")}

    def _dates(self, c):
        return {
            "application_start_date": EMPTY,
            "application_end_date": fact(c, "2026-09-27", "Sunday, September 27, 2026"),
            "late_fee_end_date": fact(c, "2026-10-05", "Monday, October 5, 2026"),
            "exam_dates": [
                {"label": "Week 1", "start_date": "2027-02-06", "end_date": "2027-02-07",
                 "quote": "February 6 & 7, 2027", "passage": passage_id(c, "February 6 & 7, 2027")},
                {"label": "Week 2", "start_date": "2027-02-13", "end_date": "2027-02-14",
                 "quote": "February 13 & 14, 2027", "passage": passage_id(c, "February 13 & 14, 2027")},
                {"label": "Week 3", "start_date": "2027-02-20", "end_date": "2027-02-21",
                 "quote": "February 20 & 21, 2027", "passage": passage_id(c, "February 20 & 21, 2027")},
            ]}

    def _eligibility(self, c):
        q = "third or higher years of any undergraduate"
        return {
            "has_no_age_limit": True, "age_limits": [],
            "qualifications": [
                {"level": lvl, "field": "Engineering/Technology/Science/Commerce/Arts",
                 "quote": q, "passage": passage_id(c, q)}
                for lvl in ("Bachelor's", "Master's", "PhD")],
            "minimum_percentage": None, "minimum_cgpa": None,
            "score_quote": None, "score_passage": None,
            "nationalities": [], "nationality_quote": None, "nationality_passage": None,
            "work_experience": EMPTY,
            "other_requirements": [{"text": "Currently in the third year or higher of a UG program, or degree completed",
                                    "quote": q, "passage": passage_id(c, q)}]}


# Names used by test_e2e_workflow.py
GATE_ANSWERS = None


class FakeProvider(ScriptedProvider):
    def __init__(self, answers=None):
        super().__init__(None)
