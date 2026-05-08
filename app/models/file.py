from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    content_type = Column(String(100))
    size = Column(Integer)
    path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)