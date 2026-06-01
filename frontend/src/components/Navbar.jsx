// src/components/Navbar.jsx
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import './Navbar.css';

export default function Navbar({ theme, toggleTheme }) {
  const location = useLocation();

  const navLinks = [
    { to: '/', label: 'Home', icon: '🏠' },
    { to: '/input', label: 'Solve', icon: '🧩' },
    { to: '/patterns', label: 'Patterns', icon: '🏁' },
    { to: '/history', label: 'History', icon: '📊' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand">
          <span className="navbar-logo">🧊</span>
          <span className="navbar-title">Rubik's Solver</span>
        </Link>

        <div className="navbar-links">
          {navLinks.map(link => (
            <Link
              key={link.to}
              to={link.to}
              className={`nav-link ${location.pathname === link.to ? 'active' : ''}`}
            >
              <span className="nav-icon">{link.icon}</span>
              <span className="nav-label">{link.label}</span>
            </Link>
          ))}
        </div>

        <div className="navbar-actions">
          <ThemeToggle theme={theme} onToggle={toggleTheme} />
        </div>
      </div>
    </nav>
  );
}
