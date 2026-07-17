import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Services from './pages/Services'
import Dashboard from './pages/Dashboard'
import About from './pages/About'
import Login from './pages/Login'
import Signup from './pages/Signup'
import ProtectedRoute from './components/ProtectedRoute'
import { AuthProvider } from './components/AuthContext'

function App() {
  return <BrowserRouter><AuthProvider><div className="app-shell"><Navbar /><main className="site-main"><Routes><Route path="/" element={<Home />} /><Route path="/services" element={<Services />} /><Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} /><Route path="/about" element={<About />} /><Route path="/login" element={<Login />} /><Route path="/signup" element={<Signup />} /></Routes></main></div></AuthProvider></BrowserRouter>
}
export default App


