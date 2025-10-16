import { useState } from "react";
import api from "../api";
import { ToastContainer, toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "react-toastify/dist/ReactToastify.css";
import './Logincss.css'

export default function Login() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Backend expects phone_number and password
      const res = await api.post("/api/token/", {
        phone_number: phoneNumber,
        password: password,
      });

      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
          toast.success("Login successful!", {
          onClose: () => navigate("/"), // Navigate only after toast closes
        });
        
        
      } else {
        toast.error("Invalid credentials");
      }
    } catch (error) {
      toast.error("Login failed. Please check your credentials.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <ToastContainer position="top-center" autoClose={2000} />
      <form onSubmit={handleLogin}>
        <label htmlFor="phone">Phone Number</label>
        <input
          type="tel"
          name="phone"
          placeholder="Enter phone number"
          pattern="[0-9]{10}"
          maxLength="10"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />

        <label htmlFor="password">Password</label>
        <input
          type="password"
          name="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
        <p>Don't have an account <Link to="/register" className="linkspan">Register</Link></p>
      </form>
    </div>
  );
}
