from __future__ import annotations

from pydantic import BaseModel, Field


class ChatTurnIn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: list[ChatTurnIn] = Field(default_factory=list, max_length=20)


class ChatSourceOut(BaseModel):
    exam_id: int
    exam_name: str
    notification_title: str | None = None
    official_url: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSourceOut] = Field(default_factory=list)
    grounded: bool
