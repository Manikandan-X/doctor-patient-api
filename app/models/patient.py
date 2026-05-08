from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    name = Column(String(100))
    age = Column(Integer)
    phone = Column(String(20))
    email = Column(String(100), unique=True)