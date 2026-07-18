import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { LogOut, Sparkles } from 'lucide-react'
import notesIcon from '../assets/icon-notes.svg'
import qaIcon from '../assets/icon-qa.svg'
import calendarIcon from '../assets/icon-calendar.svg'
import studyPlanIcon from '../assets/icon-studyplan.svg'
import quizIcon from '../assets/icon-quiz.svg'
import DashboardSections from '../components/dashboard/DashboardSections'
import { useAuth } from '../components/AuthContext'

const API_URL = import.meta.env.VITE_API_URL
const items = [['notes', notesIcon, 'Notes'], ['qa', qaIcon, 'Q&A'], ['ask-ai', Sparkles, 'Ask AI'], ['calendar', calendarIcon, 'Calendar'], ['plan', studyPlanIcon, 'Study Plan'], ['quiz', quizIcon, 'Quiz']]

export default function Dashboard() {
  const [active, setActive] = useState('notes')
  const [course, setCourse] = useState('')
  const navigate = useNavigate()
  const { logOut, updateUser, user } = useAuth()
  useEffect(() => {
    if (user) return
    const token = localStorage.getItem('study_buddy_token')
    if (!token) return
    fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then(response => response.ok ? response.json() : null)
      .then(profile => { if (profile) updateUser(profile) })
      .catch(() => {})
  }, [updateUser, user])
  const logout = () => { logOut(); navigate('/') }
  return <div className="page-container dashboard-page"><section className="dashboard-intro">{user?.username&&<p className="dashboard-welcome">Welcome back, {user.username}!</p>}<span className="eyebrow">Study workspace</span><h1>Everything for your <em className="accent-word">next session.</em></h1><p>Turn notes into answers, deadlines, plans, and practice - all in one gentle place.</p></section><div className="dashboard-workspace"><aside className="dashboard-sidebar">{items.map(([id, icon, label]) => <button className={active === id ? 'sidebar-item active' : 'sidebar-item'} onClick={() => setActive(id)} key={id}><span className="sidebar-icon">{id === 'ask-ai' ? <Sparkles size={18} aria-hidden="true" /> : <img src={icon} alt="" />}</span>{label}</button>)}<button className="sidebar-item sidebar-logout" onClick={logout}><LogOut size={18} aria-hidden="true" />Log Out</button></aside><main className="dashboard-content"><DashboardSections activeSection={active} course={course} setCourse={setCourse} /></main></div></div>
}