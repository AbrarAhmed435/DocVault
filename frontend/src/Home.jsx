import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import api from "./api";

export default function Home() {
  const [name, setName] = useState("");
  const [age, setAge] = useState();
  const [gender, setGender] = useState("");
  const [weight_kg, setWeight] = useState();
  const [height_cm, setHeight] = useState();

  const handleAdding= async (e)=>{
    e.preventDefault();

    try{
        const res=await api.post("/api/addpatients/",{
          name,
          age,
          gender,
          weight_kg,
          height_cm
        });
        if(res.status===201){
            toast.success("Patient Added Successfully",{style:{color: "white"},});
        }
    }catch(error){
        console.log(error);
    }
  }


  return (
    <div className="home">
         <ToastContainer position="top-center" autoClose={2000} />
        <div className="welcome"><span>Welcome </span> </div>
      <div className="Add-patient">
        <form onSubmit={handleAdding}>
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
          <input type="number"
          placeholder="Weight(kg)"
          step="0.1"
          value={weight_kg}
          onChange={(e)=>setWeight(e.target.value)}
          required
          />
          <input type="number" 
          step="0.1"
          placeholder="Enter Height(cm)"
          value={height_cm}
          onChange={(e)=>setHeight(e.target.value)}
          required
          />
          <button>Submit</button>
        </form>
      </div>
    </div>
  );
}

/* 
POST http://127.0.0.1:8000/api/addpatients/ HTTP/1.1
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYwNDY3OTU4LCJpYXQiOjE3NjA0NjQzNTgsImp0aSI6IjU3YjlkZGE0NTNmYTQ0OWM5ZDlmMWJlNzdiMGUwMDNkIiwidXNlcl9pZCI6N30.ZDE8-oqj5f1HAiihyYHpOCtaF7oSGJ8CUN4YSZHgtxk

{
  "name":"Tawheed",
  "age":"20",
  "gender":"M",
  "weight_kg":"100",
  "height_cm":"175"
}
*/
