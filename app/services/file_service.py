import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models import File


# ✅ Allowed types
ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"]

# ✅ Max size (2MB)
MAX_SIZE = 2 * 1024 * 1024


def save_file(file: UploadFile, db: Session):

    # 🔴 Validate type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 🔴 Read file
    content = file.file.read()

    # 🔴 Validate size
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 2MB)")

    # 🟢 Save to disk
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(content)

    # 🟢 Save metadata
    new_file = File(
        filename=file.filename,
        content_type=file.content_type,
        size=len(content),
        path=file_path
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file