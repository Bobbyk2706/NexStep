from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.eligibility_rule_group import EligibilityRuleGroup


def create_rule_group(
    notification_id,
    group_number,
    logical_operator
):
    with SessionLocal() as s:

        notification = s.scalar(
            select(OfficialNotification).where(
                OfficialNotification.notification_id
                == notification_id
            )
        )

        if notification is None:
            raise ValueError(
                "Official notification not found."
            )

        rule_group = EligibilityRuleGroup(
            notification_id=notification_id,
            group_number=group_number,
            logical_operator=logical_operator
        )

        notification.rule_groups.append(
            rule_group
        )

        s.add(rule_group)
        s.commit()
        s.refresh(rule_group)

        return rule_group.group_id