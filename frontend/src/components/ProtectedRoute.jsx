import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }) {
  return localStorage.getItem('study_buddy_token') ? children : <Navigate to="/login" replace />
}
