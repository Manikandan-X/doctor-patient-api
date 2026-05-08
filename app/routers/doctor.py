from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Doctor
from app.schemas.doctor import DoctorCreate
from app.deps import get_db, require_role
from app.services.doctor_service import create_doctor, get_doctors
from app.utils.response import success_response

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# =========================
# ✅ CREATE (ADMIN ONLY)
# =========================
@router.post("/")
def create(
    doc: DoctorCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    doctor = create_doctor(db, doc)

    return success_response(
        data=doctor,
        message="Doctor created successfully"
    )


# =========================
# ✅ GET ALL
# =========================
@router.get("/")
def list_all(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    doctors = get_doctors(db, skip, limit, sort_by, order)

    return success_response(
        data=doctors,
        message="Doctors fetched successfully"
    )


# =========================
# ✅ SEARCH
# =========================
@router.get("/search")
def search_doctors(
    name: str = Query(None),
    specialization: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Doctor).filter(Doctor.is_active == True)

    if name:
        query = query.filter(Doctor.name.ilike(f"%{name}%"))

    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))

    doctors = query.all()

    return success_response(
        data=doctors,
        message="Search results fetched"
    )


# =========================
# ✅ UPDATE
# =========================
@router.put("/{id}")
def update(
    id: int,
    data: DoctorCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for k, v in data.dict().items():
        setattr(doc, k, v)

    db.commit()
    db.refresh(doc)

    return success_response(
        data=doc,
        message="Doctor updated successfully"
    )


# =========================
# ✅ DELETE
# =========================
@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        db.delete(doc)
        db.commit()

        return success_response(message="Doctor deleted successfully")

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete doctor. Appointments exist."
        )


# =========================
# ✅ ACTIVATE
# =========================
@router.patch("/{id}/activate")
def activate(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doc.is_active = True
    db.commit()
    db.refresh(doc)

    return success_response(
        data=doc,
        message="Doctor activated"
    )


# =========================
# ✅ DEACTIVATE
# =========================
@router.patch("/{id}/deactivate")
def deactivate(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doc.is_active = False
    db.commit()
    db.refresh(doc)

    return success_response(
        data=doc,
        message="Doctor deactivated"
    )