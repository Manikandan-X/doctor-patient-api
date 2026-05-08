from sqlalchemy.orm import Session
from app.models import Doctor
from app.utils.cache import get_cache, set_cache, clear_doctor_cache
from fastapi import HTTPException
from app.models.user import User

# =========================
# ✅ CREATE DOCTOR
# =========================
def create_doctor(db: Session, data):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    doctor = Doctor(
        id=user.id,
        name=data.name,
        email=data.email,
        specialization=data.specialization
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    # ❗ Clear all doctor cache
    clear_doctor_cache()

    return doctor


# =========================
# ✅ GET DOCTORS (WITH CACHE)
# =========================
def get_doctors(db: Session, skip: int, limit: int, sort_by: str, order: str):

    cache_key = f"doctors:{skip}:{limit}:{sort_by}:{order}"

    # ✅ Try cache first
    cached = get_cache(cache_key)
    if cached is not None:
        return cached

    # 🔴 DB query
    query = db.query(Doctor).filter(Doctor.is_active == True)

    # ✅ Sorting
    if hasattr(Doctor, sort_by):
        column = getattr(Doctor, sort_by)
        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    result = query.offset(skip).limit(limit).all()

    # ✅ Store in cache
    set_cache(cache_key, result)

    return result


# =========================
# ✅ UPDATE DOCTOR
# =========================
def update_doctor(db: Session, doctor_id: int, data):
    doctor = db.get(Doctor, doctor_id)

    if not doctor:
        return None

    for key, value in data.dict().items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    # ❗ Clear cache after update
    clear_doctor_cache()

    return doctor


# =========================
# ✅ DELETE DOCTOR
# =========================
def delete_doctor(db: Session, doctor_id: int):
    doctor = db.get(Doctor, doctor_id)

    if not doctor:
        return None

    db.delete(doctor)
    db.commit()

    # ❗ Clear cache after delete
    clear_doctor_cache()

    return True