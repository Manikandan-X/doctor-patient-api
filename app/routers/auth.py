from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.models import User
from app.schemas import UserCreate, LoginRequest
from app.auth import hash_password, verify_password, create_access_token
from app.deps import get_db

# ✅ Logger setup for this file
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


# 🟢 REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    logger.info(f"Register attempt for email: {user.email}")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.warning(f"User already exists: {user.email}")
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User registered successfully: {user.email}")

    return {"message": "User registered successfully"}


# 🔵 LOGIN
@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):

    logger.info(f"Login attempt for email: {user.email}")

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        logger.error(f"User not found: {user.email}")
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        logger.warning(f"Invalid password attempt for: {user.email}")
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": db_user.email})

    logger.info(f"Login successful: {user.email}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }