from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.official_notification import OfficialNotification
from app.models.eligibility_rule_group import EligibilityRuleGroup


def create_rule_group(
    session: Session,
    notification_id: int,
    group_number: int,
    logical_operator: str,
    parent_group_id: int | None = None
):
    notification = session.scalar(
        select(OfficialNotification).where(
            OfficialNotification.notification_id == notification_id
        )
    )

    if notification is None:
        raise ValueError(
            "Official notification not found."
        )

    if parent_group_id is not None:
        parent_group = session.scalar(
            select(EligibilityRuleGroup).where(
                EligibilityRuleGroup.group_id == parent_group_id
            )
        )

        if parent_group is None:
            raise ValueError(
                "Parent eligibility rule group not found."
            )

    rule_group = EligibilityRuleGroup(
        notification_id=notification_id,
        group_number=group_number,
        logical_operator=logical_operator,
        parent_group_id=parent_group_id
    )

    session.add(rule_group)
    session.flush()

    return rule_group.group_id