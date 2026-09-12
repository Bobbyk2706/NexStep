from pydantic import BaseModel, Field


class EligibilityRuleData(BaseModel):
    attribute: str
    operator: str
    value: str


class EligibilityRuleGroupData(BaseModel):
    logical_operator: str
    rules: list[EligibilityRuleData] = Field(
        default_factory=list
    )


class EligibilityRulesData(BaseModel):
    rule_groups: list[EligibilityRuleGroupData] = Field(
        default_factory=list
    )