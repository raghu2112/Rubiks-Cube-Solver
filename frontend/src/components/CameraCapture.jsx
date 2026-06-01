// src/components/CameraCapture.jsx
import { useRef, useState, useCallback } from 'react';
import { detectColors } from '../utils/api';
import { COLOR_HEX, COLOR_NAMES } from '../utils/constants';
import './CameraCapture.css';

export default function CameraCapture({ size, onCapture, faceLabel }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [streaming, setStreaming] = useState(false);
  const [captured, setCaptured] = useState(null);
  const [detectedCells, setDetectedCells] = useState(null);
  const [detecting, setDetecting] = useState(false);
  const streamRef = useRef(null);

  const startCamera = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: 640, height: 480 },
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setStreaming(true);
      setCaptured(null);
      setDetectedCells(null);
    } catch (err) {
      console.error('Camera access denied:', err);
      alert('Camera access denied. Please allow camera permissions.');
    }
  }, []);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
    setStreaming(false);
  }, []);

  const captureFrame = useCallback(async () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    // Draw grid overlay on the captured image
    const h = canvas.height;
    const w = canvas.width;
    const cs = Math.min(h, w) / (size + 2);
    const sx = (w - size * cs) / 2;
    const sy = (h - size * cs) / 2;
    ctx.strokeStyle = 'rgba(37, 99, 235, 0.8)';
    ctx.lineWidth = 2;
    for (let i = 0; i <= size; i++) {
      ctx.beginPath(); ctx.moveTo(sx, sy + i * cs); ctx.lineTo(sx + size * cs, sy + i * cs); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(sx + i * cs, sy); ctx.lineTo(sx + i * cs, sy + size * cs); ctx.stroke();
    }

    const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
    setCaptured(dataUrl);
    stopCamera();

    // Send to backend for color detection
    setDetecting(true);
    try {
      const result = await detectColors(dataUrl, size);
      if (result.success) {
        setDetectedCells(result.cells);
      }
    } catch (err) {
      console.error('Detection failed:', err);
    }
    setDetecting(false);
  }, [size, stopCamera]);

  const handleAccept = () => {
    if (detectedCells) {
      const colors = detectedCells.map(c => c.color);
      onCapture(colors);
      setCaptured(null);
      setDetectedCells(null);
    }
  };

  const handleRetake = () => {
    setCaptured(null);
    setDetectedCells(null);
    startCamera();
  };

  return (
    <div className="camera-capture">
      {!streaming && !captured && (
        <button className="btn btn-primary camera-start-btn" onClick={startCamera}>
          📷 Open Camera
        </button>
      )}

      {streaming && (
        <div className="camera-preview">
          <video ref={videoRef} className="camera-video" playsInline muted />
          <div className="camera-grid-overlay" style={{
            '--grid-cols': size,
          }} />
          <button className="btn btn-primary camera-capture-btn" onClick={captureFrame}>
            📸 Capture {faceLabel}
          </button>
        </div>
      )}

      {captured && (
        <div className="camera-result">
          <img src={captured} alt="Captured face" className="captured-image" />

          {detecting && (
            <div className="detecting-overlay">
              <span className="detecting-spinner">🔍</span>
              <span>Detecting colors...</span>
            </div>
          )}

          {detectedCells && (
            <>
              <div className="detected-grid" style={{ gridTemplateColumns: `repeat(${size}, 1fr)` }}>
                {detectedCells.map((cell, idx) => {
                  const pct = Math.round(cell.confidence * 100);
                  const barColor = cell.confidence > 0.7 ? '#16A34A' : cell.confidence > 0.4 ? '#FBBF24' : '#DC2626';
                  return (
                    <div key={idx} className="detected-cell">
                      <span className="detected-color-dot" style={{ color: COLOR_HEX[cell.color] }}>●</span>
                      <span className="detected-color-name">{COLOR_NAMES[cell.color]}</span>
                      <div className="conf-bar">
                        <div className="conf-fill" style={{ width: `${pct}%`, background: barColor }} />
                      </div>
                      <span className="conf-pct">{pct}%</span>
                    </div>
                  );
                })}
              </div>

              {detectedCells.some(c => c.confidence < 0.5) && (
                <div className="low-conf-warning">
                  ⚠️ Low confidence on some cells. Consider retaking or manually editing.
                </div>
              )}

              <div className="camera-actions">
                <button className="btn btn-primary" onClick={handleAccept}>✅ Accept</button>
                <button className="btn btn-secondary" onClick={handleRetake}>🔄 Retake</button>
              </div>
            </>
          )}
        </div>
      )}

      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}
