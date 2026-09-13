from sqlalchemy import select
from app.models.eligibility_attribute import EligibilityAttribute
from app.ai.eligibility_schemas import EligibilityRulesData
from app.database.session import SessionLocal
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.eligibility_rule import EligibilityRule
from app.services.eligibility_rule_group_service import create_rule_group


def create_rule(
    rule_group_id,
    attribute_id,
    operator,
    value
):
    with SessionLocal() as s:

        rule_group = s.scalar(
            select(EligibilityRuleGroup).where(
                EligibilityRuleGroup.group_id == rule_group_id
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
def save_extracted_eligibility_rules(
    notification_id: int,
    data: EligibilityRulesData
):
    for group_number, group_data in enumerate(
        data.rule_groups,
        start=1
    ):

        group_id = create_rule_group(
            notification_id=notification_id,
            group_number=group_number,
            logical_operator=group_data.logical_operator
        )

        for rule_data in group_data.rules:

            with SessionLocal() as s:

                attribute = s.scalar(
                    select(EligibilityAttribute).where(
                        EligibilityAttribute.attribute_name
                        == rule_data.attribute
                    )
                )

                if attribute is None:
                    raise ValueError(
                        f"Eligibility attribute not found: "
                        f"{rule_data.attribute}"
                    )

                attribute_id = attribute.attribute_id

            create_rule(
                rule_group_id=group_id,
                attribute_id=attribute_id,
                operator=rule_data.operator,
                value=rule_data.value
            )

    return True