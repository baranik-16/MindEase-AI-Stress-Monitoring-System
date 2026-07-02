import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

const API_BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    const u = username.trim();
    const p = password.trim();
    if (!u || !p) {
      alert("Username and password are required");
      return;
    }

    try {
      const res = await axios.post(`${API_BASE}/login`, { username: u, password: p }, {
        headers: { "Content-Type": "application/json" }
      });

      if (res.data?.status === "success") {
        localStorage.setItem("username", res.data.username);
        navigate("/dashboard");
      } else {
        alert(res.data?.message || "Login failed.");
      }
    } catch (err) {
      console.error("Login error:", err?.response || err?.message || err);
      const msg = err?.response?.data?.message || "Login failed. Try again.";
      alert(msg);
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Enter Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
      <p style={{ textAlign: "center" }}>
        Don't have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}

export default Login;
