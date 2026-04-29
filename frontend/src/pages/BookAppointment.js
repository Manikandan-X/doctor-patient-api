import React, { useEffect, useState } from "react";
import API from "../api/api";

function BookAppointment() {
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);

  const [doctorId, setDoctorId] = useState("");
  const [patientId, setPatientId] = useState("");
  const [date, setDate] = useState("");

  // ✅ NEW: state for live message (optional UI display)
  const [liveMessage, setLiveMessage] = useState("");

  useEffect(() => {
  // ✅ fetch doctors
  API.get("/doctors/")
    .then((res) => setDoctors(res.data))
    .catch((err) => console.log("Doctor error:", err));

  // ✅ fetch patients
  API.get("/patients/")
    .then((res) => setPatients(res.data))
    .catch((err) => console.log("Patient error:", err));

  // ✅ prevent duplicate websocket
  if (window.ws) return;

  const doctorId = 1;

  const ws = new WebSocket(`ws://localhost:8000/ws/${doctorId}`);
  window.ws = ws;

  ws.onopen = () => {
    console.log(`Connected to doctor ${doctorId}`);
  };

  ws.onmessage = (event) => {
    console.log("Live Update:", event.data);
    setLiveMessage(event.data);
  };

  ws.onerror = (err) => {
    console.log("WebSocket error:", err);
  };

  ws.onclose = () => {
    console.log("WebSocket closed");
    window.ws = null;
  };

}, []);

  const book = async () => {
    try {
      if (!doctorId || !patientId || !date) {
        alert("Please select all fields");
        return;
      }

      await API.post("/appointments/", {
        doctor_id: doctorId,
        patient_id: patientId,
        appointment_date: date,
      });

      alert("Appointment booked");
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert("Error booking appointment");
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Book Appointment</h2>

        {/* ✅ LIVE MESSAGE UI */}
        {liveMessage && (
          <div style={styles.liveBox}>
            🔔 {liveMessage}
          </div>
        )}

        {/* Doctor */}
        <label style={styles.label}>Select Doctor</label>
        <select style={styles.input} onChange={(e) => setDoctorId(e.target.value)}>
          <option value="">Select Doctor</option>
          {doctors?.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>

        {/* Patient */}
        <label style={styles.label}>Select Patient</label>
        <select style={styles.input} onChange={(e) => setPatientId(e.target.value)}>
          <option value="">Select Patient</option>
          {patients?.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>

        {/* Date */}
        <label style={styles.label}>Appointment Date</label>
        <input
          style={styles.input}
          type="date"
          onChange={(e) => setDate(e.target.value)}
        />

        {/* Button */}
        <button style={styles.button} onClick={book}>
          Book Appointment
        </button>
      </div>
    </div>
  );
}

export default BookAppointment;

const styles = {
  page: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "40px",
    backgroundColor: "#f4f6f8",
    minHeight: "70vh",
  },
  card: {
    width: "350px",
    backgroundColor: "#ffffff",
    padding: "25px",
    borderRadius: "10px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    gap: "12px",
  },
  title: {
    textAlign: "center",
    marginBottom: "10px",
  },
  label: {
    fontSize: "14px",
    fontWeight: "bold",
  },
  input: {
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    fontSize: "14px",
  },
  button: {
    marginTop: "10px",
    padding: "10px",
    borderRadius: "5px",
    border: "none",
    backgroundColor: "#2c3e50",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
  },

  // ✅ NEW STYLE
  liveBox: {
    backgroundColor: "#e8f8f5",
    border: "1px solid #1abc9c",
    padding: "10px",
    borderRadius: "5px",
    fontSize: "14px",
  },
};