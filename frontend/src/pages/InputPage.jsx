// src/pages/InputPage.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CameraCapture from '../components/CameraCapture';
import FaceEditor from '../components/FaceEditor';
import CubeNet from '../components/CubeNet';
import { FACES, FACE_LABELS } from '../utils/constants';
import { getRandomScramble, getSolvedState, solveCube, addHistory } from '../utils/api';
import { isCubeComplete } from '../utils/cubeHelpers';
import './InputPage.css';

export default function InputPage({ cube }) {
  const navigate = useNavigate();
  const [solving, setSolving] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [loadingAction, setLoadingAction] = useState(null);

  const {
    size, cubeState, currentFaceIdx, currentFace, allCaptured,
    setFaceColors, advanceFace, setAllCaptured, setCubeState,
    setSolution, setSolveMessage, reset,
  } = cube;

  // Camera capture handler
  const handleCapture = (colors) => {
    setFaceColors(currentFace, colors);
    advanceFace();
  };

  // Random scramble
  const handleRandom = async () => {
    setLoadingAction('random');
    try {
      const res = await getRandomScramble(size);
      setCubeState(prev => ({ ...prev, ...res.cube_state }));
      setAllCaptured();
      setErrorMsg(null);
    } catch (err) {
      setErrorMsg('Failed to generate scramble');
    }
    setLoadingAction(null);
  };

  // Solved state
  const handleSolved = async () => {
    setLoadingAction('solved');
    try {
      const res = await getSolvedState(size);
      setCubeState(prev => ({ ...prev, ...res.cube_state }));
      setAllCaptured();
      setErrorMsg(null);
    } catch (err) {
      setErrorMsg('Failed to load solved state');
    }
    setLoadingAction(null);
  };

  // Solve
  const handleSolve = async () => {
    setErrorMsg(null);
    setSolving(true);
    navigate('/loading');

    try {
      const res = await solveCube(cubeState, size);
      if (res.success) {
        setSolution(res.solution);
        if (res.solution.length === 0) {
          setSolveMessage({ type: 'solved', text: 'Already solved!' });
        } else {
          setSolveMessage({ type: 'solved', text: `${res.move_count} moves` });
          // Save to history
          await addHistory(cubeState, res.solution, res.move_count);
        }
        navigate('/solution');
      } else {
        setErrorMsg(res.error);
        navigate('/input');
      }
    } catch (err) {
      setErrorMsg('Solver failed. Please check your cube state.');
      navigate('/input');
    }
    setSolving(false);
  };

  // Save face from editor
  const handleSaveFace = (face, colors) => {
    setFaceColors(face, colors);
    setSolution(null);
    setSolveMessage(null);
    setErrorMsg(null);
  };

  const capturedCount = Object.values(cubeState).filter(
    face => face.every(c => c !== 'UNKNOWN')
  ).length;

  return (
    <div className="input-page page-enter">
      <div className="input-container">
        {/* Section 1: Camera Capture */}
        <section className="input-section">
          <div className="section-header">
            <span className="section-number">1</span>
            <h2>Capture Faces</h2>
          </div>

          <div className="capture-layout">
            {/* Left: Camera / Progress */}
            <div className="capture-panel glass-card">
              {!allCaptured ? (
                <>
                  <div className="face-progress">
                    <div className="progress-bar-container">
                      <div
                        className="progress-bar-fill"
                        style={{ width: `${(currentFaceIdx / FACES.length) * 100}%` }}
                      />
                    </div>
                    <span className="progress-text">
                      Face {currentFaceIdx + 1}/6 — <strong>{FACE_LABELS[currentFace]}</strong>
                    </span>
                  </div>

                  <CameraCapture
                    size={size}
                    onCapture={handleCapture}
                    faceLabel={FACE_LABELS[currentFace]}
                  />

                  <p className="capture-hint">
                    Align the {size}×{size} cube face inside the grid overlay
                  </p>
                </>
              ) : (
                <div className="all-captured">
                  <span className="captured-icon">✅</span>
                  <h3>All 6 Faces Captured!</h3>
                  <p>You can now edit individual faces or solve the cube.</p>
                  <button className="btn btn-secondary" onClick={reset}>
                    ↩️ Reset All Captures
                  </button>
                </div>
              )}
            </div>

            {/* Right: Preview + Quick Actions */}
            <div className="preview-panel">
              <div className="quick-actions">
                <button
                  className="btn btn-secondary"
                  onClick={handleRandom}
                  disabled={loadingAction === 'random'}
                >
                  {loadingAction === 'random' ? '⏳' : '🎲'} Random Scramble
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={handleSolved}
                  disabled={loadingAction === 'solved'}
                >
                  {loadingAction === 'solved' ? '⏳' : '✨'} Solved State
                </button>
              </div>

              <div className="cube-preview-card glass-card">
                <h3 className="preview-title">Cube Preview</h3>
                <div className="cube-preview-wrapper">
                  <CubeNet cubeState={cubeState} size={size} />
                </div>
                <div className="capture-stats">
                  <span className="stat-pill">
                    {capturedCount}/6 faces
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section 2: Edit & Solve */}
        <section className="input-section">
          <div className="section-header">
            <span className="section-number">2</span>
            <h2>Edit & Solve</h2>
          </div>

          <div className="edit-layout">
            <div className="editor-panel glass-card">
              <h3>Manual Face Editor</h3>
              <FaceEditor
                cubeState={cubeState}
                size={size}
                onSaveFace={handleSaveFace}
              />
            </div>

            <div className="solve-panel glass-card">
              <div className="solve-info">
                <h3>Ready to Solve?</h3>
                <p>Ensure all faces are correctly captured or edited, then hit solve.</p>

                <div className="algo-info">
                  <span className="algo-badge">
                    {size === 2 ? '🧠 IDA* Search' : '🧠 Kociemba Two-Phase'}
                  </span>
                  <span className="algo-badge">
                    ⚡ ≤{size === 2 ? 11 : 22} moves
                  </span>
                </div>
              </div>

              <button
                className="btn btn-primary btn-lg solve-btn"
                onClick={handleSolve}
                disabled={solving || !isCubeComplete(cubeState)}
              >
                {solving ? '⏳ Solving...' : '🧠 Solve Cube'}
              </button>

              {!isCubeComplete(cubeState) && (
                <p className="solve-hint">
                  ⚠️ All faces must be filled in before solving
                </p>
              )}

              {errorMsg && (
                <div className="error-banner">
                  ❌ {errorMsg}
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
