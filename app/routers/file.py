from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
import shutil

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads"

# ✅ Ensure folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ Upload file (SAFE VERSION)
@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        # ⭐ Generate unique filename to avoid overwrite
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "File uploaded successfully",
            "filename": unique_filename,
            "file_url": f"/uploads/{unique_filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ✅ View / Download file
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