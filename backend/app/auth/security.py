"""
Password hashing and JWT helpers used by the auth router.

SECRET_KEY must be overridden via env var (JWT_SECRET_KEY) in any real
deployment — the fallback here only exists so the module runs locally
without extra setup.
"""
import os
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError  # noqa: F401  (JWTError re-exported for callers)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# bcrypt has a hard 72-byte input limit — truncate defensively rather than
# letting long passwords raise at hash/verify time. (Deliberately using
# the bcrypt package directly rather than passlib: passlib's bcrypt
# backend has a known version-detection bug against recent bcrypt
# releases that raises on every hash() call.)
_BCRYPT_MAX_BYTES = 72


def hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    try:
        return bcrypt.checkpw(pw_bytes, password_hash.encode("utf-8"))
    except ValueError:
        return False


def _create_token(subject: str, expires_delta: timedelta, extra_claims: dict) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,          # student_id / admin_id, as a string
        "iat": now,
        "exp": now + expires_delta,
        "jti": uuid.uuid4().hex,
        **extra_claims,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(principal_id: int, role: str) -> str:
    """role is 'student' or 'admin' — embedded so a single token tells you
    which table/model the subject id refers to."""
    return _create_token(
        subject=str(principal_id),
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        extra_claims={"type": "access", "role": role},
    )


def create_refresh_token(principal_id: int, role: str, token_version: str) -> str:
    return _create_token(
        subject=str(principal_id),
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        extra_claims={"type": "refresh", "role": role, "trv": token_version},
    )


def decode_token(token: str) -> dict:
    """Raises jose.JWTError on invalid/expired token — callers should catch it."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def new_token_version() -> str:
    return uuid.uuid4().hex