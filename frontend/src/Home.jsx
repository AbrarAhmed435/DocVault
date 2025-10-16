import { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { IoAddSharp } from "react-icons/io5";
import api from "./api";
import { FIRST_NAME } from "./constants";

export default function Home() {
  const [name, setName] = useState("");
  const [age, setAge] = useState();
  const [gender, setGender] = useState("");
  const [weight_kg, setWeight] = useState();
  const [height_cm, setHeight] = useState();
  const [firstName, setFirstName] = useState("");
  const [showForm, setShowForm] = useState(false); // 👈 new state to toggle
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fn = localStorage.getItem(FIRST_NAME) || "";
    setFirstName(fn);
  }, []);

  const fetchPatients = async () => {
    try {
      const res = await api.get("/api/addpatients/");
      if (res.status === 200) {
        setPatients(res.data);
      }
    } catch (error) {
      toast.error("Failed to fetch Patients");
    }
  };
  useEffect(() => {
    fetchPatients();
  }, []);

  const handleAdding = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/api/addpatients/", {
        name,
        age,
        gender,
        weight_kg,
        height_cm,
      });
      if (res.status === 201) {
        toast.success("Patient Added Successfully", {
          style: { color: "white" },
        });
        setName("");
        setAge("");
        setGender("");
        setWeight("");
        setHeight("");
        setShowForm(false); // hide form after submission
      }
    } catch (error) {
      console.log(error);
    }
    fetchPatients();
  };

  return (
    <div className="home">
      <ToastContainer position="top-center" autoClose={2000} />
      <div className="welcome">
        <span>Welcome Dr. {firstName}</span>
      </div>

      <div className="Add-patient">
        <h4
          className="add-title"
          onClick={() => setShowForm(!showForm)}
          style={{ cursor: "pointer" }}
        >
          Add Patient{" "}
          <IoAddSharp
            style={{
              verticalAlign: "middle",
              transform: showForm ? "rotate(45deg)" : "rotate(0deg)", // rotate icon when open
              transition: "transform 0.3s",
            }}
          />
        </h4>

        {showForm && (
          <form onSubmit={handleAdding} className="patient-form">
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Enter Age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              required
            />
            <select
              name="gender"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              required
            >
              <option value="">-- Select Gender --</option>
              <option value="M">Male</option>
              <option value="F">Female</option>
              <option value="O">Other</option>
            </select>
            <input
              type="number"
              placeholder="Weight (kg)"
              step="0.1"
              value={weight_kg}
              onChange={(e) => setWeight(e.target.value)}
              required
            />
            <input
              type="number"
              step="0.1"
              placeholder="Enter Height (cm)"
              value={height_cm}
              onChange={(e) => setHeight(e.target.value)}
              required
            />
            <button>Submit</button>
          </form>
        )}
      </div>
      <div className="patient_list">
        <h3>My Patients</h3>
        {patients.length === 0 ? (
          <p className="no-patient">No Patients found</p>
        ) : (
          <ul>
            {patients.map((p) => (
              // <li key={p.id}>{p.name}{" "}{p.gender=='M'?"Male":"Female"}</li>
              <li key={p.id}>
                <p className="name">{p.name}</p>
                <br />
                <p>
                  {p.gender === "M"
                    ? "Male"
                    : p.gender === "F"
                    ? "Female"
                    : "Other"}
                    {":"}{p.age}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
