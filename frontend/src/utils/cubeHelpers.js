// src/utils/cubeHelpers.js
// Utility functions for cube state manipulation

/**
 * Invert a solution (for setup alg in TwistyPlayer)
 */
export function invertMoves(moves) {
  return moves.slice().reverse().map(m => {
    if (m.endsWith("'")) return m.slice(0, -1);
    if (m.endsWith('2')) return m;
    return m + "'";
  });
}

/**
 * Check if all faces have been captured (no UNKNOWN)
 */
export function isCubeComplete(cubeState) {
  return Object.values(cubeState).every(
    face => face.every(c => c !== 'UNKNOWN')
  );
}

/**
 * Count colors across the entire cube
 */
export function countColors(cubeState) {
  const counts = {};
  Object.values(cubeState).forEach(face => {
    face.forEach(color => {
      counts[color] = (counts[color] || 0) + 1;
    });
  });
  return counts;
}

/**
 * Check if cube is in solved state
 */
export function isSolved(cubeState) {
  return Object.values(cubeState).every(
    face => face.every(c => c === face[0] && c !== 'UNKNOWN')
  );
}

/**
 * Get face count based on cube size
 */
export function getFaceCount(size) {
  return size * size;
}

/**
 * Format timestamp for display
 */
export function formatTimestamp(iso) {
  if (!iso) return '';
  return iso.slice(0, 19).replace('T', ' ');
}
