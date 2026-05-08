from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import (
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_reset_token
)
from app.db.session import get_db
from app.utils.response import success_response

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger(__name__)


# =========================
# 🟢 REGISTER
# =========================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return success_response(
        message="User registered successfully"
    )


# =========================
# 🔵 LOGIN
# =========================
@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token({
        "id": db_user.id,
        "sub": db_user.email,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# 🟡 FORGOT PASSWORD
# =========================
@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_reset_token()

    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)

    db.commit()

    return success_response(
        data={
            "reset_token": token   # ⚠️ for dev/testing
        },
        message="Reset token generated"
    )


# =========================
# 🔴 RESET PASSWORD
# =========================
@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.reset_token == data.token).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user.password = hash_password(data.new_password)
    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()

    return success_response(
        message="Password reset successful"
    )