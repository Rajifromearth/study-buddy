import { useEffect, useState } from 'react'
import { BookOpen } from 'lucide-react'
import notesIcon from '../../assets/icon-notes.svg'
import calendarIcon from '../../assets/icon-calendar.svg'

const base = import.meta.env.VITE_API_URL
const startOfToday = () => { const today = new Date(); today.setHours(0, 0, 0, 0); return today }
const eventDate = value => {
  if (!value) return null
  const parsed = /^\d{4}-\d{2}-\d{2}$/.test(value) ? new Date(`${value}T00:00:00`) : new Date(value)
  return Number.isNaN(parsed.getTime()) ? null : parsed
}

export default function DashboardStats({ refreshKey }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [unavailable, setUnavailable] = useState(false)

  useEffect(() => {
    let cancelled = false
    const load = async () => {
      setLoading(true)
      setUnavailable(false)
      try {
        const [notesResponse, eventsResponse] = await Promise.all([fetch(`${base}/notes`), fetch(`${base}/calendar/events`)])
        if (!notesResponse.ok || !eventsResponse.ok) throw new Error('Unable to load dashboard stats')
        const [notes, events] = await Promise.all([notesResponse.json(), eventsResponse.json()])
        if (!Array.isArray(notes) || !Array.isArray(events)) throw new Error('Invalid dashboard stats response')
        const today = startOfToday()
        const nextEvent = events.map(event => ({ ...event, parsedDate: eventDate(event.date) })).filter(event => event.parsedDate && event.parsedDate >= today).sort((a, b) => a.parsedDate - b.parsedDate)[0]
        const daysAway = nextEvent ? Math.round((nextEvent.parsedDate - today) / 86400000) : null
        if (!cancelled) setStats({ notes: notes.length, courses: new Set(notes.map(note => note.course).filter(Boolean)).size, nextEvent, daysAway })
      } catch {
        if (!cancelled) setUnavailable(true)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [refreshKey])

  if (loading && !stats) return <section className="dashboard-stats dashboard-stats--loading" aria-label="Loading workspace stats"><article className="dashboard-stat-card dashboard-stat-card--skeleton"/><article className="dashboard-stat-card dashboard-stat-card--skeleton"/><article className="dashboard-stat-card dashboard-stat-card--skeleton"/></section>
  if (!stats && unavailable) return <section className="dashboard-stats dashboard-stats--unavailable" aria-live="polite">Workspace stats are unavailable right now.</section>

  const deadline = stats.nextEvent ? `Next: ${stats.nextEvent.title} in ${stats.daysAway} ${stats.daysAway === 1 ? 'day' : 'days'}` : 'No upcoming deadlines'
  return <section className="dashboard-stats" aria-label="Workspace overview">
    <article className="dashboard-stat-card"><span className="dashboard-stat-icon"><img src={notesIcon} alt="" /></span><div><strong>{stats.notes}</strong><span>Total notes uploaded</span></div></article>
    <article className="dashboard-stat-card dashboard-stat-card--coral"><span className="dashboard-stat-icon"><BookOpen size={19} aria-hidden="true" /></span><div><strong>{stats.courses}</strong><span>Courses</span></div></article>
    <article className="dashboard-stat-card"><span className="dashboard-stat-icon"><img src={calendarIcon} alt="" /></span><div><strong className="dashboard-stat-deadline">{deadline}</strong><span>Upcoming deadline</span></div></article>
  </section>
}
