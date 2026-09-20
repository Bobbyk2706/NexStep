from __future__ import annotations

from pydantic import BaseModel, Field


class ChangeImpact(BaseModel):
    """
    Deterministic classification of the operational impact
    of one semantic change.
    """

    change_index: int = Field(ge=0)

    impact_type: str

    affects_eligibility: bool

    affects_application_timeline: bool

    affects_exam_schedule: bool

    requires_eligibility_re_evaluation: bool

    requires_human_review: bool

    reason: str


class ChangeImpactAnalysis(BaseModel):
    """
    Complete impact classification for a semantic change report.
    """

    impacts: list[ChangeImpact] = Field(
        default_factory=list,
    )

    overall_requires_human_review: bool

    overall_requires_eligibility_re_evaluation: bool