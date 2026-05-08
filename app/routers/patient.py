from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Patient
from app.schemas.patient import PatientCreate
from app.deps import get_db, get_current_user, require_role
from app.utils.rate_limiter import rate_limiter
from app.services.patient_service import create_patient, get_patients
from app.utils.response import success_response

router = APIRouter(prefix="/patients", tags=["Patients"])


# =========================
# ✅ CREATE (ADMIN / PATIENT)
# =========================
@router.post("/")
def create(
    p: PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role not in ["admin", "patient"]:
        raise HTTPException(status_code=403, detail="Access denied")

    patient = create_patient(db, p)

    return success_response(
        data=patient,
        message="Patient created successfully"
    )


# =========================
# ✅ LIST (ADMIN ONLY)
# =========================
@router.get("/")
def list_all(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    name: str = None,
    phone: str = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    rate_limiter(request)

    patients = get_patients(db, skip, limit, sort_by, order, name, phone)

    return success_response(
        data=patients,
        message="Patients fetched successfully"
    )


# =========================
# ✅ UPDATE (OWN / ADMIN)
# =========================
@router.put("/{id}")
def update(
    id: int,
    data: PatientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    p = db.get(Patient, id)

    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    if user.role == "patient" and user.id != id:
        raise HTTPException(status_code=403, detail="Access denied")

    for k, v in data.dict().items():
        setattr(p, k, v)

    db.commit()
    db.refresh(p)

    return success_response(
        data=p,
        message="Patient updated successfully"
    )


# =========================
# ❌ DELETE (OWN / ADMIN)
# =========================
@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    p = db.get(Patient, id)

    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    if user.role == "patient" and user.id != id:
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        db.delete(p)
        db.commit()

        return success_response(message="Patient deleted successfully")

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete patient. Appointments exist."
        )