from sqlalchemy.orm import Session
from app.models import Patient
from fastapi import HTTPException
from app.models.user import User

def create_patient(db: Session, data):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    patient = Patient(
        id=user.id,
        name=data.name,
        age=data.age,
        phone=data.phone,
        email=data.email
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_patients(db: Session, skip, limit, sort_by, order, name, phone):
    query = db.query(Patient)

    # 🔍 Filters
    if name:
        query = query.filter(Patient.name.contains(name))

    if phone:
        query = query.filter(Patient.phone.contains(phone))

    # ✅ Safe sorting
    if hasattr(Patient, sort_by):
        column = getattr(Patient, sort_by)

        if order.lower() == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    # ✅ Limit protection
    limit = min(limit, 100)

    return query.offset(skip).limit(limit).all()