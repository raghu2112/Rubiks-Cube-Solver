// src/components/TwistyPlayerCustom.jsx
// Custom 3D cube player with prev/next/play buttons and speed control
// Syncs current step with parent component for move chip highlighting
import { useEffect, useRef, useState, useCallback } from 'react';
import { invertMoves } from '../utils/cubeHelpers';
import './TwistyPlayerCustom.css';

const SPEED_OPTIONS = [
  { value: 0.5, label: '0.5×' },
  { value: 1, label: '1×' },
  { value: 1.5, label: '1.5×' },
  { value: 2, label: '2×' },
  { value: 3, label: '3×' },
];

export default function TwistyPlayerCustom({
  solution = [],
  size = 3,
  currentStep = 0,
  onStepChange,
  height = 400,
}) {
  const containerRef = useRef(null);
  const playerRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [playerReady, setPlayerReady] = useState(false);
  const playTimerRef = useRef(null);

  // Create player once on mount (or when size changes)
  useEffect(() => {
    let cancelled = false;

    async function initPlayer() {
      try {
        const { TwistyPlayer } = await import('https://cdn.cubing.net/js/cubing/twisty');
        if (cancelled || !containerRef.current) return;

        containerRef.current.innerHTML = '';

        const puzzle = size === 2 ? '2x2x2' : '3x3x3';
        const setupAlg = invertMoves(solution).join(' ');
        const moveAlg = solution.length > 0 ? solution[0] : '';

        const player = new TwistyPlayer({
          puzzle,
          alg: moveAlg,
          experimentalSetupAlg: setupAlg,
          controlPanel: 'none',
          background: 'none',
          visualization: '3D',
          tempoScale: 1.5,
        });

        player.style.width = '100%';
        player.style.height = `${height}px`;
        containerRef.current.appendChild(player);
        playerRef.current = player;
        setPlayerReady(true);
      } catch (err) {
        console.error('Failed to load TwistyPlayer:', err);
      }
    }

    initPlayer();

    return () => {
      cancelled = true;
      playerRef.current = null;
      setPlayerReady(false);
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [size, solution.join(','), height]);

  // Update the displayed state when currentStep changes
  useEffect(() => {
    if (!playerRef.current || !playerReady) return;

    try {
      // Setup alg positions cube at state BEFORE the current move
      // alg shows just the current move being applied
      const remaining = solution.slice(currentStep);
      const setupAlg = invertMoves(remaining).join(' ');
      const moveAlg = currentStep < solution.length ? solution[currentStep] : '';

      playerRef.current.experimentalSetupAlg = setupAlg;
      playerRef.current.alg = moveAlg;
    } catch (err) {
      // Silently handle — player may not support direct property setting
      console.warn('Could not update TwistyPlayer:', err);
    }
  }, [currentStep, playerReady]);

  // Play/Pause timer
  useEffect(() => {
    if (isPlaying) {
      const intervalMs = Math.max(300, 1200 / speed);
      playTimerRef.current = setInterval(() => {
        onStepChange(prev => {
          if (prev >= solution.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, intervalMs);
    }

    return () => {
      if (playTimerRef.current) {
        clearInterval(playTimerRef.current);
        playTimerRef.current = null;
      }
    };
  }, [isPlaying, speed, solution.length, onStepChange]);

  // Control handlers
  const handlePrev = useCallback(() => {
    setIsPlaying(false);
    onStepChange(prev => Math.max(0, prev - 1));
  }, [onStepChange]);

  const handleNext = useCallback(() => {
    setIsPlaying(false);
    onStepChange(prev => Math.min(solution.length - 1, prev + 1));
  }, [onStepChange, solution.length]);

  const handlePlayPause = useCallback(() => {
    if (currentStep >= solution.length - 1 && !isPlaying) {
      // Restart from beginning
      onStepChange(0);
      setIsPlaying(true);
    } else {
      setIsPlaying(prev => !prev);
    }
  }, [currentStep, solution.length, isPlaying, onStepChange]);

  const handleReset = useCallback(() => {
    setIsPlaying(false);
    onStepChange(0);
  }, [onStepChange]);

  const handleGoToEnd = useCallback(() => {
    setIsPlaying(false);
    onStepChange(solution.length - 1);
  }, [onStepChange, solution.length]);

  return (
    <div className="twisty-custom">
      {/* 3D Cube Display */}
      <div className="twisty-display" ref={containerRef}>
        <div className="twisty-loading-placeholder">
          <span className="twisty-load-icon">🧊</span>
          <span>Loading 3D Cube...</span>
        </div>
      </div>

      {/* Step Indicator */}
      <div className="twisty-step-indicator">
        <div className="step-progress-track">
          <div
            className="step-progress-fill"
            style={{ width: `${((currentStep + 1) / solution.length) * 100}%` }}
          />
          {/* Step dots */}
          {solution.length <= 30 && solution.map((_, i) => (
            <button
              key={i}
              className={`step-dot ${i === currentStep ? 'active' : ''} ${i < currentStep ? 'done' : ''}`}
              style={{ left: `${((i + 0.5) / solution.length) * 100}%` }}
              onClick={() => { setIsPlaying(false); onStepChange(i); }}
              title={`Step ${i + 1}: ${solution[i]}`}
            />
          ))}
        </div>
        <span className="step-counter">{currentStep + 1} / {solution.length}</span>
      </div>

      {/* Custom Controls */}
      <div className="twisty-controls">
        <div className="controls-main">
          <button className="ctrl-btn" onClick={handleReset} title="Go to start">
            ⏮
          </button>
          <button
            className="ctrl-btn"
            onClick={handlePrev}
            disabled={currentStep <= 0}
            title="Previous move"
          >
            ⏪
          </button>
          <button
            className={`ctrl-btn play-btn ${isPlaying ? 'playing' : ''}`}
            onClick={handlePlayPause}
            title={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? '⏸' : '▶️'}
          </button>
          <button
            className="ctrl-btn"
            onClick={handleNext}
            disabled={currentStep >= solution.length - 1}
            title="Next move"
          >
            ⏩
          </button>
          <button className="ctrl-btn" onClick={handleGoToEnd} title="Go to end">
            ⏭
          </button>
        </div>

        {/* Speed Control */}
        <div className="speed-control">
          <span className="speed-label">Speed</span>
          <div className="speed-buttons">
            {SPEED_OPTIONS.map(opt => (
              <button
                key={opt.value}
                className={`speed-btn ${speed === opt.value ? 'active' : ''}`}
                onClick={() => setSpeed(opt.value)}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
