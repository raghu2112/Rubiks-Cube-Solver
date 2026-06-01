// src/components/FaceEditor.jsx
import { useState } from 'react';
import { COLOR_OPTIONS, COLOR_HEX, FACE_LABELS, FACES } from '../utils/constants';
import './FaceEditor.css';

export default function FaceEditor({ cubeState, size, onSaveFace }) {
  const [selectedFace, setSelectedFace] = useState('U');
  const [editGrid, setEditGrid] = useState(
    () => cubeState[selectedFace] ? [...cubeState[selectedFace]] : Array(size * size).fill('UNKNOWN')
  );

  const handleFaceChange = (face) => {
    setSelectedFace(face);
    setEditGrid(cubeState[face] ? [...cubeState[face]] : Array(size * size).fill('UNKNOWN'));
  };

  const handleCellChange = (idx, value) => {
    setEditGrid(prev => {
      const next = [...prev];
      next[idx] = value;
      return next;
    });
  };

  const handleSave = () => {
    onSaveFace(selectedFace, editGrid);
  };

  return (
    <div className="face-editor">
      <div className="face-tabs">
        {FACES.map(f => (
          <button
            key={f}
            className={`face-tab ${selectedFace === f ? 'active' : ''}`}
            onClick={() => handleFaceChange(f)}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="face-tab-label">{FACE_LABELS[selectedFace]}</div>

      <div className="editor-grid" style={{ gridTemplateColumns: `repeat(${size}, 1fr)` }}>
        {editGrid.map((color, idx) => (
          <div key={idx} className="editor-cell">
            <div
              className="color-preview"
              style={{ background: COLOR_HEX[color] || '#94A3B8' }}
            />
            <select
              value={color}
              onChange={(e) => handleCellChange(idx, e.target.value)}
              className="color-select"
            >
              {COLOR_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
        ))}
      </div>

      <button className="btn btn-primary btn-lg editor-save-btn" onClick={handleSave}>
        💾 Save {selectedFace} Face
      </button>
    </div>
  );
}
