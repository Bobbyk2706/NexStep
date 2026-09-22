from __future__ import annotations

import json
from typing import Any, Callable

from app.ai.semantic_change_schemas import (
    SemanticChangeAnalysis,
)
from app.services.structural_change_detection_service import (
    StructuralChangeReport,
)


class SemanticChangeAnalysisError(RuntimeError):
    """
    Raised when semantic change analysis cannot be completed
    safely.
    """


def _serialize_change_report(
    report: StructuralChangeReport,
) -> list[dict[str, Any]]:
    """
    Convert the deterministic structural report into a
    JSON-compatible representation for the LLM.
    """

    return [
        {
            "change_index": index,
            "change_type": change.change_type,
            "path": change.path,
            "old_value": change.old_value,
            "new_value": change.new_value,
        }
        for index, change in enumerate(report.changes)
    ]


def build_semantic_change_prompt(
    report: StructuralChangeReport,
) -> str:
    """
    Build the prompt used by the semantic change analyzer.

    The prompt explicitly constrains the model to interpret
    only the deterministic structural changes supplied by
    Phase 3.
    """

    changes = _serialize_change_report(report)

    serialized_changes = json.dumps(
        changes,
        ensure_ascii=False,
        indent=2,
        default=str,
    )

    return f"""
You are analyzing changes in an official competitive-exam
notification.

A deterministic Python structural comparison has already been
performed.

Your job is ONLY to explain the meaning of those detected
changes.

IMPORTANT RULES:

1. Do not invent changes.
2. Do not identify changes that are absent from the supplied
   structural change list.
3. Do not infer requirements that are not represented by the
   supplied values.
4. Base every explanation only on the old value, new value,
   change type, and structural path.
5. If the meaning is ambiguous, say that it is ambiguous.
6. If you cannot safely determine the impact, set
   requires_human_review to true.
7. Never fabricate missing information.
8. Preserve the distinction between:
   - what definitely changed
   - what the change may affect
   - what cannot safely be determined
9. Use HIGH confidence only when the meaning is directly
   supported by the supplied structural values.
10. Every returned change must correspond to exactly one
    change_index from the supplied list.
11. Do not omit a supplied structural change.
12. Do not create additional change entries.

The structural comparison produced:

{serialized_changes}

Return a structured semantic analysis.
""".strip()


def analyze_semantic_changes(
    report: StructuralChangeReport,
    analyzer: Callable[[str], Any],
) -> SemanticChangeAnalysis:
    """
    Run semantic analysis using an injected AI analyzer.

    The analyzer is intentionally injected so that:

    - unit tests can mock Gemini
    - the service does not depend on a particular
      Gemini client implementation
    - production AI infrastructure can be changed
      independently of this service
    """

    if not isinstance(
        report,
        StructuralChangeReport,
    ):
        raise TypeError(
            "report must be StructuralChangeReport."
        )

    if not callable(analyzer):
        raise TypeError(
            "analyzer must be callable."
        )

    if not report.change_detected:
        return SemanticChangeAnalysis(
            overall_summary="No structural changes detected.",
            changes=[],
            requires_human_review=False,
        )

    prompt = build_semantic_change_prompt(report)

    try:
        raw_result = analyzer(prompt)
    except Exception as exc:
        raise SemanticChangeAnalysisError(
            "Semantic change analysis failed."
        ) from exc

    try:
        if isinstance(
            raw_result,
            SemanticChangeAnalysis,
        ):
            result = raw_result

        elif isinstance(raw_result, str):
            result = SemanticChangeAnalysis.model_validate_json(
                raw_result
            )

        elif isinstance(raw_result, dict):
            result = SemanticChangeAnalysis.model_validate(
                raw_result
            )

        else:
            raise TypeError(
                "Analyzer returned an unsupported result type."
            )

    except Exception as exc:
        raise SemanticChangeAnalysisError(
            "AI semantic analysis returned invalid structured data."
        ) from exc

    _validate_change_mapping(
        report,
        result,
    )

    return result


def _validate_change_mapping(
    report: StructuralChangeReport,
    analysis: SemanticChangeAnalysis,
) -> None:
    """
    Enforce the most important safety invariant:

    AI semantic results may interpret deterministic changes,
    but they may not create, remove, or duplicate them.
    """

    expected_indices = set(
        range(len(report.changes))
    )

    actual_indices = [
        change.change_index
        for change in analysis.changes
    ]

    actual_index_set = set(actual_indices)

    if actual_index_set != expected_indices:
        raise SemanticChangeAnalysisError(
            "AI semantic analysis does not map exactly "
            "to the deterministic structural changes."
        )

    if len(actual_indices) != len(
        actual_index_set
    ):
        raise SemanticChangeAnalysisError(
            "AI semantic analysis contains duplicate "
            "change indices."
        )

    if analysis.requires_human_review is False:
        if any(
            change.requires_human_review
            for change in analysis.changes
        ):
            raise SemanticChangeAnalysisError(
                "Analysis contains a change requiring human "
                "review but overall review status is false."
            )