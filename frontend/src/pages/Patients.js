import React, { useEffect, useState } from "react";
import API from "../api/api";

function Patients() {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    API.get("/patients")
      .then((res) => setPatients(res.data))
      .catch(() => alert("Error fetching patients"));
  }, []);

  return (
    <div style={styles.page}>
      <h2 style={styles.title}>Patients</h2>

      <div style={styles.list}>
        {patients.map((p) => (
          <div key={p.id} style={styles.card}>
            <h3 style={styles.name}>{p.name}</h3>
            <p style={styles.phone}>📞 {p.phone}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Patients;

const styles = {
  page: {
    padding: "20px",
  },
  title: {
    marginBottom: "20px",
  },
  list: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
    gap: "15px",
  },
  card: {
    padding: "15px",
    borderRadius: "10px",
    backgroundColor: "#ffffff",
    boxShadow: "0 3px 8px rgba(0,0,0,0.1)",
  },
  name: {
    margin: 0,
  },
  phone: {
    marginTop: "5px",
    color: "#555",
  },
};