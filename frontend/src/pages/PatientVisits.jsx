import { useState, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import api from "../api";
import { IoAddSharp } from "react-icons/io5";
import './Patient_Visits.css'

export default function PatientVisits() {
  const { id } = useParams();
  const location = useLocation();
  const [patient, setPatients] = useState(location.state?.patient || null);
  const [visits, setVisits] = useState([]);
  const [loading, setLoading] = useState(false);
  const [diagnosis, setDiagnosis] = useState("");
  const [treatment, setTreatment] = useState("");
  const [test, setTest] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [askAi, setAskAi] = useState(false);
  const [aires, setAiRes] = useState("");

  const fetchVisits = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/api/patients/${id}/visits/`);
      if (res.status === 200) {
        setVisits(res.data);
      }
    } catch (error) {
      toast.error("Failed to fetch Visits");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchVisits();
  }, [id]);

  const handleAddVisit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post(`/api/patients/${id}/visits/`, {
        diagnosis,
        treatment,
        test,
      });
      if (res.status === 201) {
        toast.success("Visit Added");
      }
    } catch (error) {
      toast.error("Visit was not Added");
    }
    fetchVisits();
    setAiRes("");
    setAskAi(false);
  };
  const handleAskAiClick = () => {
  if (!visits.length) {
    toast.info("Patient has no visits yet");
    return;
  }

  setAskAi(!askAi);
  handleAskAi(visits);
};
  const handleAskAi = async (visits) => {
    
    // console.log(visits)
    if(askAi) return ;
    if(aires) return ;
    try {
      const res = await api.post("/api/askai/", { content: visits });
      if(res.status==200){
      setAiRes(res.data.summary);
      }
      // if(res.status===204){
      // console.log(res.data.warning)
      // toast.info("Patient doesn't have any visits yet.");
      // setAskAi(false);
      // }
      console.log(aires);
    } catch (error) {
      console.log(error)
    }
  };

  return (
    <div className="patient-visits-page">
      <h2>
        Visits of {patient?.gender === "M" ? "Mr." : "Mrs."}
        {patient?.name}
      </h2>
      <p onClick={() => setShowForm(!showForm)} style={{ cursor: "pointer" }}>
        Add Visit{" "}
        <IoAddSharp
          style={{
            transform: showForm ? "rotate(45deg)" : "rotate(0deg)",
            verticalAlign: "middle",
            transition: "transform 0.3s",
          }}
        />
      </p>
      {showForm && (
        <form onSubmit={handleAddVisit} className="visit_form">
          <input
            type="text"
            placeholder="Diagonosis"
            value={diagnosis}
            onChange={(e) => setDiagnosis(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Treatment"
            value={treatment}
            onChange={(e) => setTreatment(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Any tests"
            value={test}
            onChange={(e) => setTest(e.target.value)}
          />

          <button>Add</button>
        </form>
      )}
      <ToastContainer position="top-center" autoClose={2000} />
      <div>
        <p onClick={() => handleAskAiClick(visits)}><button className="Ask-ai-button">As Ai</button></p>
        {askAi && <div>{!aires ? <p>Loading...</p> : <p>{aires}</p>}</div>}
      </div>
      {loading ? (
        <p>Loading visits...</p>
      ) : visits.length === 0 ? (
        <p>No visits found</p>
      ) : (
        <ul>
          {visits.map((v) => (
            <li key={v.id}>
              <p>Visit No: {v.visit_no}</p>
              <p>Diagnosis: {v.diagnosis}</p>
              <p>Treatment: {v.treatment}</p>
              {v.test && <p>Test: {v.test}</p>}
              <p>Date: {new Date(v.date_created).toLocaleString()}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
