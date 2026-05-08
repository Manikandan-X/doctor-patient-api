from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(100))
    specialization = Column(String(100))
    email = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)