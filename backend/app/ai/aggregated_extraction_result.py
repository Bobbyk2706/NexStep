from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from app.ai.extraction_evidence import ExtractionEvidence
from app.ai.extraction_schemas import CompleteExtractionData


class ExtractionIssue(BaseModel):
    """
    A problem, or noteworthy fact, found while extracting.

    severity:
        error   - approving this extraction would store bad or
                  incomplete data; the administrator must look.
        warning - probably fine, but should be verified.
        info    - context that helps the reviewer (for example a
                  date the source lists as "to be announced").
    """

    severity: Literal["error", "warning", "info"] = "warning"
    code: str = ""
    field: str | None = None
    message: str


class ConflictOption(BaseModel):
    value: str
    source: str = ""
    pages: list[int] = Field(default_factory=list)


class ExtractionConflict(BaseModel):
    """
    The document appears to give more than one value for a field.
    """

    field: str
    options: list[ConflictOption] = Field(default_factory=list)

    # Which option the pipeline provisionally used (if any).
    chosen: str | None = None
    reason: str | None = None


class AggregatedExtractionResult(BaseModel):
    extraction: CompleteExtractionData
    evidence: list[ExtractionEvidence]

    # v2 pipeline fields. Old stored rows do not have them, so every
    # one has a default and old rows keep deserializing unchanged.
    conflicts: list[ExtractionConflict] = Field(default_factory=list)
    issues: list[ExtractionIssue] = Field(default_factory=list)
    pipeline: dict[str, Any] = Field(default_factory=dict)

    @property
    def blocking_issues(self) -> list[ExtractionIssue]:
        return [i for i in self.issues if i.severity == "error"]
