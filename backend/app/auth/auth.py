import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user, require_role
from models import User, Role
from schemas import SignupRequest, LoginRequest, RefreshRequest, TokenPair, UserOut

from security import(
    hash_password,
    verify_passowrd,
    create_access_token,
    create_refresh_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])
 
 
@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
 
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=Role.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
 
 
@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")
 
    access = create_access_token(str(user.id), user.role.value)
    refresh = create_refresh_token(str(user.id), user.token_version)
    return TokenPair(access_token=access, refresh_token=refresh)
 
 
@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    invalid = HTTPException(status_code=401, detail="Invalid or expired refresh token")
    try:
        claims = decode_token(payload.refresh_token)
    except JWTError:
        raise invalid
 
    if claims.get("type") != "refresh":
        raise invalid
 
    user = db.query(User).filter(User.id == claims.get("sub")).first()
    if user is None or not user.is_active:
        raise invalid
 
    # Reject refresh tokens issued before the last logout/rotation.
    if claims.get("trv") != user.token_version:
        raise invalid
 
    # Rotate: issue a brand new refresh token and invalidate this one by
    # bumping token_version, so a stolen refresh token can't be reused
    # after the legitimate client rotates.
    user.token_version = uuid.uuid4().hex
    db.commit()
 
    access = create_access_token(str(user.id), user.role.value)
    new_refresh = create_refresh_token(str(user.id), user.token_version)
    return TokenPair(access_token=access, refresh_token=new_refresh)
 
 
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Invalidates all outstanding refresh tokens for this user."""
    current_user.token_version = uuid.uuid4().hex
    db.commit()
 
 
@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
 
 
@router.get("/admin-only", response_model=UserOut)
def admin_only(current_user: User = Depends(require_role(Role.ADMIN))):
    """Example of a role-gated route — reuse require_role(...) like this."""
    return current_user
 