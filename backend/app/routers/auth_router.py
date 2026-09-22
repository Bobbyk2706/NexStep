from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.student import Student
from app.models.admin import Admin
from app.auth.dependencies import (
    get_current_principal,
    get_current_student,
    get_current_admin,
    is_account_blocked,
)
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    new_token_version,
    decode_token,
)
from app.schemas.auth import (
    StudentSignupRequest,
    LoginRequest,
    RefreshRequest,
    TokenPair,
    StudentOut,
    AdminOut,
    SimpleSignupRequest,
    AuthResponse,
    UserSummary,
)
from app.routers.profile_router import student_has_profile

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------- signup ---

@router.post(
    "/student/signup",
    response_model=StudentOut,
    status_code=status.HTTP_201_CREATED,
)
def student_signup(payload: StudentSignupRequest, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = Student(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        date_of_birth=payload.date_of_birth,
        nationality=payload.nationality,
        state=payload.state,
        gender=payload.gender,
        account_status="active",
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


# NOTE: no admin self-signup route — admin accounts are provisioned
# directly (e.g. by another admin or a DB seed script), not via a public
# endpoint. Say the word if NexStep needs an admin-invite flow instead.


# ------------------------------------------------ unified (frontend) ---

@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def unified_signup(payload: SimpleSignupRequest, db: Session = Depends(get_db)):
    """Matches the frontend's exact contract: name/email/password only,
    returns a single token (no refresh token — the frontend doesn't
    implement refresh handling) plus hasProfile. Student-only; wraps the
    same Student row /auth/student/signup uses, just with the extra
    fields (DOB/nationality/state/gender) left unset until the profile
    step fills them in via PUT /student/profile."""
    existing = db.query(Student).filter(Student.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    student = Student(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        account_status="active",
        token_version=new_token_version(),
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    access = create_access_token(student.student_id, "student")
    return AuthResponse(
        token=access,
        user=UserSummary(name=student.name, email=student.email),
        hasProfile=False,
    )


@router.post("/login", response_model=AuthResponse)
def unified_login(payload: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == payload.email).first()
    if not student or not verify_password(payload.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if is_account_blocked(student.account_status):
        raise HTTPException(status_code=403, detail="Account is disabled")

    if not student.token_version:
        student.token_version = new_token_version()
        db.commit()

    access = create_access_token(student.student_id, "student")
    return AuthResponse(
        token=access,
        user=UserSummary(name=student.name, email=student.email),
        hasProfile=student_has_profile(db, student.student_id),
    )


# ----------------------------------------------------------------- login ---

@router.post("/student/login", response_model=TokenPair)
def student_login(payload: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == payload.email).first()
    if not student or not verify_password(payload.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if is_account_blocked(student.account_status):
        raise HTTPException(status_code=403, detail="Account is disabled")

    if not student.token_version:
        student.token_version = new_token_version()
        db.commit()

    access = create_access_token(student.student_id, "student")
    refresh = create_refresh_token(student.student_id, "student", student.token_version)
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/admin/login", response_model=TokenPair)
def admin_login(payload: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == payload.email).first()
    if not admin or not verify_password(payload.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if is_account_blocked(admin.account_status):
        raise HTTPException(status_code=403, detail="Account is disabled")

    if not admin.token_version:
        admin.token_version = new_token_version()
        db.commit()

    access = create_access_token(admin.admin_id, "admin")
    refresh = create_refresh_token(admin.admin_id, "admin", admin.token_version)
    return TokenPair(access_token=access, refresh_token=refresh)


# --------------------------------------------------------- refresh/logout ---

@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    invalid = HTTPException(status_code=401, detail="Invalid or expired refresh token")
    try:
        claims = decode_token(payload.refresh_token)
    except JWTError:
        raise invalid

    if claims.get("type") != "refresh":
        raise invalid

    role = claims.get("role")
    principal_id = claims.get("sub")
    if role not in ("student", "admin") or principal_id is None:
        raise invalid

    model = Student if role == "student" else Admin
    pk_column = Student.student_id if role == "student" else Admin.admin_id
    principal = db.query(model).filter(pk_column == int(principal_id)).first()

    if principal is None or is_account_blocked(principal.account_status):
        raise invalid
    # Reject refresh tokens issued before the last logout/rotation.
    if claims.get("trv") != principal.token_version:
        raise invalid

    # Rotate: issue a brand new refresh token and invalidate this one by
    # bumping token_version, so a stolen refresh token can't be reused
    # after the legitimate client rotates.
    principal.token_version = new_token_version()
    db.commit()

    access = create_access_token(int(principal_id), role)
    new_refresh = create_refresh_token(int(principal_id), role, principal.token_version)
    return TokenPair(access_token=access, refresh_token=new_refresh)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    principal: tuple[str, Student | Admin] = Depends(get_current_principal),
    db: Session = Depends(get_db),
):
    """Invalidates all outstanding refresh tokens for the current student/admin."""
    _, obj = principal
    obj.token_version = new_token_version()
    db.commit()


# -------------------------------------------------------------------- me ---

@router.get("/me", response_model=Union[StudentOut, AdminOut])
def read_me(principal: tuple[str, Student | Admin] = Depends(get_current_principal)):
    _, obj = principal
    return obj


@router.get("/admin/ping", response_model=AdminOut)
def admin_only_example(current_admin: Admin = Depends(get_current_admin)):
    """Example of a role-gated route — reuse Depends(get_current_admin) like this."""
    return current_admin


@router.get("/student/ping", response_model=StudentOut)
def student_only_example(current_student: Student = Depends(get_current_student)):
    """Example of a role-gated route — reuse Depends(get_current_student) like this."""
    return current_student