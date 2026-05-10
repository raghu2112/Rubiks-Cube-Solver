# solver/pocket_cube.py
"""
2x2x2 Pocket Cube Solver using Bidirectional BFS.
God's number is 11 (HTM). We search from both solved and scrambled states,
meeting in the middle at depth ~5-6 each, which is very fast.
"""
from collections import deque

# State: tuple of 24 sticker values
# U[0-3], R[4-7], F[8-11], D[12-15], L[16-19], B[20-23]

def _apply(state, perm):
    return tuple(state[perm[i]] for i in range(24))

# ── Move Permutations (perm[dst_idx] = src_idx) ─────────────────────────
# Corner definitions with sticker indices:
# UFR: U3(3),  F1(9),  R0(4)
# UBR: U1(1),  B0(20), R1(5)
# UFL: U2(2),  F0(8),  L1(17)
# UBL: U0(0),  B1(21), L0(16)
# DFR: D1(13), F3(11), R2(6)
# DBR: D3(15), B2(22), R3(7)
# DFL: D0(12), F2(10), L3(19)
# DBL: D2(14), B3(23), L2(18)

def _make_move(cycles):
    """Build perm from list of cycles. Each cycle is [(dst, src), ...]."""
    p = list(range(24))
    for dst, src in cycles:
        p[dst] = src
    return tuple(p)

# R CW: cycle UFR->DFR->DBR->UBR->UFR
_R = _make_move([
    # UFR(3,9,4) -> UBR position means UBR gets UFR's stickers
    # Actually: UFR corner moves to DFR position.
    # Sticker at U3(3) goes to F3(11): perm[11]=3
    # Sticker at F1(9) goes to D1(13): perm[13]=9
    # Sticker at R0(4) goes to R2(6): perm[6]=4
    (11,3), (13,9), (6,4),      # UFR -> DFR
    (22,13), (15,11), (7,6),    # DFR -> DBR
    (20,15), (1,22), (5,7),     # DBR -> UBR
    (9,1), (3,20), (4,5),       # UBR -> UFR
])

# U CW: cycle UFL->UFR->UBR->UBL->UFL
_U = _make_move([
    # UFL(2,8,17) -> UFR(3,9,4)
    # U2->U3, F0->R0, L1->F1
    (3,2), (4,17), (9,8),       # UFL -> UFR
    (1,3), (20,4), (5,9),       # UFR -> UBR
    (0,1), (16,20), (21,5),     # UBR -> UBL
    (2,0), (8,21), (17,16),     # UBL -> UFL
])

# F CW: cycle UFL->UFR->DFR->DFL->UFL
_F = _make_move([
    # UFL(2,8,17) -> UFR(3,9,4)
    # U2->R0, F0->F1, L1->U3
    (4,2), (9,8), (3,17),       # UFL -> UFR
    (6,3), (11,9), (13,4),      # UFR -> DFR
    (19,13), (10,11), (12,6),   # DFR -> DFL
    (17,12), (8,10), (2,19),    # DFL -> UFL: D0->L1, F2->F0, L3->U2
])

def _build_moves():
    moves = {}
    for name, perm in [('R', _R), ('U', _U), ('F', _F)]:
        moves[name] = perm
        moves[name + '2'] = tuple(perm[perm[i]] for i in range(24))
        moves[name + "'"] = tuple(perm[perm[perm[i]]] for i in range(24))
    return moves

ALL_MOVES = _build_moves()
MOVE_NAMES = list(ALL_MOVES.keys())

def _inverse_move(m):
    if m.endswith("'"): return m[:-1]
    elif m.endswith("2"): return m
    else: return m + "'"

def _is_solved(state):
    for f in range(6):
        b = f * 4
        if not (state[b] == state[b+1] == state[b+2] == state[b+3]):
            return False
    return True

def _normalize(state):
    """Normalize by mapping the first sticker of each face-group to a canonical label.
    This handles whole-cube rotations producing different sticker arrangements for the same state."""
    return state  # For BFS on sticker tuples, no normalization needed since we fix DLB implicitly

