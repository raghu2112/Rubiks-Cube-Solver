// src/pages/LandingPage.jsx
import { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import TwistyPlayer from '../components/TwistyPlayer';
import './LandingPage.css';

export default function LandingPage({ size, onSizeChange }) {
  const particlesRef = useRef(null);

  useEffect(() => {
    // Create floating cube particles
    const container = particlesRef.current;
    if (!container) return;

    const emojis = ['🟥', '🟧', '🟨', '🟩', '🟦', '⬜'];
    const particles = [];

    for (let i = 0; i < 20; i++) {
      const el = document.createElement('span');
      el.className = 'floating-particle';
      el.textContent = emojis[i % emojis.length];
      el.style.left = `${Math.random() * 100}%`;
      el.style.top = `${Math.random() * 100}%`;
      el.style.animationDelay = `${Math.random() * 6}s`;
      el.style.animationDuration = `${6 + Math.random() * 8}s`;
      el.style.fontSize = `${0.8 + Math.random() * 1.2}rem`;
      el.style.opacity = 0.15 + Math.random() * 0.15;
      container.appendChild(el);
      particles.push(el);
    }

    return () => particles.forEach(p => p.remove());
  }, []);

  return (
    <div className="landing-page page-enter">
      <div className="particles-bg" ref={particlesRef} />

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-glow" />
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="gradient-text">Rubik's Cube</span>
            <br />
            <span className="hero-subtitle-text">Solver</span>
          </h1>
          <p className="hero-description">
            AI-powered solving using {size === 2 ? 'IDA* Search' : "Kociemba's Two-Phase Algorithm"}
            <br />
            <span className="hero-sub">Solve any {size}×{size} cube in ≤{size === 2 ? 11 : 22} moves with 3D visualization</span>
          </p>

          <div className="hero-badges">
            <span className="badge">⚡ ≤{size === 2 ? 11 : 22} moves</span>
            <span className="badge">🎯 Near-optimal</span>
            <span className="badge">🧠 AI detection</span>
            <span className="badge">🎮 3D visualization</span>
            <span className="badge">🧩 {size}×{size} cube</span>
          </div>

          {/* Size Toggle */}
          <div className="size-toggle">
            <button
              className={`size-btn ${size === 2 ? 'active' : ''}`}
              onClick={() => onSizeChange(2)}
            >
              2×2 Pocket
            </button>
            <button
              className={`size-btn ${size === 3 ? 'active' : ''}`}
              onClick={() => onSizeChange(3)}
            >
              3×3 Standard
            </button>
          </div>

          <Link to="/input" className="btn btn-primary btn-cta">
            Get Started
            <span className="cta-arrow">→</span>
          </Link>
        </div>

        {/* 3D Cube Hero */}
        <div className="hero-cube">
          <TwistyPlayer
            solution={[]}
            size={size}
            setupAlg=""
            height={380}
            controls={false}
          />
        </div>
      </section>

      {/* Explore Dashboard Section */}
      <section className="menu-section">
        <h2 className="section-title">
          <span className="section-num">🎮</span>
          Explore Dashboard
        </h2>
        <div className="menu-grid">
          <div className="menu-card glass-card">
            <span className="menu-card-icon">🧩</span>
            <h3 className="menu-card-title">Interactive Solver</h3>
            <p className="menu-card-desc">
              Scan your Rubik's Cube with a webcam or input colors manually to get a step-by-step animated guide.
            </p>
            <Link to="/input" className="btn btn-primary menu-card-btn">
              Open Solver ➡️
            </Link>
          </div>

          <div className="menu-card glass-card">
            <span className="menu-card-icon">🏁</span>
            <h3 className="menu-card-title">Famous Patterns</h3>
            <p className="menu-card-desc">
              Browse visual designs like Checkerboard and Superflip. Follow algorithms to paint patterns on your cube.
            </p>
            <Link to="/patterns" className="btn btn-secondary menu-card-btn">
              View Patterns ➡️
            </Link>
          </div>

          <div className="menu-card glass-card">
            <span className="menu-card-icon">📊</span>
            <h3 className="menu-card-title">Analytics & History</h3>
            <p className="menu-card-desc">
              Review your solve history logs, metrics, move averages, and progress over time.
            </p>
            <Link to="/history" className="btn btn-secondary menu-card-btn">
              Show History ➡️
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2 className="section-title">
          <span className="section-num">✨</span>
          How It Works
        </h2>
        <div className="features-grid">
          {[
            { icon: '📷', title: 'Capture', desc: 'Use your camera or manually enter the colors of each face' },
            { icon: '🧠', title: 'Detect', desc: 'AI-powered color detection with confidence scoring' },
            { icon: '⚡', title: 'Solve', desc: `Near-optimal solution in ≤${size === 2 ? 11 : 22} moves` },
            { icon: '🎮', title: 'Visualize', desc: 'Interactive 3D playback with step-by-step walkthrough' },
          ].map((feat, i) => (
            <div key={i} className="feature-card glass-card" style={{ animationDelay: `${i * 0.1}s` }}>
              <span className="feature-icon">{feat.icon}</span>
              <h3 className="feature-title">{feat.title}</h3>
              <p className="feature-desc">{feat.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-grid">
          {[
            { value: size === 2 ? '3.67M' : '43 Quintillion', label: 'Possible States' },
            { value: size === 2 ? '≤11' : '≤22', label: 'Max Moves' },
            { value: size === 2 ? 'IDA*' : 'Kociemba', label: 'Algorithm' },
            { value: '3D', label: 'Visualization' },
          ].map((stat, i) => (
            <div key={i} className="stat-card">
              <span className="stat-value gradient-text">{stat.value}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>Built with ❤️ using React & FastAPI · {size === 2 ? 'IDA*' : 'Kociemba Two-Phase'} Algorithm</p>
      </footer>
    </div>
  );
}
