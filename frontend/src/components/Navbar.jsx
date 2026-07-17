import { NavLink, useNavigate } from 'react-router-dom'
import logo from '../assets/logo.svg'
import { useAuth } from './AuthContext'

function Navbar(){
  const { isLoggedIn, logOut } = useAuth()
  const navigate = useNavigate()
  const logout = () => { logOut(); navigate('/') }
  return <header className="site-header"><nav className="navbar" aria-label="Main navigation"><NavLink className="brand" to="/"><img src={logo} alt="Study Buddy" /></NavLink><div className="nav-links"><NavLink to="/">Home</NavLink><NavLink to="/services">Services</NavLink>{isLoggedIn && <NavLink to="/dashboard">Dashboard</NavLink>}<NavLink to="/about">About</NavLink></div><div className="nav-auth">{isLoggedIn ? <button className="nav-login nav-logout" onClick={logout}>Log Out</button> : <><NavLink className="nav-login" to="/login">Log In</NavLink><NavLink className="nav-cta" to="/signup">Sign Up <span>?</span></NavLink></>}</div></nav></header>
}
export default Navbar
