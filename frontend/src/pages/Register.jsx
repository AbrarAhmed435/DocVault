/* 
{
  "first_name": "Dr. Johny",
  "last_name":"Sins",
  "username": "sins123",
  "phone_number": "1010101010",
  "employee_id":"pornhub001",
  "password": "dani435@",
  "confirm_password":"dani435@"
} */

import "./Register.css";
import { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import api from "../api";
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [phone_number, setPhoneNumber] = useState("");
  const [employee_id, setEmployeeId] = useState("");
  const [password, setPassword] = useState("");
  const [confirm_password, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);

const navigate = useNavigate();
  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    if(confirm_password!==password){
      toast.error("Passwords didn't match");
      return ;
    }
      
    try {

      const res = await api.post("/api/register/", {
        first_name,
        last_name,
        username,
        phone_number,
        employee_id,
        password,
        confirm_password,
      });

      if (res.status === 201) {
        setFirstName("");
        setLastName("");
        setConfirmPassword("");
        setPassword("");
        setEmployeeId("");
        setPhoneNumber("");
        setUsername("");
        toast.success("Register successful! Redirecting to Login Page....", {
          onClose: () => navigate("/login"), // Navigate only after toast closes
        });
      }
    } catch (error) {
      console.log(error)
       if (error.response && error.response.data) {
    const errors = error.response.data;

    // Loop through all error messages and show them in toasts
    Object.keys(errors).forEach((key) => {
      const message = errors[key];
      // Some errors are arrays, handle both string and array
      if (Array.isArray(message)) {
        message.forEach((m) => toast.error(`${key}: ${m}`));
      } else {
        toast.error(`${key}: ${message}`);
      }
    });
  } else {
    toast.error("Something went wrong. Please try again.");
  }
      
     
    }
  };

  return (
    <div className="Register-Container">
      <h2>DockVault</h2>
      <ToastContainer position="top-center" autoClose={2000} />
      <form onSubmit={handleRegister} className="Register-form">
        <label htmlFor="fist_name">First Name</label>
        <input
          type="text"
          placeholder="Enter First Name..."
          name="first_name"
          value={first_name}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
        <label htmlFor="last_name">Last Name</label>
        <input
          type="text"
          placeholder="Enter Last Name..."
          name="last_name"
          value={last_name}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        <label htmlFor="username">Username</label>
        <input
          type="text"
          placeholder="Set Username"
          name="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <label htmlFor="phone_number">Phone</label>
        <input
          type="tel"
          maxLength={10}
          pattern="[0-9]{10}"

          name="phone_number"
          placeholder="Enter Phone number (10)"
          value={phone_number}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />
       

        <label htmlFor="employee_id">Employee_id</label>
        <input
          type="text"
          placeholder="Enter Employee id"
          value={employee_id}
          name="employee_id"
          onChange={(e) => setEmployeeId(e.target.value)}
          required
        />
        <label htmlFor="password">Password</label>
        <input
          type="password"
          placeholder="Password..(min 8)"
          value={password}
          name="password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <label htmlFor="confirm_password">Confirm Password</label>
        <input
          type="password"
          placeholder="Confirm Password.."
          value={confirm_password}
          name="confirm_password"
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <button>Register  </button>
        <p>Already have an account  <Link to="/login" className="linkspan">Login</Link></p>
      </form>
      
    </div>
  );
}
