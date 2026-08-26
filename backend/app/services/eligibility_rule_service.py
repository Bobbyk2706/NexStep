from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.eligibility_rule import EligibilityRule


def create_rule(
    rule_group_id,
    attribute_id,
    operator,
    value
):
    with SessionLocal() as s:

        rule_group = s.scalar(
            select(EligibilityRuleGroup).where(
                EligibilityRuleGroup.rule_group_id == rule_group_id
            )
        )

        rule = EligibilityRule(
            attribute_id=attribute_id,
            operator=operator,
            value=value
        )

        rule_group.rules.append(rule)

        s.add(rule)
        s.commit()

        return rule.rule_id