# Doctor Patient FastAPI Project

## 📌 Description
This project is a simple REST API built using FastAPI to manage Doctors and Patients.

## 🛠 Tech Stack
- Python 3.12
- FastAPI
- Pydantic
- Uvicorn

## ▶️ Setup Instructions

1. Install dependencies:
   pip install fastapi uvicorn

2. Run the server:
   uvicorn main:app --reload

3. Open browser:
   http://127.0.0.1:8000/docs

## 📡 API Endpoints

### Doctors
- POST /doctors → Create doctor
- GET /doctors → List doctors
- GET /doctors/{doctor_id} → Get doctor by ID

### Patients
- POST /patients → Create patient
- GET /patients → List patients
- GET /patients/{patient_id} → Get patient by ID

## ✅ Validation
- Email is validated using Pydantic
- Age must be greater than 0

## ⚠️ Error Handling
- 404 if resource not found
- 400 for duplicate doctor email