def solve_2x2(cube_state_dict):
    """
    Solve a 2x2 cube using bidirectional BFS.
    
    Parameters: cube_state_dict: {face: [4 colors]} for U/R/F/D/L/B
    Returns: (success: bool, result: list[str] | str)
    """
    state = []
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        colors = cube_state_dict.get(face, ['UNKNOWN'] * 4)
        if len(colors) != 4:
            return False, f"Face {face} has {len(colors)} stickers, expected 4."
        if 'UNKNOWN' in colors:
            return False, f"Face {face} has undetected stickers."
        state.extend(colors)
    start = tuple(state)

    if _is_solved(start):
        return True, []

    # Determine the solved state from the center colors
    # In a valid cube, each color appears exactly 4 times; the "solved" state
    # has each face uniform. We need to figure out which color goes where.
    # The center of each face on a 2x2 is undefined, so we reconstruct from
    # the DBL corner (indices 14,23,18 = D2, B3, L2) which we treat as fixed.
    # DBL corner tells us: D-face color = state[14], B-face color = state[23], L-face color = state[18]
    # From there: U = opposite of D, F = opposite of B, R = opposite of L
    color_opposites = {'W':'Y','Y':'W','R':'O','O':'R','G':'B','B':'G'}
    d_color = start[14]  # D face center
    b_color = start[23]  # B face center
    l_color = start[18]  # L face center
    u_color = color_opposites.get(d_color, 'W')
    f_color = color_opposites.get(b_color, 'G')
    r_color = color_opposites.get(l_color, 'R')
    
    goal = tuple(
        [u_color]*4 + [r_color]*4 + [f_color]*4 +
        [d_color]*4 + [l_color]*4 + [b_color]*4
    )

    if start == goal:
        return True, []

    # Bidirectional BFS
    fwd = {start: []}  # state -> moves from start
    bwd = {goal: []}   # state -> moves from goal (reversed)
    fwd_q = deque([start])
    bwd_q = deque([goal])

    for depth in range(7):  # max 6 each side = 12 total (>11 God's number)
        # Expand forward
        next_fwd = deque()
        while fwd_q:
            s = fwd_q.popleft()
            for mn in MOVE_NAMES:
                ns = _apply(s, ALL_MOVES[mn])
                if ns not in fwd:
                    fwd[ns] = fwd[s] + [mn]
                    next_fwd.append(ns)
                    if ns in bwd:
                        # Found! Combine forward path + reversed backward path
                        bwd_moves = bwd[ns]
                        inv_bwd = [_inverse_move(m) for m in reversed(bwd_moves)]
                        return True, fwd[ns] + inv_bwd
        fwd_q = next_fwd

        # Expand backward
        next_bwd = deque()
        while bwd_q:
            s = bwd_q.popleft()
            for mn in MOVE_NAMES:
                ns = _apply(s, ALL_MOVES[mn])
                if ns not in bwd:
                    bwd[ns] = bwd[s] + [mn]
                    next_bwd.append(ns)
                    if ns in fwd:
                        fwd_moves = fwd[ns]
                        inv_bwd = [_inverse_move(m) for m in reversed(bwd[ns])]
                        return True, fwd_moves + inv_bwd
        bwd_q = next_bwd

    return False, "No solution found within search limit."

def validate_2x2(cube_state_dict):
    """Validate a 2x2 cube state."""
    all_colors = []
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        colors = cube_state_dict.get(face, [])
        if len(colors) != 4:
            return False, f"Face {face} must have exactly 4 stickers."
        all_colors.extend(colors)
    
    if 'UNKNOWN' in all_colors:
        return False, "All stickers must be detected. Please fill in any unknown cells."
    
    from collections import Counter
    counts = Counter(all_colors)
    for color in ['W', 'Y', 'R', 'O', 'G', 'B']:
        if counts.get(color, 0) != 4:
            return False, f"Color {color} appears {counts.get(color, 0)} times, expected 4."
    
    return True, "Valid"
