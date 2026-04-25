from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.auth import verify_token
from app.database import SessionLocal

security = HTTPBearer()

def get_current_user(credentials=Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing token")

    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()