from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI(title="Doctor Patient API")

@app.get("/")
def home():
    return {"message": "API is running"}

# In-memory storage
doctors = []
patients = []

# SCHEMAS 

class Doctor(BaseModel):
    name: str
    specialization: str
    email: EmailStr
    is_active: bool = True


class Patient(BaseModel):
    name: str
    age: int = Field(gt=0)  # Age must be > 0
    phone: str


# DOCTOR APIs

@app.post("/doctors")
def create_doctor(doctor: Doctor):
    # Check duplicate email
    for d in doctors:
        if d["email"] == doctor.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    doctor_dict = doctor.dict()
    doctor_dict["id"] = len(doctors) + 1
    doctors.append(doctor_dict)

    return doctor_dict


@app.get("/doctors")
def get_doctors():
    return doctors


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")


# PATIENT APIs 

@app.post("/patients")
def create_patient(patient: Patient):
    patient_dict = patient.dict()
    patient_dict["id"] = len(patients) + 1
    patients.append(patient_dict)

    return patient_dict


@app.get("/patients")
def get_patients():
    return patients


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")