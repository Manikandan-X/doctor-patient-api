from fastapi import HTTPException
from datetime import date
from sqlalchemy.orm import Session

from app.models.appointment import Appointment

# ✅ VALID STATUS FLOW
VALID_STATUS = ["pending", "approved", "rejected", "completed", "cancelled"]


# =========================
# ✅ CREATE APPOINTMENT
# =========================
def create_appointment_service(db: Session, data):

    # ✅ 1. Get appointment date directly
    appt_date = data.appointment_date

    # ✅ 2. Prevent past booking
    if appt_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Cannot book past date"
        )

    # ✅ 3. Prevent double booking
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == data.doctor_id,
        Appointment.appointment_date == data.appointment_date,
        Appointment.status != "cancelled"
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Time slot already booked"
        )

    # ✅ 4. Create appointment
    appointment = Appointment(
        doctor_id=data.doctor_id,
        patient_id=data.patient_id,
        appointment_date=data.appointment_date,
        status="pending"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

# =========================
# ✅ GET APPOINTMENT
# =========================

def get_appointments(db, skip, limit, sort_by, order):
    query = db.query(Appointment)

    if hasattr(Appointment, sort_by):
        column = getattr(Appointment, sort_by)
        query = query.order_by(column.desc() if order == "desc" else column.asc())

    return query.offset(skip).limit(limit).all()


# =========================
# ✅ UPDATE STATUS
# =========================
def update_status_service(db: Session, appt: Appointment, new_status: str):

    new_status = new_status.lower()

    # 🔴 1. Validate status
    if new_status not in VALID_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")

    # 🔐 2. Status flow rules

    # ❌ Cannot change after completion
    if appt.status == "completed":
        raise HTTPException(status_code=400, detail="Already completed")

    # ❌ Cannot change after rejection
    if appt.status == "rejected":
        raise HTTPException(status_code=400, detail="Already rejected")

    # ❌ Cannot change after cancellation
    if appt.status == "cancelled":
        raise HTTPException(status_code=400, detail="Already cancelled")

    # ✅ Valid transitions
    if appt.status == "pending" and new_status not in ["approved", "rejected", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid transition")

    if appt.status == "approved" and new_status not in ["completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Invalid transition")

    # 🟢 Update status
    appt.status = new_status

    return appt