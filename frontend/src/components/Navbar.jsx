import { useEffect, useState } from 'react'
import { Menu, X } from 'lucide-react'
import { NavLink, useNavigate } from 'react-router-dom'
import logo from '../assets/logo.svg'
import { useAuth } from './AuthContext'

function Navbar(){
  const { isLoggedIn, logOut } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()
  useEffect(() => {
    if (!menuOpen) return
    const onKeyDown = event => { if (event.key === 'Escape') setMenuOpen(false) }
    document.body.classList.add('mobile-menu-open')
    window.addEventListener('keydown', onKeyDown)
    return () => {
      document.body.classList.remove('mobile-menu-open')
      window.removeEventListener('keydown', onKeyDown)
    }
  }, [menuOpen])
  const closeMenu = () => setMenuOpen(false)
  const logout = () => { logOut(); closeMenu(); navigate('/') }
  const links = <><NavLink to="/" onClick={closeMenu}>Home</NavLink><NavLink to="/services" onClick={closeMenu}>Services</NavLink>{isLoggedIn && <NavLink to="/dashboard" onClick={closeMenu}>Dashboard</NavLink>}<NavLink to="/about" onClick={closeMenu}>About</NavLink></>
  return <header className="site-header"><nav className="navbar" aria-label="Main navigation"><NavLink className="brand" to="/"><img src={logo} alt="Study Buddy" /></NavLink><div className="nav-links">{links}</div><div className="nav-auth">{isLoggedIn ? <button className="nav-login nav-logout" onClick={logout}>Log Out</button> : <><NavLink className="nav-login" to="/login">Log In</NavLink><NavLink className="nav-cta" to="/signup">Sign Up <span>?</span></NavLink></>}</div><button className="mobile-menu-toggle" type="button" aria-label="Open menu" aria-expanded={menuOpen} onClick={()=>setMenuOpen(true)}><Menu size={21}/></button></nav>{menuOpen&&<><button className="mobile-drawer-backdrop" type="button" aria-label="Close menu" onClick={closeMenu}/><aside className="mobile-drawer" role="dialog" aria-modal="true" aria-label="Mobile navigation"><button className="mobile-menu-close" type="button" aria-label="Close menu" onClick={closeMenu}><X size={22}/></button><div className="mobile-drawer-links">{links}</div><div className="mobile-drawer-auth">{isLoggedIn ? <button className="mobile-logout" onClick={logout}>Log Out</button> : <><NavLink to="/login" onClick={closeMenu}>Log In</NavLink><NavLink className="mobile-signup" to="/signup" onClick={closeMenu}>Sign Up</NavLink></>}</div></aside></>}</header>
}
export default Navbar
