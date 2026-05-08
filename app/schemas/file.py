from pydantic import BaseModel
from datetime import datetime


class FileResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    size: int
    path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True