from datetime import date
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
)


# ---------------------------------------------------------------- email ---
#
# Strict email type used for everything the client SENDS (signup/login).
# It trims whitespace and requires a real dotted domain with a 2+ letter
# ending, so "example@nexstep" is rejected but "name@example.com" and
# "name@college.ac.in" pass.
#
# Response models below deliberately use plain `str` for email, so a
# legacy row with a bad address can never turn a response into a 500.


def _strip(value):
    return value.strip() if isinstance(value, str) else value


def _require_dotted_domain(value: str) -> str:
    domain = value.rpartition("@")[2]
    labels = domain.split(".")

    if len(labels) < 2 or not all(labels) or len(labels[-1]) < 2:
        raise ValueError(
            "Enter a valid email address, for example name@example.com"
        )

    return value


StrictEmail = Annotated[
    EmailStr,
    BeforeValidator(_strip),
    AfterValidator(_require_dotted_domain),
]


# --------------------------------------------------------------- requests ---


class StudentSignupRequest(BaseModel):
    name: str
    email: StrictEmail
    password: str = Field(min_length=8, max_length=128)
    date_of_birth: date
    nationality: str
    state: str
    gender: str


class LoginRequest(BaseModel):
    email: StrictEmail
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


# Unified endpoints matching the frontend's contract (POST /auth/signup,
# POST /auth/login): student-only, single token, no refresh flow.


class SimpleSignupRequest(BaseModel):
    name: str
    email: StrictEmail
    # The frontend requires 6+ characters, so the API matches it.
    password: str = Field(min_length=6, max_length=128)


# -------------------------------------------------------------- responses ---


class UserSummary(BaseModel):
    name: str
    email: str


class AuthResponse(BaseModel):
    token: str
    user: UserSummary
    hasProfile: bool


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: int
    name: str
    email: str
    account_status: str | None = None


class AdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    admin_id: int
    name: str
    email: str
    account_status: str | None = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"