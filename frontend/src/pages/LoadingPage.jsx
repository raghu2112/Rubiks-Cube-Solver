// src/pages/LoadingPage.jsx
import { useEffect, useState } from 'react';
import './LoadingPage.css';

const LOADING_MESSAGES = [
  'Analyzing cube state...',
  'Building solution tree...',
  'Searching for optimal moves...',
  'Almost there...',
];

export default function LoadingPage() {
  const [msgIdx, setMsgIdx] = useState(0);
  const [dots, setDots] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setMsgIdx(prev => (prev + 1) % LOADING_MESSAGES.length);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => (prev.length >= 3 ? '' : prev + '.'));
    }, 400);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-page">
      <div className="loading-glow glow-1" />
      <div className="loading-glow glow-2" />

      <div className="loading-content">
        <div className="loading-cube-container">
          <span className="loading-cube-emoji">🧊</span>
          <div className="loading-ring" />
          <div className="loading-ring ring-2" />
        </div>

        <h2 className="loading-title gradient-text">Solving Your Cube</h2>
        <p className="loading-message">
          {LOADING_MESSAGES[msgIdx]}{dots}
        </p>

        <div className="loading-progress-bar">
          <div className="loading-progress-fill" />
        </div>

        <div className="loading-particles">
          {['🟥', '🟧', '🟨', '🟩', '🟦', '⬜'].map((e, i) => (
            <span key={i} className="loading-particle" style={{
              animationDelay: `${i * 0.3}s`,
              left: `${15 + i * 12}%`,
            }}>{e}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
