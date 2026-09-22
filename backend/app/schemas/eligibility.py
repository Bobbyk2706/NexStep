from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EligibilityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    eligibility_id: int
    student_id: int
    exam_id: int
    eligibility_status: str
    reason: str | None = None
    evaluated_at: datetime | None = None