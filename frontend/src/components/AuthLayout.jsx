import { Link } from 'react-router-dom'
import illustration from '../assets/auth-illustration.svg'

export default function AuthLayout({ title, subtitle, children, footer }) {
  return <div className="auth-layout"><aside className="auth-visual"><img src={illustration} alt="Study notes and planning cards" /><div><span className="eyebrow">Study Buddy</span><h1>Make space for <em>better learning.</em></h1><p>One calm place for your notes, plans, and progress.</p></div></aside><section className="auth-panel"><Link className="auth-brand" to="/">Study Buddy</Link><div className="auth-card"><h2>{title}</h2><p>{subtitle}</p>{children}{footer && <p className="auth-footer">{footer}</p>}</div></section></div>
}
