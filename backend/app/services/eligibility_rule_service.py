from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.eligibility_attribute import EligibilityAttribute
from app.ai.eligibility_schemas import EligibilityRulesData
from app.database.session import SessionLocal
from app.models.eligibility_rule_group import EligibilityRuleGroup
from app.models.eligibility_rule import EligibilityRule


def create_rule(
    session: Session,
    rule_group_id: int,
    attribute_id: int,
    operator: str,
    value: str
):
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
        operator=operator,
        value=value
    )

    rule_group.rules.append(rule)

    session.add(rule)
    session.flush()

    return rule.rule_id


def save_extracted_eligibility_rules(
    notification_id: int,
    data: EligibilityRulesData
):
    with SessionLocal() as session:

        try:
            for group_number, group_data in enumerate(
                data.rule_groups,
                start=1
            ):

                # Create rule group
                rule_group = EligibilityRuleGroup(
                    notification_id=notification_id,
                    group_number=group_number,
                    logical_operator=group_data.logical_operator
                )

                session.add(rule_group)
                session.flush()

                # Create rules inside the same transaction
                for rule_data in group_data.rules:

                    attribute = session.scalar(
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

                    create_rule(
                        session=session,
                        rule_group_id=rule_group.group_id,
                        attribute_id=attribute.attribute_id,
                        operator=rule_data.operator,
                        value=rule_data.value
                    )

            session.commit()

        except Exception:
            session.rollback()
            raise

    return True