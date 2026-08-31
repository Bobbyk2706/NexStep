from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.student import Student
from app.models.admin import Admin
from app.auth.security import decode_token

bearer_scheme = HTTPBearer(auto_error=True)

# account_status values that block login/access. Everything else
# (including NULL, '', 'active') is treated as active.
_BLOCKED_STATUSES = {"suspended", "inactive", "disabled"}


def is_account_blocked(account_status: str | None) -> bool:
    return (account_status or "").lower() in _BLOCKED_STATUSES


def get_current_principal(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> tuple[str, Student | Admin]:
    """Decodes the access token and loads the matching Student or Admin row.

    Returns (role, principal). Prefer get_current_student / get_current_admin
    in route signatures — this is the shared building block for both.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(creds.credentials)
    except JWTError:
        raise credentials_exception

    if payload.get("type") != "access":
        raise credentials_exception

    role = payload.get("role")
    principal_id = payload.get("sub")
    if role not in ("student", "admin") or principal_id is None:
        raise credentials_exception

    model = Student if role == "student" else Admin
    pk_column = Student.student_id if role == "student" else Admin.admin_id
    principal = db.query(model).filter(pk_column == int(principal_id)).first()

    if principal is None:
        raise credentials_exception
    if role == "student" and is_account_blocked(principal.account_status):
        raise credentials_exception
    if role == "admin" and is_account_blocked(principal.account_status):
        raise credentials_exception

    return role, principal


def get_current_student(
    principal: tuple[str, Student | Admin] = Depends(get_current_principal),
) -> Student:
    role, obj = principal
    if role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access only",
        )
    return obj


def get_current_admin(
    principal: tuple[str, Student | Admin] = Depends(get_current_principal),
) -> Admin:
    role, obj = principal
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only",
        )
    return obj