import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import notesIcon from '../assets/icon-notes.svg'
import qaIcon from '../assets/icon-qa.svg'
import calendarIcon from '../assets/icon-calendar.svg'
import studyPlanIcon from '../assets/icon-studyplan.svg'
import quizIcon from '../assets/icon-quiz.svg'
import DashboardSections from '../components/dashboard/DashboardSections'
import { useAuth } from '../components/AuthContext'

const items = [['notes', notesIcon, 'Notes'], ['qa', qaIcon, 'Q&A'], ['ask-ai', '✨', 'Ask AI'], ['calendar', calendarIcon, 'Calendar'], ['plan', studyPlanIcon, 'Study Plan'], ['quiz', quizIcon, 'Quiz']]

export default function Dashboard() {
  const [active, setActive] = useState('notes')
  const navigate = useNavigate()
  const { logOut } = useAuth()
  const logout = () => { logOut(); navigate('/') }
  return <div className="page-container dashboard-page"><section className="dashboard-intro"><span className="eyebrow">Study workspace</span><h1>Everything for your <em className="accent-word">next session.</em></h1><p>Turn notes into answers, deadlines, plans, and practice�all in one gentle place.</p></section><div className="dashboard-workspace"><aside className="dashboard-sidebar">{items.map(([id, icon, label]) => <button className={active === id ? 'sidebar-item active' : 'sidebar-item'} onClick={() => setActive(id)} key={id}><span className="sidebar-icon">{id === 'ask-ai' ? icon : <img src={icon} alt="" />}</span>{label}</button>)}<button className="sidebar-item sidebar-logout" onClick={logout}><span>?</span>Log Out</button></aside><main className="dashboard-content"><DashboardSections activeSection={active} /></main></div></div>
}


