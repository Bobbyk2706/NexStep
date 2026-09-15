from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.eligibility_schemas import (
    EligibilityRuleGroupData,
    EligibilityRulesData,
)
from app.database.session import SessionLocal
from app.models.eligibility_attribute import EligibilityAttribute
from app.models.eligibility_rule import EligibilityRule
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.official_notification import OfficialNotification


SUPPORTED_LOGICAL_OPERATORS = {
    "AND",
    "OR",
}


def create_rule(
    session: Session,
    rule_group_id: int,
    attribute_id: int,
    operator: str,
    value: str,
):
    """
    Create one eligibility rule inside an existing rule group.

    The caller controls the transaction.
    """

    rule_group = session.scalar(
        select(EligibilityRuleGroup).where(
            EligibilityRuleGroup.group_id == rule_group_id
        )
    )

    if rule_group is None:
        raise ValueError(
            "Eligibility rule group not found."
        )

    rule = EligibilityRule(
        attribute_id=attribute_id,
        value=value,
        operator=operator,
    )

    rule_group.rules.append(rule)

    session.add(rule)
    session.flush()

    return rule.rule_id


def _create_rule_group_recursive(
    session: Session,
    notification_id: int,
    group_data: EligibilityRuleGroupData,
    group_number: int,
    parent_group_id: int | None = None,
) -> int:
    """
    Recursively persist one eligibility rule group and
    all of its descendants.

    The logical structure supplied by the extraction is
    preserved exactly.
    """

    logical_operator = group_data.logical_operator.strip().upper()

    if logical_operator not in SUPPORTED_LOGICAL_OPERATORS:
        raise ValueError(
            f"Unsupported logical operator: "
            f"{group_data.logical_operator}"
        )

    rule_group = EligibilityRuleGroup(
        notification_id=notification_id,
        group_number=group_number,
        logical_operator=logical_operator,
        parent_group_id=parent_group_id,
    )

    session.add(rule_group)
    session.flush()

    # ---------------------------------------------------------
    # SAVE RULES BELONGING TO THIS GROUP
    # ---------------------------------------------------------

    for rule_data in group_data.rules:

        attribute = session.scalar(
            select(EligibilityAttribute).where(
                EligibilityAttribute.attribute_name
                == rule_data.attribute
            )
        )

        if attribute is None:
            raise ValueError(
                "Eligibility attribute not found: "
                f"{rule_data.attribute}"
            )

        create_rule(
            session=session,
            rule_group_id=rule_group.group_id,
            attribute_id=attribute.attribute_id,
            operator=rule_data.operator,
            value=rule_data.value,
        )

    # ---------------------------------------------------------
    # SAVE CHILD GROUPS RECURSIVELY
    # ---------------------------------------------------------

    for child_number, child_group in enumerate(
        group_data.child_groups,
        start=1,
    ):
        _create_rule_group_recursive(
            session=session,
            notification_id=notification_id,
            group_data=child_group,
            group_number=child_number,
            parent_group_id=rule_group.group_id,
        )

    return rule_group.group_id


def save_extracted_eligibility_rules(
    notification_id: int,
    data: EligibilityRulesData,
):
    """
    Persist the complete eligibility rule tree.

    One database transaction is used for the entire operation.

    If any group, rule, or attribute fails, the complete
    operation is rolled back.
    """

    with SessionLocal() as session:
        try:

            # -------------------------------------------------
            # VERIFY NOTIFICATION
            # -------------------------------------------------

            notification = session.scalar(
                select(OfficialNotification).where(
                    OfficialNotification.notification_id
                    == notification_id
                )
            )

            if notification is None:
                raise ValueError(
                    "Official notification not found."
                )

            # -------------------------------------------------
            # SAVE ROOT GROUPS
            # -------------------------------------------------

            for group_number, group_data in enumerate(
                data.rule_groups,
                start=1,
            ):
                _create_rule_group_recursive(
                    session=session,
                    notification_id=notification_id,
                    group_data=group_data,
                    group_number=group_number,
                    parent_group_id=None,
                )

            # -------------------------------------------------
            # COMMIT EVERYTHING
            # -------------------------------------------------

            session.commit()

        except Exception:
            session.rollback()
            raise

    return True