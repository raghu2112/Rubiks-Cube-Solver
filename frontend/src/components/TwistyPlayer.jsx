// src/components/TwistyPlayer.jsx
// Wrapper for cubing.net's TwistyPlayer web component
import { useEffect, useRef } from 'react';
import './TwistyPlayer.css';

export default function TwistyPlayer({
  solution = [],
  size = 3,
  setupAlg = '',
  height = 400,
  controls = true,
  autoPlay = false,
}) {
  const containerRef = useRef(null);
  const playerRef = useRef(null);

  useEffect(() => {
    let cancelled = false;

    async function loadPlayer() {
      try {
        const { TwistyPlayer } = await import('https://cdn.cubing.net/js/cubing/twisty');

        if (cancelled || !containerRef.current) return;

        // Clear previous player
        containerRef.current.innerHTML = '';

        const puzzle = size === 2 ? '2x2x2' : '3x3x3';
        const algStr = solution.join(' ');

        // Compute setup alg: if we have a solution, the setup is the inverse
        let setup = setupAlg;
        if (!setup && solution.length > 0) {
          const inv = solution.slice().reverse().map(m => {
            if (m.endsWith("'")) return m.slice(0, -1);
            if (m.endsWith('2')) return m;
            return m + "'";
          });
          setup = inv.join(' ');
        }

        const player = new TwistyPlayer({
          puzzle,
          alg: algStr,
          experimentalSetupAlg: setup,
          controlPanel: controls ? 'bottom-row' : 'none',
          background: 'none',
          visualization: '3D',
          tempoScale: 2,
        });

        player.style.width = '100%';
        player.style.height = `${height}px`;
        containerRef.current.appendChild(player);
        playerRef.current = player;
      } catch (err) {
        console.error('Failed to load TwistyPlayer:', err);
      }
    }

    loadPlayer();

    return () => {
      cancelled = true;
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [solution.join(','), size, setupAlg, height, controls]);

  return (
    <div className="twisty-player-wrapper" ref={containerRef}>
      <div className="twisty-loading">
        <span className="twisty-spinner">🧊</span>
        <span>Loading 3D Cube...</span>
      </div>
    </div>
  );
}
