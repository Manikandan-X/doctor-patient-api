from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Doctor
from app.schemas import DoctorCreate, DoctorResponse
from app.deps import get_db, get_current_user
from app.utils.rate_limiter import rate_limiter

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# ✅ CREATE
@router.post("/", response_model=DoctorResponse)
def create(doc: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**doc.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


# ✅ GET ALL + PAGINATION + FILTER
@router.get("/", response_model=list[DoctorResponse])
def list_all(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    specialization: str = None,
    db: Session = Depends(get_db)
):
    rate_limiter(request)
    query = db.query(Doctor)

    # only active doctors
    query = query.filter(Doctor.is_active == True)

    # filter by specialization
    if specialization:
        query = query.filter(Doctor.specialization == specialization)

    return query.offset(skip).limit(limit).all()


# ✅ SEARCH (NEW FEATURE)
@router.get("/search", response_model=list[DoctorResponse])
def search_doctors(
    name: str = Query(...),
    db: Session = Depends(get_db)
):
    return db.query(Doctor).filter(Doctor.name.contains(name)).all()


# ✅ UPDATE
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


# ✅ DELETE
@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
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


# ✅ ACTIVATE
@router.patch("/{id}/activate", response_model=DoctorResponse)
def activate(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doc.is_active = True
    db.commit()
    db.refresh(doc)

    return doc


# ✅ DEACTIVATE
@router.patch("/{id}/deactivate", response_model=DoctorResponse)
def deactivate(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    doc = db.get(Doctor, id)

    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doc.is_active = False
    db.commit()
    db.refresh(doc)

    return doc