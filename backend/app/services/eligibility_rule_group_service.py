from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.eligibility_rule_group import EligibilityRuleGroup


def create_rule_group(
    notification_id,
    group_name,
    group_type
):
    with SessionLocal() as s:

        notification = s.scalar(
            select(OfficialNotification).where(
                OfficialNotification.notification_id == notification_id
            )
        )

        rule_group = EligibilityRuleGroup(
            group_name=group_name,
            group_type=group_type
        )

        notification.rule_groups.append(rule_group)

        s.add(rule_group)
        s.commit()

        return rule_group.rule_group_id