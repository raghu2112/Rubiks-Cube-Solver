// src/pages/SolutionPage.jsx
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import confetti from 'canvas-confetti';
import TwistyPlayer from '../components/TwistyPlayer';
import MoveChip from '../components/MoveChip';
import { MOVE_DESC, MOVE_INSTRUCTIONS } from '../utils/constants';
import './SolutionPage.css';

export default function SolutionPage({ cube }) {
  const navigate = useNavigate();
  const { size, solution, walkStep, setWalkStep } = cube;

  // Confetti on mount if solved
  useEffect(() => {
    if (solution && solution.length > 0) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#DC2626', '#F97316', '#FBBF24', '#16A34A', '#2563EB', '#FFFFFF'],
      });
    }
  }, [solution]);

  // Redirect if no solution
  if (!solution) {
    return (
      <div className="solution-page page-enter">
        <div className="solution-container">
          <div className="no-solution glass-card">
            <span className="no-solution-icon">🧩</span>
            <h2>No Solution Yet</h2>
            <p>Go to the Input page and solve a cube first.</p>
            <button className="btn btn-primary" onClick={() => navigate('/input')}>
              🧩 Go to Input
            </button>
          </div>
        </div>
      </div>
    );
  }

  const matchesLength = solution.length;
  const alreadySolved = matchesLength === 0;

  return (
    <div className="solution-page page-enter">
      <div className="solution-container">
        
        {/* Top Header Row */}
        <div className="solution-header">
          <button className="btn btn-secondary back-btn-sol" onClick={() => navigate('/')}>
            ← Home
          </button>
          <div className="solution-title-wrap">
            <h1 className="solution-title">
              <span className="gradient-text">
                {alreadySolved ? 'Cube Solved!' : 'Solution Dashboard'}
              </span>
            </h1>
            <p className="solution-subtitle">
              {alreadySolved 
                ? 'Your cube is already in a solved state!' 
                : `Interactive guide to solve your ${size}x${size} cube.`
              }
            </p>
          </div>
        </div>

        {alreadySolved ? (
          <div className="already-solved-card glass-card">
            <span className="solved-emoji">🎉</span>
            <h2>Your cube is already solved!</h2>
            <p>No moves are needed to solve this configuration. Try scrambing it and solving again.</p>
            <div className="solved-actions">
              <button className="btn btn-primary btn-lg" onClick={() => navigate('/input')}>
                🧩 Solve Another Cube
              </button>
            </div>
          </div>
        ) : (
          <div className="solution-layout-grid">
            
            {/* Left Column: Instructions and Step List */}
            <div className="solution-left-panel">
              
              {/* Stats & Current Instruction Card */}
              <div className="instruction-card glass-card">
                <div className="instruction-header">
                  <span className="step-badge">
                    Step {walkStep + 1} of {matchesLength}
                  </span>
                  <span className="solve-speed-label">
                    Solved in {matchesLength} moves
                  </span>
                </div>

                <div className="instruction-move-display">
                  <span className="instruction-move-notation">{solution[walkStep]}</span>
                  <span className="instruction-move-desc">
                    — {MOVE_DESC[solution[walkStep]] || solution[walkStep]}
                  </span>
                </div>

                <p className="instruction-details">
                  {MOVE_INSTRUCTIONS[solution[walkStep]] || 'Perform the indicated rotation.'}
                </p>

                {/* Walkthrough Navigation Controls */}
                <div className="walk-controls">
                  <button
                    className="btn btn-secondary"
                    onClick={() => setWalkStep(Math.max(0, walkStep - 1))}
                    disabled={walkStep <= 0}
                  >
                    ⬅️ Prev
                  </button>
                  <button
                    className="btn btn-secondary"
                    onClick={() => setWalkStep(0)}
                  >
                    🔄 Reset
                  </button>
                  <button
                    className="btn btn-primary"
                    onClick={() => setWalkStep(Math.min(solution.length - 1, walkStep + 1))}
                    disabled={walkStep >= solution.length - 1}
                  >
                    Next ➡️
                  </button>
                </div>
              </div>

              {/* Scrollable Move Sequence Card */}
              <div className="move-sequence-card glass-card">
                <h3>Full Move Sequence</h3>
                <div className="scrollable-moves-container">
                  <div className="moves-flow">
                    {solution.map((move, i) => (
                      <MoveChip
                        key={i}
                        move={move}
                        index={i}
                        isActive={i === walkStep}
                        delay={i * 0.02}
                      />
                    ))}
                  </div>
                </div>
              </div>

            </div>

            {/* Right Column: Interactive 3D Cube (Native Player) */}
            <div className="solution-right-panel glass-card">
              <div className="right-panel-header">
                <h2>3D Interactive Player</h2>
                <p>Play the animated algorithm directly on the cube simulation.</p>
              </div>

              <div className="twisty-player-panel-wrap">
                <TwistyPlayer
                  solution={solution}
                  size={size}
                  height={380}
                  controls={true}
                />
              </div>

              <div className="right-panel-footer">
                <button className="btn btn-primary solve-another-btn" onClick={() => navigate('/input')}>
                  🧩 Solve Another Cube
                </button>
              </div>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}
