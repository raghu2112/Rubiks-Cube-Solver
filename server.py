# server.py — FastAPI backend for Rubik's Cube Solver
"""
REST API exposing all cube solver functionality to the React frontend.
Keeps all existing Python modules (solver, detection, validation, utils) intact.
"""
import sys
import os
import json
import base64
import random
import datetime
import numpy as np
import cv2

# Ensure project root is on the path
_project_dir = os.path.dirname(os.path.abspath(__file__))
if _project_dir not in sys.path:
    sys.path.insert(0, _project_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from config.settings import FACES
from solver.engine import CubeSolver
from validation.validator import validate_cube_state
from utils.colors import COLOR_TO_FACE_3X3, classify_color_debug

# ── History file path ────────────────────────────────────────
_HISTORY_FILE = os.path.join(_project_dir, "solve_history.json")

def _load_history():
    try:
        with open(_HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_history(records):
    with open(_HISTORY_FILE, "w") as f:
        json.dump(records, f, indent=2)

# ── FastAPI App ──────────────────────────────────────────────
app = FastAPI(title="Rubik's Cube Solver API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request/Response Models ──────────────────────────────────
class CubeState(BaseModel):
    cube_state: dict  # {face: [colors]}
    size: int = 3

class SolveRequest(BaseModel):
    cube_state: dict
    size: int = 3

class DetectRequest(BaseModel):
    image_base64: str
    size: int = 3

class HistoryRecord(BaseModel):
    cube_state: dict
    solution: list
    move_count: int

# ── API Endpoints ────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Rubik's Cube Solver API is running"}

@app.post("/api/validate")
def validate_cube(req: CubeState):
    """Validate a cube state for physical possibility."""
    if req.size == 2:
        from solver.pocket_cube import validate_2x2
        ok, msg = validate_2x2(req.cube_state)
    else:
        ok, msg = validate_cube_state(req.cube_state, size=req.size)
    return {"valid": ok, "message": msg}

@app.post("/api/solve")
def solve_cube(req: SolveRequest):
    """Validate and solve the cube."""
    # Validate first
    if req.size == 2:
        from solver.pocket_cube import validate_2x2
        ok, msg = validate_2x2(req.cube_state)
    else:
        ok, msg = validate_cube_state(req.cube_state, size=req.size)
    
    if not ok:
        return {"success": False, "error": msg}
    
    # Solve
    solver = CubeSolver(size=req.size)
    ok2, res = solver.solve_dispatch(req.cube_state, COLOR_TO_FACE_3X3)
    
    if ok2:
        if not res:
            return {"success": True, "solution": [], "message": "Already solved!", "move_count": 0}
        return {"success": True, "solution": res, "move_count": len(res)}
    else:
        return {"success": False, "error": res}

@app.post("/api/detect-colors")
def detect_colors(req: DetectRequest):
    """Detect colors from a base64-encoded image."""
    try:
        # Decode base64 image
        img_data = base64.b64decode(req.image_base64.split(",")[-1])
        nparr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        h, w = frame_rgb.shape[:2]
        size = req.size
        cs = min(h, w) // (size + 2)
        sx = (w - size * cs) // 2
        sy = (h - size * cs) // 2
        
        # Convert to HSV for detection
        hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
        results = []
        offset = int(cs * 0.2)
        
        for row in range(size):
            for col in range(size):
                cx = sx + col * cs + cs // 2
                cy_pos = sy + row * cs + cs // 2
                y1 = max(0, cy_pos - offset)
                y2 = min(hsv.shape[0], cy_pos + offset)
                x1 = max(0, cx - offset)
                x2 = min(hsv.shape[1], cx + offset)
                roi = hsv[y1:y2, x1:x2]
                
                if roi.size == 0:
                    results.append({"color": "UNKNOWN", "confidence": 0.0})
                    continue
                
                med = np.median(roi.reshape(-1, 3), axis=0)
                color, _ = classify_color_debug(med)
                std = np.mean(np.std(roi.reshape(-1, 3), axis=0))
                conf = max(0.0, min(1.0, 1.0 - (std / 60.0)))
                results.append({"color": color, "confidence": round(conf, 3)})
        
        return {"success": True, "cells": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/random-scramble")
def random_scramble(size: int = 3):
    """Generate a random scramble."""
    if size == 2:
        from solver.pocket_cube import ALL_MOVES, MOVE_NAMES
        state = tuple('W' * 4 + 'R' * 4 + 'G' * 4 + 'Y' * 4 + 'O' * 4 + 'B' * 4)
        for _ in range(20):
            m = random.choice(MOVE_NAMES)
            state = tuple(state[ALL_MOVES[m][i]] for i in range(24))
        cube_state = {}
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        for i, face in enumerate(face_order):
            cube_state[face] = list(state[i * 4:(i + 1) * 4])
        return {"cube_state": cube_state}
    else:
        solver_dir = os.path.join(_project_dir, "solver")
        if solver_dir not in sys.path:
            sys.path.insert(0, solver_dir)
        from pykociemba.tools import randomCube
        rc = randomCube()
        m = {'U': 'W', 'R': 'R', 'F': 'G', 'D': 'Y', 'L': 'O', 'B': 'B'}
        cube_state = {}
        for i, face in enumerate(['U', 'R', 'F', 'D', 'L', 'B']):
            cube_state[face] = [m[rc[i * 9 + j]] for j in range(9)]
        return {"cube_state": cube_state}

@app.get("/api/solved-state")
def solved_state(size: int = 3):
    """Return a solved cube state."""
    n = size * size
    return {
        "cube_state": {
            'U': ['W'] * n, 'R': ['R'] * n, 'F': ['G'] * n,
            'D': ['Y'] * n, 'L': ['O'] * n, 'B': ['B'] * n
        }
    }

@app.get("/api/history")
def get_history():
    """Return solve history, newest first."""
    records = _load_history()
    return {"history": list(reversed(records))}

@app.post("/api/history")
def add_history(req: HistoryRecord):
    """Add a solve record."""
    records = _load_history()
    records.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "cube_state": req.cube_state,
        "solution": req.solution,
        "move_count": req.move_count,
    })
    if len(records) > 50:
        records = records[-50:]
    _save_history(records)
    return {"success": True}

@app.delete("/api/history")
def clear_history():
    """Clear all history."""
    _save_history([])
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  🧊 Rubik's Cube Solver — API Server")
    print("=" * 50)
    print("  Starting FastAPI server on http://localhost:8000")
    print("  API docs at http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
