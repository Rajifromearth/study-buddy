import { createContext, useCallback, useContext, useState } from 'react'

const AuthContext = createContext(null)

const storedUser = () => {
  try {
    return JSON.parse(localStorage.getItem('study_buddy_user') || 'null')
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(() => Boolean(localStorage.getItem('study_buddy_token')))
  const [user, setUser] = useState(storedUser)
  const logIn = useCallback((token, nextUser) => {
    localStorage.setItem('study_buddy_token', token)
    if (nextUser) localStorage.setItem('study_buddy_user', JSON.stringify(nextUser))
    setUser(nextUser || null)
    setIsLoggedIn(true)
  }, [])
  const updateUser = useCallback(nextUser => {
    localStorage.setItem('study_buddy_user', JSON.stringify(nextUser))
    setUser(nextUser)
  }, [])
  const logOut = useCallback(() => {
    localStorage.removeItem('study_buddy_token')
    localStorage.removeItem('study_buddy_user')
    setUser(null)
    setIsLoggedIn(false)
  }, [])
  return <AuthContext.Provider value={{ isLoggedIn, user, logIn, logOut, updateUser }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const auth = useContext(AuthContext)
  if (!auth) throw new Error('useAuth must be used within AuthProvider.')
  return auth
}