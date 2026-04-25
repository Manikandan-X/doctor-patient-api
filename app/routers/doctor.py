from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Doctor
from app.schemas import DoctorCreate, DoctorResponse
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# CREATE
@router.post("/", response_model=DoctorResponse)
def create(doc: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**doc.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


# GET ALL
@router.get("/", response_model=list[DoctorResponse])
def list_all(skip: int = 0, limit: int = 10, specialization: str = None, db: Session = Depends(get_db)):
    query = db.query(Doctor)
    query = query.filter(Doctor.is_active == True)
    if specialization:
        query = query.filter(Doctor.specialization == specialization)

    return query.offset(skip).limit(limit).all()


# UPDATE
@router.put("/{id}", response_model=DoctorResponse)
def update(id: int, data: DoctorCreate, db: Session = Depends(get_db)):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    for k, v in data.dict().items():
        setattr(doc, k, v)

    db.commit()
    db.refresh(doc)
    return doc


# DELETE
@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    try:
        db.delete(doc)
        db.commit()
        return {"msg": "Doctor deleted"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete doctor. Appointments exist for this doctor."
        )


# Activate doctor
@router.patch("/{id}/activate", response_model=DoctorResponse)
def activate(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(404, "Doctor not found")

    doc.is_active = True

    db.commit()
    db.refresh(doc)

    return doc

# Deactivate doctor

@router.patch("/{id}/deactivate", response_model=DoctorResponse)
def deactivate(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(404, "Doctor not found")

    doc.is_active = False

    db.commit()
    db.refresh(doc)

    return doc