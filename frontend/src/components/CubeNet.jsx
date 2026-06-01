// src/components/CubeNet.jsx
// 2D unfolded cube net preview — renders the classic cross layout
import { COLOR_HEX, COLOR_BORDER } from '../utils/constants';
import './CubeNet.css';

export default function CubeNet({ cubeState, size = 3 }) {
  const renderFace = (faceKey, label) => {
    const colors = cubeState[faceKey] || Array(size * size).fill('UNKNOWN');
    return (
      <div className="cube-face-container">
        <span className="face-label">{label}</span>
        <div
          className="cube-face-grid"
          style={{ gridTemplateColumns: `repeat(${size}, 1fr)` }}
        >
          {colors.map((color, idx) => (
            <div
              key={idx}
              className="cube-cell"
              style={{
                background: COLOR_HEX[color] || '#94A3B8',
                borderColor: COLOR_BORDER[color] || '#64748B',
              }}
              title={`${faceKey}[${idx}]: ${color}`}
            />
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="cube-net">
      {/* Row 1: Up */}
      <div className="cube-net-row">
        <div className="face-placeholder" />
        {renderFace('U', 'UP')}
        <div className="face-placeholder" />
        <div className="face-placeholder" />
      </div>
      {/* Row 2: Left, Front, Right, Back */}
      <div className="cube-net-row">
        {renderFace('L', 'LEFT')}
        {renderFace('F', 'FRONT')}
        {renderFace('R', 'RIGHT')}
        {renderFace('B', 'BACK')}
      </div>
      {/* Row 3: Down */}
      <div className="cube-net-row">
        <div className="face-placeholder" />
        {renderFace('D', 'DOWN')}
        <div className="face-placeholder" />
        <div className="face-placeholder" />
      </div>
    </div>
  );
}
