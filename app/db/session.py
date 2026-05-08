import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ✅ LOAD ENV HERE (IMPORTANT)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ SAFETY CHECK
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set. Check your .env file")

# ✅ SQLite fix (if using sqlite)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()