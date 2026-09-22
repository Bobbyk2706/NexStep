from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.ai.extraction_schemas import CompleteExtractionData


@dataclass(frozen=True)
class StructuralChange:
    """
    Represents one deterministic structural difference between
    an approved extraction and a newly validated extraction.
    """

    change_type: str
    path: str
    old_value: Any = None
    new_value: Any = None


@dataclass
class StructuralChangeReport:
    """
    Result of deterministic structural comparison.
    """

    change_detected: bool
    changes: list[StructuralChange] = field(default_factory=list)

    @property
    def change_count(self) -> int:
        return len(self.changes)


def _normalize_value(value: Any) -> Any:
    """
    Convert Pydantic models and nested structures into
    deterministic Python structures.
    """

    if hasattr(value, "model_dump"):
        return _normalize_value(value.model_dump(mode="python"))

    if isinstance(value, dict):
        return {
            str(key): _normalize_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _normalize_value(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            _normalize_value(item)
            for item in value
        ]

    return value


def _format_path(parent: str, key: Any) -> str:
    """
    Build a readable structural path.
    """

    if parent:
        if isinstance(key, int):
            return f"{parent}[{key}]"

        return f"{parent}.{key}"

    if isinstance(key, int):
        return f"[{key}]"

    return str(key)


def _freeze(value: Any) -> Any:
    """
    Convert a nested structure into a hashable representation.

    Used only for deterministic matching of unordered domain
    collections.
    """

    if isinstance(value, dict):
        return tuple(
            sorted(
                (
                    key,
                    _freeze(item),
                )
                for key, item in value.items()
            )
        )

    if isinstance(value, list):
        return tuple(
            _freeze(item)
            for item in value
        )

    if isinstance(value, tuple):
        return tuple(
            _freeze(item)
            for item in value
        )

    return value


def _compare_values(
    old_value: Any,
    new_value: Any,
    path: str,
    changes: list[StructuralChange],
) -> None:
    """
    Generic recursive comparison.

    This is used for ordinary scalar/dictionary structures.
    Domain-specific unordered collections are handled separately.
    """

    if isinstance(old_value, dict) and isinstance(new_value, dict):
        old_keys = set(old_value.keys())
        new_keys = set(new_value.keys())

        for key in sorted(new_keys - old_keys):
            changes.append(
                StructuralChange(
                    change_type="ADDED",
                    path=_format_path(path, key),
                    old_value=None,
                    new_value=new_value[key],
                )
            )

        for key in sorted(old_keys - new_keys):
            changes.append(
                StructuralChange(
                    change_type="REMOVED",
                    path=_format_path(path, key),
                    old_value=old_value[key],
                    new_value=None,
                )
            )

        for key in sorted(old_keys & new_keys):
            _compare_values(
                old_value[key],
                new_value[key],
                _format_path(path, key),
                changes,
            )

        return

    if isinstance(old_value, list) and isinstance(new_value, list):
        common_length = min(
            len(old_value),
            len(new_value),
        )

        for index in range(common_length):
            _compare_values(
                old_value[index],
                new_value[index],
                _format_path(path, index),
                changes,
            )

        for index in range(
            common_length,
            len(new_value),
        ):
            changes.append(
                StructuralChange(
                    change_type="ADDED",
                    path=_format_path(path, index),
                    old_value=None,
                    new_value=new_value[index],
                )
            )

        for index in range(
            common_length,
            len(old_value),
        ):
            changes.append(
                StructuralChange(
                    change_type="REMOVED",
                    path=_format_path(path, index),
                    old_value=old_value[index],
                    new_value=None,
                )
            )

        return

    if old_value != new_value:
        changes.append(
            StructuralChange(
                change_type="MODIFIED",
                path=path,
                old_value=old_value,
                new_value=new_value,
            )
        )


# ------------------------------------------------------------------
# Exam-date comparison
# ------------------------------------------------------------------


def _exam_date_identity(exam_date: dict[str, Any]) -> tuple[Any, Any]:
    """
    Identity for an exam-date range.

    The start date is the primary identity because if only the
    end date changes, we want that to be reported as MODIFIED
    rather than REMOVE + ADD.
    """

    return (
        exam_date.get("start_date"),
        exam_date.get("end_date"),
    )


def _exam_date_match_key(exam_date: dict[str, Any]) -> Any:
    """
    Match exam dates primarily by start date.

    If the same start date exists but the end date changed,
    the range can be reported as MODIFIED.
    """

    return exam_date.get("start_date")


def _compare_exam_dates(
    old_dates: list[dict[str, Any]],
    new_dates: list[dict[str, Any]],
    path: str,
    changes: list[StructuralChange],
) -> None:
    """
    Compare exam-date ranges without treating ordering as meaningful.
    """

    old_by_start: dict[Any, list[dict[str, Any]]] = {}
    new_by_start: dict[Any, list[dict[str, Any]]] = {}

    for item in old_dates:
        old_by_start.setdefault(
            _exam_date_match_key(item),
            [],
        ).append(item)

    for item in new_dates:
        new_by_start.setdefault(
            _exam_date_match_key(item),
            [],
        ).append(item)

    all_keys = sorted(
        set(old_by_start) | set(new_by_start),
        key=lambda value: str(value),
    )

    output_index = 0

    for key in all_keys:
        old_items = old_by_start.get(key, [])
        new_items = new_by_start.get(key, [])

        common_count = min(
            len(old_items),
            len(new_items),
        )

        for index in range(common_count):
            old_item = old_items[index]
            new_item = new_items[index]

            if old_item != new_item:
                changes.append(
                    StructuralChange(
                        change_type="MODIFIED",
                        path=f"{path}[{output_index}]",
                        old_value=old_item,
                        new_value=new_item,
                    )
                )

            output_index += 1

        for index in range(
            common_count,
            len(new_items),
        ):
            changes.append(
                StructuralChange(
                    change_type="ADDED",
                    path=f"{path}[{output_index}]",
                    old_value=None,
                    new_value=new_items[index],
                )
            )

            output_index += 1

        for index in range(
            common_count,
            len(old_items),
        ):
            changes.append(
                StructuralChange(
                    change_type="REMOVED",
                    path=f"{path}[{output_index}]",
                    old_value=old_items[index],
                    new_value=None,
                )
            )

            output_index += 1


# ------------------------------------------------------------------
# Eligibility-rule comparison
# ------------------------------------------------------------------


def _rule_match_key(rule: dict[str, Any]) -> tuple[Any, Any]:
    """
    Identify a rule by attribute + operator.

    This allows:

        CGPA >= 7.0
        CGPA >= 7.5

    to be recognized as the same rule whose value changed.

    If the operator itself changes, the rule is treated as
    REMOVE + ADD because its identity changed.
    """

    return (
        rule.get("attribute"),
        rule.get("operator"),
    )


def _compare_rules(
    old_rules: list[dict[str, Any]],
    new_rules: list[dict[str, Any]],
    path: str,
    changes: list[StructuralChange],
) -> None:
    """
    Compare eligibility rules without treating their order
    as meaningful.
    """

    old_by_key: dict[
        tuple[Any, Any],
        list[dict[str, Any]],
    ] = {}

    new_by_key: dict[
        tuple[Any, Any],
        list[dict[str, Any]],
    ] = {}

    for rule in old_rules:
        old_by_key.setdefault(
            _rule_match_key(rule),
            [],
        ).append(rule)

    for rule in new_rules:
        new_by_key.setdefault(
            _rule_match_key(rule),
            [],
        ).append(rule)

    all_keys = sorted(
        set(old_by_key) | set(new_by_key),
        key=lambda value: str(value),
    )

    output_index = 0

    for key in all_keys:
        old_items = old_by_key.get(key, [])
        new_items = new_by_key.get(key, [])

        common_count = min(
            len(old_items),
            len(new_items),
        )

        for index in range(common_count):
            old_rule = old_items[index]
            new_rule = new_items[index]

            _compare_values(
                old_rule,
                new_rule,
                f"{path}[{output_index}]",
                changes,
            )

            output_index += 1

        for index in range(
            common_count,
            len(new_items),
        ):
            changes.append(
                StructuralChange(
                    change_type="ADDED",
                    path=f"{path}[{output_index}]",
                    old_value=None,
                    new_value=new_items[index],
                )
            )

            output_index += 1

        for index in range(
            common_count,
            len(old_items),
        ):
            changes.append(
                StructuralChange(
                    change_type="REMOVED",
                    path=f"{path}[{output_index}]",
                    old_value=old_items[index],
                    new_value=None,
                )
            )

            output_index += 1


# ------------------------------------------------------------------
# Eligibility-group comparison
# ------------------------------------------------------------------


def _group_identity(group: dict[str, Any]) -> Any:
    """
    Build an order-independent identity for an eligibility group.

    Rule values are deliberately excluded from the identity.

    This means:

        CGPA >= 7.0
        CGPA >= 7.5

    remain the same logical rule/group for comparison purposes,
    allowing the actual value change to be reported.

    The logical operator remains part of identity because:

        A AND B

    is structurally different from:

        A OR B
    """

    rule_identity = sorted(
        (
            rule.get("attribute"),
            rule.get("operator"),
        )
        for rule in group.get("rules", [])
    )

    child_identity = sorted(
        _group_identity(child)
        for child in group.get("child_groups", [])
    )

    return (
        group.get("logical_operator"),
        tuple(rule_identity),
        tuple(child_identity),
    )


def _compare_group(
    old_group: dict[str, Any],
    new_group: dict[str, Any],
    path: str,
    changes: list[StructuralChange],
) -> None:
    """
    Recursively compare two matched eligibility groups.

    Rule and child-group ordering is ignored.
    """

    old_operator = old_group.get("logical_operator")
    new_operator = new_group.get("logical_operator")

    if old_operator != new_operator:
        changes.append(
            StructuralChange(
                change_type="MODIFIED",
                path=f"{path}.logical_operator",
                old_value=old_operator,
                new_value=new_operator,
            )
        )

    _compare_rules(
        old_group.get("rules", []),
        new_group.get("rules", []),
        f"{path}.rules",
        changes,
    )

    _compare_groups(
        old_group.get("child_groups", []),
        new_group.get("child_groups", []),
        f"{path}.child_groups",
        changes,
    )


def _compare_groups(
    old_groups: list[dict[str, Any]],
    new_groups: list[dict[str, Any]],
    path: str,
    changes: list[StructuralChange],
) -> None:
    """
    Compare eligibility groups without treating sibling-group
    ordering as meaningful.
    """

    old_by_identity: dict[Any, list[dict[str, Any]]] = {}
    new_by_identity: dict[Any, list[dict[str, Any]]] = {}

    for group in old_groups:
        old_by_identity.setdefault(
            _group_identity(group),
            [],
        ).append(group)

    for group in new_groups:
        new_by_identity.setdefault(
            _group_identity(group),
            [],
        ).append(group)

    all_keys = sorted(
        set(old_by_identity) | set(new_by_identity),
        key=lambda value: str(value),
    )

    output_index = 0

    for identity in all_keys:
        old_items = old_by_identity.get(identity, [])
        new_items = new_by_identity.get(identity, [])

        common_count = min(
            len(old_items),
            len(new_items),
        )

        for index in range(common_count):
            _compare_group(
                old_items[index],
                new_items[index],
                f"{path}[{output_index}]",
                changes,
            )

            output_index += 1

        for index in range(
            common_count,
            len(new_items),
        ):
            changes.append(
                StructuralChange(
                    change_type="ADDED",
                    path=f"{path}[{output_index}]",
                    old_value=None,
                    new_value=new_items[index],
                )
            )

            output_index += 1

        for index in range(
            common_count,
            len(old_items),
        ):
            changes.append(
                StructuralChange(
                    change_type="REMOVED",
                    path=f"{path}[{output_index}]",
                    old_value=old_items[index],
                    new_value=None,
                )
            )

            output_index += 1


# ------------------------------------------------------------------
# Top-level comparison
# ------------------------------------------------------------------


def _compare_complete_extractions(
    old_data: dict[str, Any],
    new_data: dict[str, Any],
) -> list[StructuralChange]:
    """
    Compare the known CompleteExtractionData structure.

    Domain-specific collections are handled using their
    semantic structural identities.
    """

    changes: list[StructuralChange] = []

    old_exam = old_data.get(
        "exam_information",
        {},
    )

    new_exam = new_data.get(
        "exam_information",
        {},
    )

    # --------------------------------------------------------------
    # Exam information
    # --------------------------------------------------------------

    old_exam_dates = old_exam.pop(
        "exam_dates",
        [],
    )

    new_exam_dates = new_exam.pop(
        "exam_dates",
        [],
    )

    _compare_values(
        old_exam,
        new_exam,
        "exam_information",
        changes,
    )

    _compare_exam_dates(
        old_exam_dates,
        new_exam_dates,
        "exam_information.exam_dates",
        changes,
    )

    # --------------------------------------------------------------
    # Eligibility rules
    # --------------------------------------------------------------

    old_rules = old_data.get(
        "eligibility_rules",
        {},
    )

    new_rules = new_data.get(
        "eligibility_rules",
        {},
    )

    old_rule_groups = old_rules.get(
        "rule_groups",
        [],
    )

    new_rule_groups = new_rules.get(
        "rule_groups",
        [],
    )

    _compare_groups(
        old_rule_groups,
        new_rule_groups,
        "eligibility_rules.rule_groups",
        changes,
    )

    # --------------------------------------------------------------
    # Any future top-level fields
    # --------------------------------------------------------------

    old_other = {
        key: value
        for key, value in old_data.items()
        if key not in {
            "exam_information",
            "eligibility_rules",
        }
    }

    new_other = {
        key: value
        for key, value in new_data.items()
        if key not in {
            "exam_information",
            "eligibility_rules",
        }
    }

    _compare_values(
        old_other,
        new_other,
        "",
        changes,
    )

    return changes


def detect_structural_changes(
    approved_extraction: CompleteExtractionData,
    new_extraction: CompleteExtractionData,
) -> StructuralChangeReport:
    """
    Deterministically compare an approved extraction with a
    newly validated extraction.

    No LLM is used.

    Domain-aware behavior:

    - exam-date ordering is ignored
    - eligibility-rule ordering is ignored
    - eligibility-group ordering is ignored
    - rule value changes are detected as MODIFIED
    - additions/removals remain explicit
    - logical operator changes are detected
    """

    if not isinstance(
        approved_extraction,
        CompleteExtractionData,
    ):
        raise TypeError(
            "approved_extraction must be CompleteExtractionData."
        )

    if not isinstance(
        new_extraction,
        CompleteExtractionData,
    ):
        raise TypeError(
            "new_extraction must be CompleteExtractionData."
        )

    old_data = _normalize_value(
        approved_extraction
    )

    new_data = _normalize_value(
        new_extraction
    )

    changes = _compare_complete_extractions(
        old_data,
        new_data,
    )

    return StructuralChangeReport(
        change_detected=bool(changes),
        changes=changes,
    )