// src/utils/constants.js
// All static data: face labels, color maps, move descriptions

export const FACES = ['U', 'R', 'F', 'D', 'L', 'B'];

export const FACE_LABELS = {
  U: '⬆️ Up (White)',
  D: '⬇️ Down (Yellow)',
  F: '🟩 Front (Green)',
  B: '🟦 Back (Blue)',
  L: '🟧 Left (Orange)',
  R: '🟥 Right (Red)',
};

export const COLOR_OPTIONS = [
  { value: 'UNKNOWN', label: '❓ Unknown', emoji: '❓' },
  { value: 'W', label: '⬜ White', emoji: '⬜' },
  { value: 'Y', label: '🟨 Yellow', emoji: '🟨' },
  { value: 'R', label: '🟥 Red', emoji: '🟥' },
  { value: 'O', label: '🟧 Orange', emoji: '🟧' },
  { value: 'G', label: '🟩 Green', emoji: '🟩' },
  { value: 'B', label: '🟦 Blue', emoji: '🟦' },
];

export const COLOR_NAMES = {
  W: 'White', Y: 'Yellow', R: 'Red',
  O: 'Orange', G: 'Green', B: 'Blue',
  UNKNOWN: 'Unknown',
};

export const COLOR_HEX = {
  W: '#FFFFFF', Y: '#FBBF24', R: '#DC2626',
  O: '#F97316', G: '#16A34A', B: '#2563EB',
  UNKNOWN: '#94A3B8',
};

export const COLOR_HEX_DARK = {
  W: '#F1F5F9', Y: '#F59E0B', R: '#EF4444',
  O: '#FB923C', G: '#22C55E', B: '#3B82F6',
  UNKNOWN: '#64748B',
};

export const COLOR_BORDER = {
  W: '#CBD5E1', Y: '#D97706', R: '#991B1B',
  O: '#C2410C', G: '#166534', B: '#1E40AF',
  UNKNOWN: '#64748B',
};

export const MOVE_DESC = {
  'U': 'Up ↻', "U'": 'Up ↺', 'U2': 'Up 180°',
  'D': 'Down ↻', "D'": 'Down ↺', 'D2': 'Down 180°',
  'R': 'Right ↻', "R'": 'Right ↺', 'R2': 'Right 180°',
  'L': 'Left ↻', "L'": 'Left ↺', 'L2': 'Left 180°',
  'F': 'Front ↻', "F'": 'Front ↺', 'F2': 'Front 180°',
  'B': 'Back ↻', "B'": 'Back ↺', 'B2': 'Back 180°',
};

export const MOVE_INSTRUCTIONS = {
  'U': 'Hold the cube steady. Rotate the TOP face 90° clockwise (when viewed from above).',
  "U'": 'Hold the cube steady. Rotate the TOP face 90° counter-clockwise.',
  'U2': 'Rotate the TOP face 180°.',
  'D': 'Rotate the BOTTOM face 90° clockwise (viewed from below).',
  "D'": 'Rotate the BOTTOM face 90° counter-clockwise.',
  'D2': 'Rotate the BOTTOM face 180°.',
  'R': 'Rotate the RIGHT face 90° clockwise (viewed from the right).',
  "R'": 'Rotate the RIGHT face 90° counter-clockwise.',
  'R2': 'Rotate the RIGHT face 180°.',
  'L': 'Rotate the LEFT face 90° clockwise (viewed from the left).',
  "L'": 'Rotate the LEFT face 90° counter-clockwise.',
  'L2': 'Rotate the LEFT face 180°.',
  'F': 'Rotate the FRONT face 90° clockwise (viewed from the front).',
  "F'": 'Rotate the FRONT face 90° counter-clockwise.',
  'F2': 'Rotate the FRONT face 180°.',
  'B': 'Rotate the BACK face 90° clockwise (viewed from the back).',
  "B'": 'Rotate the BACK face 90° counter-clockwise.',
  'B2': 'Rotate the BACK face 180°.',
};

export const FAMOUS_PATTERNS = {
  '🏁 Checkerboard': 'U2 D2 F2 B2 L2 R2',
  '🌀 Superflip': "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2",
  '🧊 Cube in a Cube': "F L F U' R U F2 L2 U' L' B D' B' L2 U",
  '➕ The Cross': "U F B' L2 U2 L2 F' B U2 L2 U",
  '🐍 Anaconda': "L U B' U' R L' B R' F B' D R D' F'",
};

export const INITIAL_CUBE_STATE = (size = 3) => {
  const n = size * size;
  return {
    U: Array(n).fill('UNKNOWN'),
    R: Array(n).fill('UNKNOWN'),
    F: Array(n).fill('UNKNOWN'),
    D: Array(n).fill('UNKNOWN'),
    L: Array(n).fill('UNKNOWN'),
    B: Array(n).fill('UNKNOWN'),
  };
};
