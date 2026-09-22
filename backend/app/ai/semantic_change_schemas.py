from __future__ import annotations

from pydantic import BaseModel, Field


class SemanticChange(BaseModel):
    """
    AI interpretation of one deterministic structural change.

    The AI is interpreting an already detected change.
    It must not create new structural changes.
    """

    change_index: int = Field(
        ge=0,
        description=(
            "Zero-based index of the corresponding "
            "structural change."
        ),
    )

    summary: str = Field(
        description=(
            "Concise factual description of what changed."
        ),
    )

    affected_requirement: str = Field(
        description=(
            "The exam requirement or exam information "
            "affected by the change."
        ),
    )

    impact: str = Field(
        description=(
            "Potential impact of the change on exam "
            "eligibility or application information."
        ),
    )

    confidence: str = Field(
        description=(
            "Confidence level: HIGH, MEDIUM, or LOW."
        ),
    )

    requires_human_review: bool = Field(
        description=(
            "Whether the change requires human review "
            "because its meaning is ambiguous or cannot "
            "be safely determined."
        ),
    )

    explanation: str = Field(
        description=(
            "Evidence-grounded explanation based only on "
            "the supplied old and new values."
        ),
    )


class SemanticChangeAnalysis(BaseModel):
    """
    Complete AI semantic interpretation of a structural
    change report.
    """

    overall_summary: str = Field(
        description=(
            "Factual summary of the detected changes."
        ),
    )

    changes: list[SemanticChange] = Field(
        default_factory=list,
    )

    requires_human_review: bool = Field(
        description=(
            "Whether the complete change set requires "
            "human review."
        ),
    )