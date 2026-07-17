import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import AuthLayout from '../components/AuthLayout'
import { useAuth } from '../components/AuthContext'

const API_URL = 'http://127.0.0.1:8000'
export default function Login() { const [email,setEmail]=useState(''),[password,setPassword]=useState(''),[error,setError]=useState(''),[loading,setLoading]=useState(false),navigate=useNavigate(),{ logIn }=useAuth(); const submit=async e=>{e.preventDefault();if(!email||!password)return setError('Enter your email and password.');try{setLoading(true);setError('');const response=await fetch(`${API_URL}/auth/login`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});const data=await response.json();if(!response.ok)throw Error(response.status===401?'Invalid email or password.':data.detail||'Unable to log in.');logIn(data.token);navigate('/dashboard')}catch(err){setError(err.message)}finally{setLoading(false)}};return localStorage.getItem('study_buddy_token') ? <Navigate to="/dashboard" replace /> : <AuthLayout title="Welcome back" subtitle="Pick up right where you left off." footer={<>Don�t have an account? <Link to="/signup">Sign up</Link></>}><form className="auth-form" onSubmit={submit}><label>Email<input type="email" value={email} onChange={e=>setEmail(e.target.value)} autoComplete="email" /></label><label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} autoComplete="current-password" /></label>{error&&<p className="auth-error" role="alert">{error}</p>}<button className="button button--accent" disabled={loading}>{loading?'Logging in�':'Log In'}</button></form></AuthLayout>}



