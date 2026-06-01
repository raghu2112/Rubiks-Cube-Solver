// src/pages/PatternsPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TwistyPlayer from '../components/TwistyPlayer';
import { FAMOUS_PATTERNS } from '../utils/constants';
import './PatternsPage.css';

const PATTERN_INFO = {
  '🏁 Checkerboard': {
    description: 'The classic checkerboard pattern. Every face shows alternating colors, creating a clean grid style.',
    difficulty: 'Easy',
    steps: '6 moves'
  },
  '🌀 Superflip': {
    description: 'A mind-bending configuration where every single corner is solved, but all twelve edges are flipped in place.',
    difficulty: 'Hard',
    steps: '20 moves'
  },
  '🧊 Cube in a Cube': {
    description: 'A beautiful visual illusion that looks like a mini 2x2 cube is nested inside a larger 3x3 cube.',
    difficulty: 'Medium',
    steps: '15 moves'
  },
  '➕ The Cross': {
    description: 'Generates a cross shape of a different color on all six faces of the Rubik\'s Cube.',
    difficulty: 'Medium',
    steps: '11 moves'
  },
  '🐍 Anaconda': {
    description: 'A serpentine path of colored facelets that winds across the faces, resembling an anaconda snake.',
    difficulty: 'Medium',
    steps: '14 moves'
  }
};

export default function PatternsPage() {
  const navigate = useNavigate();
  const [selectedPattern, setSelectedPattern] = useState(Object.keys(FAMOUS_PATTERNS)[0]);
  const [copied, setCopied] = useState(false);

  const handleCopy = (alg) => {
    navigator.clipboard.writeText(alg);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="patterns-page page-enter">
      <div className="patterns-container">
        
        {/* Header */}
        <div className="patterns-header">
          <button className="btn btn-secondary back-btn" onClick={() => navigate('/')}>
            ← Back to Home
          </button>
          <h1 className="patterns-title">
            <span className="gradient-text">Famous Patterns</span>
          </h1>
          <p className="patterns-subtitle">
            Cool configurations and algorithms to try on your Rubik's Cube. 
            Start from a fully solved cube and execute the algorithm.
          </p>
        </div>

        {/* Layout */}
        <div className="patterns-layout">
          
          {/* Left: Pattern Menu List */}
          <div className="patterns-list-panel">
            {Object.keys(FAMOUS_PATTERNS).map((name) => {
              const info = PATTERN_INFO[name] || {};
              const isSelected = selectedPattern === name;
              return (
                <div
                  key={name}
                  className={`pattern-card glass-card ${isSelected ? 'active' : ''}`}
                  onClick={() => setSelectedPattern(name)}
                >
                  <div className="pattern-card-header">
                    <h3>{name}</h3>
                    <span className={`badge difficulty-${info.difficulty?.toLowerCase()}`}>
                      {info.difficulty}
                    </span>
                  </div>
                  <p className="pattern-card-desc">{info.description}</p>
                  <div className="pattern-card-footer">
                    <span className="pattern-card-steps">⚡ {info.steps}</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right: Visualizer & Info */}
          <div className="patterns-visualizer-panel glass-card">
            <h2>{selectedPattern}</h2>
            
            <div className="pattern-player-wrapper">
              <TwistyPlayer
                key={selectedPattern}
                solution={[]}
                size={3}
                setupAlg={FAMOUS_PATTERNS[selectedPattern]}
                height={350}
                controls={false}
              />
            </div>

            <div className="pattern-info-card">
              <div className="info-row">
                <span className="info-label">Algorithm:</span>
                <div className="pattern-alg-box">
                  <code className="pattern-alg-code">{FAMOUS_PATTERNS[selectedPattern]}</code>
                  <button 
                    className={`btn copy-btn ${copied ? 'copied' : ''}`} 
                    onClick={() => handleCopy(FAMOUS_PATTERNS[selectedPattern])}
                  >
                    {copied ? '✅ Copied!' : '📋 Copy'}
                  </button>
                </div>
              </div>

              <div className="tip-box">
                <span className="tip-icon">ℹ️</span>
                <p>
                  Perform these moves in order. Make sure you hold the cube with White on top and Green on front for standard color alignment before starting.
                </p>
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
