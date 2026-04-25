from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Patient
from app.schemas import PatientCreate, PatientResponse
from app.deps import get_db, get_current_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/")
def create(
    p: PatientCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    patient = Patient(**p.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/")
def list_all(
    name: str = None,
    phone: str = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = db.query(Patient)

    if name:
        query = query.filter(Patient.name.contains(name))
    if phone:
        query = query.filter(Patient.phone.contains(phone))

    return query.all()


@router.put("/{id}", response_model=PatientResponse)
def update(
    id: int,
    data: PatientCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    p = db.get(Patient, id)

    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    for k, v in data.dict().items():
        setattr(p, k, v)

    db.commit()
    db.refresh(p)

    return p


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    p = db.get(Patient, id)

    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    try:
        db.delete(p)
        db.commit()
        return {"msg": "Deleted"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete patient. Appointments exist for this patient."
        )