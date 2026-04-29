from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session

from app.models import Appointment, Doctor
from app.schemas import AppointmentCreate, AppointmentResponse
from app.deps import get_db, get_current_user
from app.services.appointment_service import create_appointment_service
from app.utils.rate_limiter import rate_limiter
from app.websocket_manager import manager

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# 📩 Background task (assignment requirement)
def send_notification_log():
    print("Notification logged: Appointment created")


# =========================
# ✅ CREATE APPOINTMENT
# =========================
@router.post("/", response_model=AppointmentResponse)
async def create(
    data: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    doctor = db.get(Doctor, data.doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor not available")

    # ✅ create appointment
    appt = create_appointment_service(db, data)

    db.commit()
    db.refresh(appt)

    # background log
    background_tasks.add_task(send_notification_log)

    # 🔔 WebSocket notify doctor
    await manager.send(
        str(data.doctor_id),
        f"New appointment booked (Doctor ID {data.doctor_id})"
    )

    return appt


# =========================
# ✅ GET ALL APPOINTMENTS
# =========================
@router.get("/", response_model=list[AppointmentResponse])
def get_all(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    rate_limiter(request)
    return db.query(Appointment).offset(skip).limit(limit).all()


# =========================
# ✅ GET BY DOCTOR
# =========================
@router.get("/doctor/{doctor_id}", response_model=list[AppointmentResponse])
def get_by_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).all()


# =========================
# ✅ GET BY PATIENT
# =========================
@router.get("/patient/{patient_id}", response_model=list[AppointmentResponse])
def get_by_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).all()


# =========================
# ❌ CANCEL APPOINTMENT
# =========================
@router.patch("/{id}/cancel", response_model=AppointmentResponse)
async def cancel(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.status == "completed":
        raise HTTPException(status_code=400, detail="Cannot cancel completed appointment")

    appt.status = "cancelled"

    db.commit()
    db.refresh(appt)

    # 🔔 WebSocket notify
    await manager.send(
        str(appt.doctor_id),
        "Appointment CANCELLED"
    )

    return appt


# =========================
# ✅ COMPLETE APPOINTMENT
# =========================
@router.patch("/{id}/complete", response_model=AppointmentResponse)
async def complete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.status == "cancelled":
        raise HTTPException(status_code=400, detail="Cannot complete cancelled appointment")

    appt.status = "completed"

    db.commit()
    db.refresh(appt)

    # 🔔 WebSocket notify
    await manager.send(
        str(appt.doctor_id),
        "Appointment COMPLETED"
    )

    return appt