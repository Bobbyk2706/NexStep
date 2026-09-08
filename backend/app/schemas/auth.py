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


# --- Unified endpoints matching the frontend's contract (POST /auth/signup,
# POST /auth/login) — student-only, single token, no separate refresh flow.
# See app/routers/auth_router.py for why this exists alongside the
# role-specific /auth/student/... and /auth/admin/... routes.

class SimpleSignupRequest(BaseModel):
    name: str
    email: EmailStr
    # Frontend's own client-side check requires 6+ chars — matched here
    # rather than the stricter 8 used by StudentSignupRequest above, so
    # a password the frontend accepts doesn't get rejected by the API.
    password: str = Field(min_length=6, max_length=128)


class UserSummary(BaseModel):
    name: str
    email: EmailStr


class AuthResponse(BaseModel):
    token: str
    user: UserSummary
    hasProfile: bool


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