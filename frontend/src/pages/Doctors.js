import React, { useEffect, useState } from "react";
import API from "../api/api";

function Doctors() {
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    API.get("/doctors")
      .then((res) => setDoctors(res.data))
      .catch(() => alert("Error fetching doctors"));
  }, []);

  return (
    <div style={styles.page}>
      <h2 style={styles.title}>Doctors</h2>

      <div style={styles.list}>
        {doctors.map((doc) => (
          <div key={doc.id} style={styles.card}>
            <h3 style={styles.name}>{doc.name}</h3>
            <p style={styles.spec}>{doc.specialization}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Doctors;

const styles = {
  page: {
    padding: "20px",
  },
  title: {
    marginBottom: "20px",
  },
  list: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
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
  spec: {
    marginTop: "5px",
    color: "#555",
  },
};