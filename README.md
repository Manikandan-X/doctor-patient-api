# 🏥 Doctor Appointment API (FastAPI)

A backend API built using FastAPI to manage doctors, patients, and appointments with JWT authentication.

---

## 🚀 Features

* 🔐 JWT Authentication (Register & Login)
* 👨‍⚕️ Doctor Management (CRUD + Activate/Deactivate)
* 🧑‍🤝‍🧑 Patient Management (CRUD)
* 📅 Appointment Booking System
* ✅ Appointment Status (Scheduled / Completed / Cancelled)
* 🔎 Filtering (Doctor specialization, Patient search)
* 📄 Pagination support
* ⚙️ Environment variables (.env)
* 🧱 Clean modular structure

---

## 🛠 Tech Stack

* FastAPI
* Python
* SQLAlchemy
* MySQL
* Pydantic
* JWT (python-jose)
* Passlib (bcrypt)

---

## 📂 Project Structure

```
app/
 ├── routers/
 │    ├── auth.py
 │    ├── doctor.py
 │    ├── patient.py
 │    ├── appointment.py
 │
 ├── models/
 ├── schemas/
 ├── database.py
 ├── deps.py
 ├── auth.py
 ├── main.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/Manikandan-X/doctor-patient-api
cd doctor-api
```

---

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` file

```
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5️⃣ Run the server

```
uvicorn app.main:app --reload
```

---

### 6️⃣ Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication

### Register

```
POST /auth/register
```

### Login

```
POST /auth/login
```

👉 Returns JWT token → use in Authorization header:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### 👨‍⚕️ Doctors

* POST `/doctors/` → Create doctor
* GET `/doctors/` → Get all doctors (with filter & pagination)
* PUT `/doctors/{id}` → Update doctor
* DELETE `/doctors/{id}` → Delete doctor
* PATCH `/doctors/{id}/activate` → Activate doctor
* PATCH `/doctors/{id}/deactivate` → Deactivate doctor

---

### 🧑 Patients

* POST `/patients/` → Create patient
* GET `/patients/` → Get all patients
* PUT `/patients/{id}` → Update patient
* DELETE `/patients/{id}` → Delete patient

---

### 📅 Appointments

* POST `/appointments/` → Create appointment
* GET `/appointments/` → Get all appointments
* GET `/appointments/doctor/{id}` → Get by doctor
* GET `/appointments/patient/{id}` → Get by patient
* PATCH `/appointments/{id}/cancel` → Cancel appointment
* PATCH `/appointments/{id}/complete` → Mark as completed

---

## 🧠 Business Logic

* ❌ Cannot create appointment with inactive doctor
* ❌ Cannot delete doctor if appointments exist
* ✔ Only authenticated users can access protected APIs

---

## 📄 Example Request (Create Appointment)

```json
{
  "doctor_id": 1,
  "patient_id": 1,
  "appointment_date": "2026-04-25T10:00:00"
}
```

---

## 📸 Screenshots

*Add Swagger UI screenshots here*

---

## 📬 Postman Collection

*Add your exported Postman collection JSON file*

---

## 👨‍💻 Author

Manikandan S

---

## 📝 Notes

This project is built for learning and demonstration of backend development using FastAPI with best practices like modular structure, authentication, and validation.
