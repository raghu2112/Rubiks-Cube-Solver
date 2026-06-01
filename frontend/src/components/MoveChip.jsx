// src/components/MoveChip.jsx
import { useEffect, useRef } from 'react';
import { MOVE_DESC } from '../utils/constants';
import './MoveChip.css';

export default function MoveChip({ move, index, isActive, delay = 0 }) {
  const chipRef = useRef(null);

  useEffect(() => {
    if (isActive && chipRef.current) {
      chipRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'nearest'
      });
    }
  }, [isActive]);

  return (
    <div
      ref={chipRef}
      className={`move-chip ${isActive ? 'active' : ''}`}
      style={{ animationDelay: `${delay}s` }}
    >
      <span className="chip-num">{index + 1}</span>
      <span className="chip-move">{move}</span>
      <span className="chip-desc">{MOVE_DESC[move] || move}</span>
    </div>
  );
}
