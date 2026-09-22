from pydantic import BaseModel

from app.ai.exam_schemas import ExamInformation
from app.ai.eligibility_schemas import EligibilityRulesData


class CompleteExtractionData(BaseModel):
    exam_information: ExamInformation
    eligibility_rules: EligibilityRulesData