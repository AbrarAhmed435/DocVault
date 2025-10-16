import { useState } from 'react'
import { BrowserRouter,Route,Routes,Navigate } from 'react-router-dom'
import Login from './pages/Login'
import ProtectedRoute from './ProtectedRoutes'
import Home from './Home'
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Register from './pages/Register'

function Logout(){
  localStorage.clear();
  return <Navigate to ="/login" />
}

function App() {
  

  return (
    <>
    
    <BrowserRouter>
    <ToastContainer position="top-center" autoClose={3000} />
    <Routes>
      <Route path="/" element={<ProtectedRoute><Home/></ProtectedRoute>}/>
      <Route path='/login' element={<Login/>}/>
      <Route path='/register' element={< Register/>} />
      <Route path='/logout' element={<Logout/>} />
    </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
