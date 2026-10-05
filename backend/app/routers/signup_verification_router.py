from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth.security import create_access_token
from app.database.session import get_db
from app.schemas.auth import AuthResponse, StrictEmail, UserSummary
from app.services.signup_verification_service import (
    SignupVerificationError,
    resend_code,
    start_signup,
    verify_signup,
)

router = APIRouter(prefix="/auth/register", tags=["auth-register"])


class StartSignupRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: StrictEmail
    password: str = Field(min_length=6, max_length=128)


class VerifySignupRequest(BaseModel):
    email: StrictEmail
    code: str = Field(pattern=r"^\d{6}$")


class ResendCodeRequest(BaseModel):
    email: StrictEmail


def _http_error(exc: SignupVerificationError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=str(exc))


@router.post("/start")
def start(payload: StartSignupRequest, db: Session = Depends(get_db)):
    """Step 1: email a verification code. No account is created yet."""

    try:
        return start_signup(
            db,
            name=payload.name,
            email=payload.email,
            password=payload.password,
        )
    except SignupVerificationError as exc:
        raise _http_error(exc) from exc


@router.post(
    "/verify",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def verify(payload: VerifySignupRequest, db: Session = Depends(get_db)):
    """Step 2: confirm the code. The account is created only now."""

    try:
        student = verify_signup(db, email=payload.email, code=payload.code)
    except SignupVerificationError as exc:
        raise _http_error(exc) from exc

    return AuthResponse(
        token=create_access_token(student.student_id, "student"),
        user=UserSummary(name=student.name, email=student.email),
        hasProfile=False,
    )


@router.post("/resend")
def resend(payload: ResendCodeRequest, db: Session = Depends(get_db)):
    """Send a fresh code for a signup that is waiting for verification."""

    try:
        return resend_code(db, email=payload.email)
    except SignupVerificationError as exc:
        raise _http_error(exc) from exc