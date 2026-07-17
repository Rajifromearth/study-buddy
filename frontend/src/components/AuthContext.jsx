import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(() => Boolean(localStorage.getItem('study_buddy_token')))
  const logIn = token => { localStorage.setItem('study_buddy_token', token); setIsLoggedIn(true) }
  const logOut = () => { localStorage.removeItem('study_buddy_token'); setIsLoggedIn(false) }
  return <AuthContext.Provider value={{ isLoggedIn, logIn, logOut }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const auth = useContext(AuthContext)
  if (!auth) throw new Error('useAuth must be used within AuthProvider.')
  return auth
}
