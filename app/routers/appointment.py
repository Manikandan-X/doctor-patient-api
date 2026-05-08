from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Query
from sqlalchemy.orm import Session

from app.models import Appointment, Doctor
from app.schemas.appointment import AppointmentCreate
from app.deps import get_db, require_role
from app.services.appointment_service import (
    create_appointment_service,
    update_status_service,
    get_appointments
)
from app.utils.rate_limiter import rate_limiter
from app.websocket_manager import manager
from app.utils.background_tasks import log_appointment_creation
from app.utils.response import success_response
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/appointments", tags=["Appointments"])


# =========================
# ✅ CREATE (PATIENT ONLY)
# =========================
@router.post("/")
async def create(
    data: AppointmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(require_role("patient"))
):
    doctor = db.get(Doctor, data.doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor not available")

    appt = create_appointment_service(db, data)

    db.commit()
    db.refresh(appt)

    background_tasks.add_task(log_appointment_creation, data.doctor_id)

    await manager.send(
        str(data.doctor_id),
        f"New appointment booked (Doctor ID {data.doctor_id})"
    )

    return success_response(
        data=appt,
        message="Appointment created successfully"
    )


# =========================
# ✅ GET ALL (ADMIN ONLY)
# =========================
@router.get("/")
def get_all(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    rate_limiter(request)

    data = get_appointments(db, skip, limit, sort_by, order)

    return success_response(
        data=data,
        message="Appointments fetched successfully"
    )


# =========================
# ✅ FILTER
# =========================
@router.get("/filter")
def filter_appointments(
    date: str = Query(None),
    status: str = Query(None),
    doctor_id: int = Query(None),
    patient_id: int = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Appointment)

    if user["role"] == "doctor":
        query = query.filter(Appointment.doctor_id == user["id"])

    elif user["role"] == "patient":
        query = query.filter(Appointment.patient_id == user["id"])

    if date:
        query = query.filter(Appointment.appointment_date.contains(date))

    if status:
        query = query.filter(Appointment.status == status.lower())

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)

    data = query.all()

    return success_response(
        data=data,
        message="Filtered appointments fetched"
    )


# =========================
# ✅ DOCTOR VIEW
# =========================
@router.get("/doctor/{doctor_id}")
def get_by_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("doctor"))
):
    if user.id != doctor_id:
        raise HTTPException(status_code=403, detail="Access denied")

    data = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).all()

    return success_response(
        data=data,
        message="Doctor appointments fetched"
    )


# =========================
# ✅ PATIENT VIEW
# =========================
@router.get("/patient/{patient_id}")
def get_by_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("patient"))
):
    if user.id != patient_id:
        raise HTTPException(status_code=403, detail="Access denied")

    data = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).all()

    return success_response(
        data=data,
        message="Patient appointments fetched"
    )


# =========================
# ❌ CANCEL
# =========================
@router.patch("/{id}/cancel")
async def cancel(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if user["role"] == "patient" and appt.patient_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not your appointment")

    if appt.status in ["completed", "rejected"]:
        raise HTTPException(status_code=400, detail="Cannot cancel")

    appt.status = "cancelled"

    db.commit()
    db.refresh(appt)

    await manager.send(
        str(appt.doctor_id),
        "Appointment CANCELLED"
    )

    return success_response(
        data=appt,
        message="Appointment cancelled"
    )


# =========================
# ✅ APPROVE
# =========================
@router.patch("/{id}/approve")
def approve(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("doctor"))
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.doctor_id != user.id:
        raise HTTPException(status_code=403, detail="Not your appointment")

    update_status_service(db, appt, "approved")

    db.commit()
    db.refresh(appt)

    return success_response(
        data=appt,
        message="Appointment approved"
    )


# =========================
# ❌ REJECT
# =========================
@router.patch("/{id}/reject")
def reject(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("doctor"))
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.doctor_id != user.id:
        raise HTTPException(status_code=403, detail="Not your appointment")

    update_status_service(db, appt, "rejected")

    db.commit()
    db.refresh(appt)

    return success_response(
        data=appt,
        message="Appointment rejected"
    )


# =========================
# ✅ COMPLETE
# =========================
@router.patch("/{id}/complete")
async def complete(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("doctor"))
):
    appt = db.get(Appointment, id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.doctor_id != user.id:
        raise HTTPException(status_code=403, detail="Not your appointment")

    update_status_service(db, appt, "completed")

    db.commit()
    db.refresh(appt)

    await manager.send(
        str(appt.doctor_id),
        "Appointment COMPLETED"
    )

    return success_response(
        data=appt,
        message="Appointment completed"
    )