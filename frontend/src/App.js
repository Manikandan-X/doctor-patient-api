import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Login from "./pages/Login";
import Doctors from "./pages/Doctors";
import Patients from "./pages/Patients";
import BookAppointment from "./pages/BookAppointment";

function App() {
  return (
    <BrowserRouter>
      {/* 🔝 Navbar */}
      <div style={styles.navbar}>
        <h2 style={styles.logo}>Doctor App</h2>

        <div style={styles.navLinks}>
          <Link to="/doctors" style={styles.link}>Doctors</Link>
          <Link to="/patients" style={styles.link}>Patients</Link>
          <Link to="/book" style={styles.link}>Book</Link>
        </div>
      </div>

      {/* 📦 Page Container */}
      <div style={styles.container}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/doctors" element={<Doctors />} />
          <Route path="/patients" element={<Patients />} />
          <Route path="/book" element={<BookAppointment />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 30px",
    backgroundColor: "#2c3e50",
    color: "white",
  },
  logo: {
    margin: 0,
  },
  navLinks: {
    display: "flex",
    gap: "20px",
  },
  link: {
    color: "white",
    textDecoration: "none",
    fontWeight: "bold",
  },
  container: {
    padding: "30px",
  },
};