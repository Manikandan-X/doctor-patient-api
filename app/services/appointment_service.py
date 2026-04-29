from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Appointment, Doctor


def create_appointment_service(db: Session, data):
    # ✅ check doctor
    doctor = db.get(Doctor, data.doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor not available")

    # ✅ create appointment
    appt = Appointment(**data.dict())
    appt.status = "scheduled"

    db.add(appt)
    db.commit()
    db.refresh(appt)

    return appt