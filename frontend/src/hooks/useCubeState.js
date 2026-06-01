// src/hooks/useCubeState.js
import { useState, useCallback } from 'react';
import { FACES, INITIAL_CUBE_STATE } from '../utils/constants';

export function useCubeState(initialSize = 3) {
  const [size, setSize] = useState(initialSize);
  const [cubeState, setCubeState] = useState(() => INITIAL_CUBE_STATE(initialSize));
  const [currentFaceIdx, setCurrentFaceIdx] = useState(0);
  const [solution, setSolution] = useState(null);
  const [solveMessage, setSolveMessage] = useState(null);
  const [walkStep, setWalkStep] = useState(0);

  const reset = useCallback(() => {
    setCubeState(INITIAL_CUBE_STATE(size));
    setCurrentFaceIdx(0);
    setSolution(null);
    setSolveMessage(null);
    setWalkStep(0);
  }, [size]);

  const changeSize = useCallback((newSize) => {
    setSize(newSize);
    setCubeState(INITIAL_CUBE_STATE(newSize));
    setCurrentFaceIdx(0);
    setSolution(null);
    setSolveMessage(null);
    setWalkStep(0);
  }, []);

  const setFaceColors = useCallback((face, colors) => {
    setCubeState(prev => ({ ...prev, [face]: colors }));
  }, []);

  const advanceFace = useCallback(() => {
    setCurrentFaceIdx(prev => prev + 1);
  }, []);

  const setAllCaptured = useCallback(() => {
    setCurrentFaceIdx(FACES.length);
  }, []);

  const currentFace = currentFaceIdx < FACES.length ? FACES[currentFaceIdx] : null;
  const allCaptured = currentFaceIdx >= FACES.length;

  return {
    size,
    cubeState,
    currentFaceIdx,
    currentFace,
    allCaptured,
    solution,
    solveMessage,
    walkStep,
    setSize: changeSize,
    setCubeState,
    setFaceColors,
    advanceFace,
    setAllCaptured,
    setSolution,
    setSolveMessage,
    setWalkStep,
    reset,
  };
}
