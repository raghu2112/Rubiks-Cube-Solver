// src/utils/api.js
// API client functions for communicating with the FastAPI backend

const BASE_URL = '/api';

async function request(endpoint, options = {}) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function healthCheck() {
  return request('/health');
}

export async function solveCube(cubeState, size = 3) {
  return request('/solve', {
    method: 'POST',
    body: JSON.stringify({ cube_state: cubeState, size }),
  });
}

export async function validateCube(cubeState, size = 3) {
  return request('/validate', {
    method: 'POST',
    body: JSON.stringify({ cube_state: cubeState, size }),
  });
}

export async function detectColors(imageBase64, size = 3) {
  return request('/detect-colors', {
    method: 'POST',
    body: JSON.stringify({ image_base64: imageBase64, size }),
  });
}

export async function getRandomScramble(size = 3) {
  return request(`/random-scramble?size=${size}`);
}

export async function getSolvedState(size = 3) {
  return request(`/solved-state?size=${size}`);
}

export async function getHistory() {
  return request('/history');
}

export async function addHistory(cubeState, solution, moveCount) {
  return request('/history', {
    method: 'POST',
    body: JSON.stringify({
      cube_state: cubeState,
      solution,
      move_count: moveCount,
    }),
  });
}

export async function clearHistory() {
  return request('/history', { method: 'DELETE' });
}
