from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid

from app.db.session import get_db
from app.models.file import File as FileModel
from app.deps import get_current_user
from app.utils.background_tasks import process_uploaded_file
from app.utils.response import success_response   # ✅ NEW

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = ["image/jpeg", "image/png", "application/pdf"]
MAX_SIZE = 2 * 1024 * 1024


# =========================
# ✅ UPLOAD FILE
# =========================
@router.post("/upload")
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        # 🔴 Validate type
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type")

        content = file.file.read()

        # 🔴 Validate size
        if len(content) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 2MB)")

        # ⭐ Unique filename
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # 🟢 Save file
        with open(file_path, "wb") as buffer:
            buffer.write(content)

        # 🟢 Save metadata
        new_file = FileModel(
            filename=unique_filename,
            content_type=file.content_type,
            size=len(content),
            path=file_path
        )

        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        # ✅ Background task
        background_tasks.add_task(process_uploaded_file, unique_filename)

        return success_response(
            data={
                "file_id": new_file.id,
                "file_url": f"/uploads/{unique_filename}"
            },
            message="File uploaded successfully"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# =========================
# ✅ DOWNLOAD FILE
# =========================
@router.get("/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )