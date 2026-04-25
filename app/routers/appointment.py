from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Appointment, Doctor
from app.schemas import AppointmentCreate, AppointmentResponse
from app.deps import get_db, get_current_user
 

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse)
def create(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    # ✅ STEP 1 — check doctor
    doctor = db.get(Doctor, data.doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor not available")

    # ✅ STEP 2 — create appointment
    appt = Appointment(**data.dict())
    appt.status = "scheduled"

    db.add(appt)
    db.commit()
    db.refresh(appt)

    return appt

@router.get("/", response_model=list[AppointmentResponse])
def get_all(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Appointment).all()


@router.get("/doctor/{doctor_id}", response_model=list[AppointmentResponse])
def get_by_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()


@router.get("/patient/{patient_id}", response_model=list[AppointmentResponse])
def get_by_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


@router.patch("/{id}/cancel", response_model=AppointmentResponse)
def cancel(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(404, "Appointment not found")

    if appt.status == "completed":
        raise HTTPException(400, "Cannot cancel completed appointment")

    appt.status = "cancelled"

    db.commit()
    db.refresh(appt)

    return appt

@router.patch("/{id}/complete", response_model=AppointmentResponse)
def complete(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(404, "Appointment not found")

    if appt.status == "cancelled":
        raise HTTPException(400, "Cannot complete cancelled appointment")

    appt.status = "completed"

    db.commit()
    db.refresh(appt)

    return appt