from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


# =========================
# DOCTOR SCHEMAS
# =========================

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorResponse(DoctorCreate):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# PATIENT SCHEMAS
# =========================

class PatientCreate(BaseModel):
    name: str
    age: int = Field(gt=0)
    phone: str


class PatientResponse(PatientCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# APPOINTMENT SCHEMAS
# =========================

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime   # ✅ FIXED (better than string)


class AppointmentResponse(AppointmentCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# AUTH SCHEMAS
# =========================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str