// src/pages/HistoryPage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHistory, clearHistory as apiClearHistory } from '../utils/api';
import { formatTimestamp } from '../utils/cubeHelpers';
import './HistoryPage.css';

export default function HistoryPage() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load history
  useEffect(() => {
    getHistory()
      .then((res) => {
        setHistory(res.history || []);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to clear your entire solve history? This cannot be undone.')) {
      await apiClearHistory();
      setHistory([]);
    }
  };

  // Metrics calculations
  const totalSolves = history.length;
  const avgMoves = totalSolves
    ? (history.reduce((s, r) => s + (r.move_count || 0), 0) / totalSolves).toFixed(1)
    : 0;
  const bestSolve = totalSolves
    ? Math.min(...history.map((r) => r.move_count || 99))
    : 0;

  // Distribution by cube size
  const twoByTwoSolves = history.filter((r) => r.size === 2).length;
  const threeByThreeSolves = history.filter((r) => r.size === 3 || !r.size).length;

  return (
    <div className="history-page page-enter">
      <div className="history-container">
        
        {/* Header */}
        <div className="history-header">
          <button className="btn btn-secondary back-btn" onClick={() => navigate('/')}>
            ← Back to Home
          </button>
          <h1 className="history-title">
            <span className="gradient-text">Solve History</span>
          </h1>
          <p className="history-subtitle">
            Track your solving performance, analyze step metrics, and review past algorithms.
          </p>
        </div>

        {loading ? (
          <div className="history-loading-spinner">
            <span className="spinner-icon">🌀</span>
            <p>Loading analytics data...</p>
          </div>
        ) : totalSolves === 0 ? (
          <div className="history-empty-card glass-card">
            <span className="empty-icon">📊</span>
            <h2>No Solves Yet</h2>
            <p>Once you solve a Rubik's Cube on the input page, your analytics will be displayed here.</p>
            <button className="btn btn-primary" onClick={() => navigate('/input')}>
              🧩 Solve Your First Cube
            </button>
          </div>
        ) : (
          <>
            {/* Metrics Dashboard */}
            <div className="metrics-dashboard">
              <div className="metric-card glass-card">
                <span className="metric-icon">🏆</span>
                <div className="metric-info">
                  <span className="metric-value gradient-text">{totalSolves}</span>
                  <span className="metric-label">Total Solves</span>
                </div>
              </div>

              <div className="metric-card glass-card">
                <span className="metric-icon">⚡</span>
                <div className="metric-info">
                  <span className="metric-value gradient-text">{avgMoves}</span>
                  <span className="metric-label">Average Moves</span>
                </div>
              </div>

              <div className="metric-card glass-card">
                <span className="metric-icon">🎯</span>
                <div className="metric-info">
                  <span className="metric-value gradient-text">{bestSolve}</span>
                  <span className="metric-label">Best Solve (Moves)</span>
                </div>
              </div>

              <div className="metric-card glass-card">
                <span className="metric-icon">🧩</span>
                <div className="metric-info">
                  <span className="metric-value distribution-text">
                    2x2: {twoByTwoSolves} | 3x3: {threeByThreeSolves}
                  </span>
                  <span className="metric-label">Puzzle Distribution</span>
                </div>
              </div>
            </div>

            {/* List Panel */}
            <div className="history-list-panel glass-card">
              <div className="panel-header">
                <h2>Recent Solves</h2>
                <button className="btn btn-danger-outline" onClick={handleClearHistory}>
                  🗑️ Clear All
                </button>
              </div>

              <div className="history-table-wrapper">
                <div className="history-rows">
                  {history.map((rec, i) => (
                    <div key={i} className="history-row-item">
                      <div className="row-main">
                        <span className="row-date">🕐 {formatTimestamp(rec.timestamp)}</span>
                        <span className="row-size-badge">{rec.size || 3}x{rec.size || 3}</span>
                        <span className="row-moves">{rec.move_count} moves</span>
                      </div>
                      <details className="row-details">
                        <summary>View Solution Algorithm</summary>
                        <div className="details-content">
                          <code className="algorithm-code">
                            {(rec.solution || []).join(' ') || 'Already Solved'}
                          </code>
                        </div>
                      </details>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}

      </div>
    </div>
  );
}
