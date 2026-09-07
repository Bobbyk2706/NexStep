from datetime import date

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentSignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    date_of_birth: date
    nationality: str
    state: str
    gender: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: int
    name: str
    email: EmailStr
    account_status: str | None = None


class AdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    admin_id: int
    name: str
    email: EmailStr
    account_status: str | None = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"