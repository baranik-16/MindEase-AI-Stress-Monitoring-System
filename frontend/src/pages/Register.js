import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

// ✅ Fallback to 127.0.0.1 if env isn’t loaded
const API_BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    const u = username.trim();
    const p = password.trim();
    if (!u || !p) {
      alert("Username and password are required");
      return;
    }

    try {
      const res = await axios.post(`${API_BASE}/register`, { username: u, password: p }, {
        headers: { "Content-Type": "application/json" }
      });

      if (res.data?.status === "success") {
        alert("Registration successful!");
        navigate("/");
      } else {
        alert(res.data?.message || "Registration failed.");
      }
    } catch (err) {
      console.error("Register error:", err?.response || err?.message || err);
      const msg = err?.response?.data?.message || "Registration failed.";
      alert(msg);
    }
  };

  return (
    <div className="container">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Create Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Create Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
      <p style={{ textAlign: "center" }}>
        Already have an account? <Link to="/">Login</Link>
      </p>
    </div>
  );
}

export default Register;
