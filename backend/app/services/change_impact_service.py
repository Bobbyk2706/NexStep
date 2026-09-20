from __future__ import annotations

from app.ai.change_impact_schemas import (
    ChangeImpact,
    ChangeImpactAnalysis,
)
from app.ai.semantic_change_schemas import (
    SemanticChangeAnalysis,
)
from app.services.structural_change_detection_service import (
    StructuralChangeReport,
)


class ChangeImpactClassificationError(RuntimeError):
    """
    Raised when change impact classification cannot be
    completed safely.
    """


ELIGIBILITY_PATH_MARKERS = (
    "eligibility_rules",
)

APPLICATION_TIMELINE_PATH_MARKERS = (
    "application_start_date",
    "application_end_date",
)

EXAM_SCHEDULE_PATH_MARKERS = (
    "exam_dates",
)


def _classify_change(
    change_index: int,
    structural_change,
    semantic_change,
) -> ChangeImpact:
    """
    Deterministically classify one change using its structural
    path and validated semantic interpretation.

    The structural path is authoritative for identifying which
    part of the extraction changed.
    """

    path = structural_change.path

    # ------------------------------------------------------------
    # Eligibility changes
    # ------------------------------------------------------------

    if any(
        marker in path
        for marker in ELIGIBILITY_PATH_MARKERS
    ):
        return ChangeImpact(
            change_index=change_index,
            impact_type="ELIGIBILITY_REQUIREMENT_CHANGED",
            affects_eligibility=True,
            affects_application_timeline=False,
            affects_exam_schedule=False,
            requires_eligibility_re_evaluation=True,
            requires_human_review=(
                semantic_change.requires_human_review
            ),
            reason=(
                "The structural change occurs inside the "
                "eligibility rules."
            ),
        )

    # ------------------------------------------------------------
    # Application timeline
    # ------------------------------------------------------------

    if any(
        marker in path
        for marker in APPLICATION_TIMELINE_PATH_MARKERS
    ):
        return ChangeImpact(
            change_index=change_index,
            impact_type="APPLICATION_TIMELINE_CHANGED",
            affects_eligibility=False,
            affects_application_timeline=True,
            affects_exam_schedule=False,
            requires_eligibility_re_evaluation=False,
            requires_human_review=(
                semantic_change.requires_human_review
            ),
            reason=(
                "The structural change affects the "
                "application timeline."
            ),
        )

    # ------------------------------------------------------------
    # Exam schedule
    # ------------------------------------------------------------

    if any(
        marker in path
        for marker in EXAM_SCHEDULE_PATH_MARKERS
    ):
        return ChangeImpact(
            change_index=change_index,
            impact_type="EXAM_SCHEDULE_CHANGED",
            affects_eligibility=False,
            affects_application_timeline=False,
            affects_exam_schedule=True,
            requires_eligibility_re_evaluation=False,
            requires_human_review=(
                semantic_change.requires_human_review
            ),
            reason=(
                "The structural change affects the "
                "exam schedule."
            ),
        )

    # ------------------------------------------------------------
    # Other exam information
    # ------------------------------------------------------------

    return ChangeImpact(
        change_index=change_index,
        impact_type="EXAM_INFORMATION_CHANGED",
        affects_eligibility=False,
        affects_application_timeline=False,
        affects_exam_schedule=False,
        requires_eligibility_re_evaluation=False,
        requires_human_review=(
            semantic_change.requires_human_review
        ),
        reason=(
            "The structural change affects exam "
            "information outside the known eligibility, "
            "application timeline, and exam schedule fields."
        ),
    )


def classify_change_impacts(
    structural_report: StructuralChangeReport,
    semantic_analysis: SemanticChangeAnalysis,
) -> ChangeImpactAnalysis:
    """
    Deterministically classify the operational impact of
    semantic changes.

    Structural paths remain authoritative.

    No new changes may be created here.
    """

    if not isinstance(
        structural_report,
        StructuralChangeReport,
    ):
        raise TypeError(
            "structural_report must be StructuralChangeReport."
        )

    if not isinstance(
        semantic_analysis,
        SemanticChangeAnalysis,
    ):
        raise TypeError(
            "semantic_analysis must be SemanticChangeAnalysis."
        )

    if not structural_report.change_detected:
        if semantic_analysis.changes:
            raise ChangeImpactClassificationError(
                "Semantic changes exist even though the "
                "structural report contains no changes."
            )

        return ChangeImpactAnalysis(
            impacts=[],
            overall_requires_human_review=False,
            overall_requires_eligibility_re_evaluation=False,
        )

    expected_indices = set(
        range(
            len(structural_report.changes)
        )
    )

    semantic_indices = {
        change.change_index
        for change in semantic_analysis.changes
    }

    if semantic_indices != expected_indices:
        raise ChangeImpactClassificationError(
            "Semantic analysis does not map exactly "
            "to the structural changes."
        )

    semantic_by_index = {
        change.change_index: change
        for change in semantic_analysis.changes
    }

    impacts: list[ChangeImpact] = []

    for index, structural_change in enumerate(
        structural_report.changes
    ):
        semantic_change = semantic_by_index[index]

        impacts.append(
            _classify_change(
                change_index=index,
                structural_change=structural_change,
                semantic_change=semantic_change,
            )
        )

    overall_requires_human_review = (
        semantic_analysis.requires_human_review
        or any(
            impact.requires_human_review
            for impact in impacts
        )
    )

    overall_requires_eligibility_re_evaluation = any(
        impact.requires_eligibility_re_evaluation
        for impact in impacts
    )

    return ChangeImpactAnalysis(
        impacts=impacts,
        overall_requires_human_review=(
            overall_requires_human_review
        ),
        overall_requires_eligibility_re_evaluation=(
            overall_requires_eligibility_re_evaluation
        ),
    )