# 🏥 Doctor Appointment System (Full-Stack Application)

A complete full-stack application built using **FastAPI (Backend)** and **React (Frontend)** to manage doctors, patients, and appointments with real-time updates and secure authentication.

---

## 🚀 Features

### 🔐 Authentication

* JWT-based Register & Login
* Secure protected APIs using Bearer token

### 👨‍⚕️ Doctor Management

* Create, update, delete doctors
* Activate / deactivate doctors
* Filter by specialization
* Pagination support

### 🧑 Patient Management

* Full CRUD operations
* List all patients

### 📅 Appointment System

* Book appointments
* View by doctor / patient
* Status updates:

  * Scheduled
  * Completed
  * Cancelled

---

## ⚡ Real-Time Features (WebSockets)

* 🔔 Notify doctor when a new appointment is booked
* 🔄 Live appointment status updates (Cancel / Complete)
* User-specific WebSocket connection

```
ws://127.0.0.1:8000/ws/{doctor_id}
```

---

## 📂 File Upload Module

* Upload patient reports/documents
* Files stored locally (`/uploads`)
* View/download files via API

---

## 🧠 Advanced Backend Features

* 📄 Pagination (`skip`, `limit`)
* 🔎 Search & filtering (doctor specialization)
* 🚦 API rate limiting (basic)
* ⚙️ Background tasks (FastAPI BackgroundTasks)
* 📝 Logging for API requests & errors
* ⚡ Caching (optional – not implemented)

---

## 🧪 Testing

* Basic unit tests using `pytest`
* Covered important APIs

```
python -m pytest -v
```

---

## 🖥 Frontend (React)

### Pages:

* Login page
* Doctors listing
* Patients listing
* Book Appointment UI

### Features:

* API integration with FastAPI
* JWT token handling
* Protected routes
* Real-time notifications (WebSocket)

---

## 🛠 Tech Stack

### Backend:

* FastAPI
* Python
* SQLAlchemy
* MySQL
* Pydantic
* JWT (python-jose)
* Passlib (bcrypt)

### Frontend:

* React
* Axios
* React Router

---

## 📂 Project Structure

```
app/
 ├── routers/
 │    ├── auth.py
 │    ├── doctor.py
 │    ├── patient.py
 │    ├── appointment.py
 │    ├── websocket.py
 │    ├── file.py
 │
 ├── models/
 ├── schemas/
 ├── services/
 ├── utils/
 ├── database.py
 ├── deps.py
 ├── main.py

frontend/
 ├── src/
 │    ├── pages/
 │    ├── api/
 │    ├── App.js
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/Manikandan-X/doctor-patient-api
cd doctor-patient-api
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

### 5️⃣ Run Backend

```
python -m uvicorn app.main:app --reload
```

👉 API Docs:

```
http://127.0.0.1:8000/docs
```

---

### 6️⃣ Run Frontend

```
cd frontend
npm install
npm start
```

👉 Frontend:

```
http://localhost:3000
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

Use token:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### 👨‍⚕️ Doctors

* POST `/doctors/`
* GET `/doctors/`
* PUT `/doctors/{id}`
* DELETE `/doctors/{id}`
* PATCH `/doctors/{id}/activate`
* PATCH `/doctors/{id}/deactivate`

---

### 🧑 Patients

* POST `/patients/`
* GET `/patients/`
* PUT `/patients/{id}`
* DELETE `/patients/{id}`

---

### 📅 Appointments

* POST `/appointments/`
* GET `/appointments/`
* GET `/appointments/doctor/{id}`
* GET `/appointments/patient/{id}`
* PATCH `/appointments/{id}/cancel`
* PATCH `/appointments/{id}/complete`

---

## 🧠 Business Logic

* ❌ Cannot book appointment with inactive doctor
* ❌ Cannot complete cancelled appointment
* ❌ Cannot cancel completed appointment
* ✔ Only authenticated users can access APIs

---

## 📄 Example Request (Create Appointment)

```json
{
  "doctor_id": 1,
  "patient_id": 1,
  "appointment_date": "2026-04-25"
}
```

---

## 📸 Screenshots

* Swagger UI
* React UI (Login, Doctors, Booking)

---

## 📬 Postman Collection

(Add your exported Postman collection JSON file here)

---

## 👨‍💻 Author

**Manikandan S**

---

## 📝 Notes

This project demonstrates:

* Full-stack development (FastAPI + React)
* REST API design
* Authentication & security (JWT)
* Real-time communication using WebSockets
* File handling (upload & download)
* Clean architecture and modular coding practices
