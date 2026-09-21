from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrackedExamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tracking_id: int
    student_id: int
    exam_id: int
    tracked_at: datetime | None = None
    tracking_status: str