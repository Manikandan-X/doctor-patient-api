from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(100), unique=True, index=True, nullable=False)

    password = Column(String(255), nullable=False)

    # ✅ RBAC
    role = Column(String(50), default="patient")

    # ⚠️ FIXED: use Boolean instead of string (VERY IMPORTANT)
    is_active = Column(Boolean, default=True)

    # 🔐 password reset
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)