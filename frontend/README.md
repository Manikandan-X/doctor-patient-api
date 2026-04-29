# 🖥 Frontend - Doctor Appointment System (React)

This is the frontend application for the Doctor Appointment System, built using React and integrated with a FastAPI backend.

---

## 🚀 Features

* 🔐 Login with JWT authentication
* 👨‍⚕️ View list of doctors
* 🧑 View list of patients
* 📅 Book appointments
* 🔄 Real-time updates using WebSockets
* 🔒 Protected routes (requires login)

---

## 🛠 Tech Stack

* React
* Axios
* React Router

---

## ⚙️ Setup Instructions

### 1️⃣ Go to frontend folder

```bash
cd frontend
```

---

### 2️⃣ Install dependencies

```bash
npm install
```

---

### 3️⃣ Run the application

```bash
npm start
```

---

## 🌐 Application URL

```
http://localhost:3000
```

---

## 🔗 Backend Requirement

Make sure backend is running at:

```
http://127.0.0.1:8000
```

---

## ⚡ WebSocket Connection

```
ws://127.0.0.1:8000/ws/{doctor_id}
```

Used for:

* New appointment notifications
* Appointment status updates

---

## 🧠 How It Works

* User logs in → token stored in localStorage
* Token sent with every API request
* Backend validates user
* WebSocket connects using doctor ID for live updates

---

## ⚠️ Important Notes

* Backend must be running before starting frontend
* If you get `401 Unauthorized`, login again
* Do not open protected routes directly without login

---

## 👨‍💻 Author

Manikandan S
