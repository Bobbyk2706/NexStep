from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ConductingBodyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    body_id: int
    name: str
    main_website: str
    description: str | None = None
    logo_url: str | None = None


class ExamDateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    exam_date_id: int
    start_date: date
    end_date: date


class OfficialNotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    notification_id: int
    title: str
    notification_type: str
    release_date: date | None = None
    application_start_date: date | None = None
    application_end_date: date | None = None
    official_url: str
    document_url: str | None = None
    ai_summary: str | None = None
    ai_change_summary: str | None = None
    exam_dates: list[ExamDateOut] = Field(default_factory=list)


class ExamListOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    exam_id: int
    name: str
    type: str
    description: str | None = None
    off_exam_page: str | None = None
    status: str | None = None
    conducting_body: ConductingBodyOut


class ExamDetailOut(ExamListOut):
    latest_approved_notification: OfficialNotificationOut | None = None