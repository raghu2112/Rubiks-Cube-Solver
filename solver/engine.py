# solver/engine.py
"""
Rubik's Cube Solver Engine
Uses Herbert Kociemba's Two-Phase Algorithm (pure Python implementation).
Solves any valid 3×3 cube in ≤22 moves (typically 18-21).
"""
import sys
import os
import time

# Ensure the pykociemba package (bundled in solver/) is importable
_solver_dir = os.path.dirname(os.path.abspath(__file__))
if _solver_dir not in sys.path:
    sys.path.insert(0, _solver_dir)


# ── Eagerly import pykociemba so pruning tables load at module-import time,
#    NOT inside the solve() call where the timeout clock is ticking. ─────────
_search_mod = None
_verify_func = None

def _ensure_loaded():
    """Load pykociemba modules once (tables take ~2s on first import)."""
    global _search_mod, _verify_func
    if _search_mod is None:
        from pykociemba import search as _sm
        from pykociemba.tools import verify as _vf
        _search_mod = _sm
        _verify_func = _vf

# Pre-load on module import so Streamlit's first solve isn't slow
try:
    _ensure_loaded()
except Exception:
    pass  # Will be retried in solve()


# ── Error code mapping from pykociemba ──────────────────────────────────────
_VERIFY_ERRORS = {
    -1: "Each color must appear exactly 9 times. Check for missing or duplicate stickers.",
    -2: "Not all 12 edge pieces exist. Some sticker combinations form impossible edges.",
    -3: "Edge flip error: one edge is flipped in place (physically impossible without disassembly).",
    -4: "Not all 8 corner pieces exist. Some sticker combinations form impossible corners.",
    -5: "Corner twist error: one corner is twisted in place (physically impossible without disassembly).",
    -6: "Parity error: two pieces need to be swapped (physically impossible without disassembly).",
}


class CubeSolver:
    def __init__(self, size=3):
        self.size = size

    def solve(self, cube_string):
        """
        Solve the cube using Kociemba's Two-Phase Algorithm.

        Parameters
        ----------
        cube_string : str
            54-character string in order U1..U9, R1..R9, F1..F9, D1..D9, L1..L9, B1..B9.
            Each character is one of U, R, F, D, L, B indicating which face that sticker
            belongs to.

        Returns
        -------
        (success: bool, result: list[str] | str)
            On success: (True, list_of_moves)  — each move in WCA notation
            On failure: (False, error_message)
        """
        # Guard against undetected (UNKNOWN) cells
        if '?' in cube_string:
            return False, ("Cube has undetected (UNKNOWN) cells. "
                           "Please re-capture or manually correct the face state.")

        # Check if already solved
        if all(cube_string[i * 9] * 9 == cube_string[i * 9:(i + 1) * 9] for i in range(6)):
            return True, []

        try:
            _ensure_loaded()

            # ── Validate the cube is physically possible ────────
            err = _verify_func(cube_string)
            if err != 0:
                friendly = _VERIFY_ERRORS.get(err, f"Unknown validation error (code {err}).")
                return False, f"Invalid cube state: {friendly}"

            # ── Solve ──────────────────────────────────────────
            # maxDepth=24, timeOut=60s (generous — pure Python is slower),
            # useSeparator=False
            searcher = _search_mod.Search()
            raw = searcher.solution(cube_string, 24, 60, False)

            # Check for error codes in the result
            if raw.startswith("Error"):
                code = int(raw.split()[1])
                error_map = {
                    1: "Invalid cube string (wrong number of facelets).",
                    2: "Not all 12 edges exist exactly once.",
                    3: "One edge needs to be flipped.",
                    4: "Not all 8 corners exist exactly once.",
                    5: "One corner needs to be twisted.",
                    6: "Parity error.",
                    7: "No solution found within depth limit. Try again.",
                    8: "Solver timed out. The cube state may be extremely complex — try again.",
                }
                msg = error_map.get(code, f"Solver error code {code}.")
                return False, msg

            # Parse move string → list
            moves = raw.strip().split()
            return True, moves

        except Exception as e:
            return False, f"Solver error: {str(e)}"

    def build_cube_string(self, cube_dict, color_mapping):
        """
        Convert a color dictionary {face: [colors]} to the 54-char facelet string
        expected by the Kociemba solver.

        The facelet order is: U1..U9, R1..R9, F1..F9, D1..D9, L1..L9, B1..B9
        Each character is mapped from color name (W/Y/R/O/G/B) to face name (U/R/F/D/L/B).
        """
        order = ['U', 'R', 'F', 'D', 'L', 'B']
        result = ""
        for face in order:
            for color in cube_dict[face]:
                result += color_mapping.get(color, '?')
        return result
