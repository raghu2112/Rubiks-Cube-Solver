# validation/validator.py
"""
Validates that the user-entered cube state is physically possible
before sending it to the solver.
"""

COLOR_NAMES = {
    'W': 'White', 'Y': 'Yellow', 'R': 'Red',
    'O': 'Orange', 'G': 'Green', 'B': 'Blue',
    'UNKNOWN': 'Unknown'
}


def validate_cube_state(cube_dict, size=3):
    """
    Validates if the detected cube has the correct number of facelets per color.

    Returns (is_valid: bool, message: str).
    """
    expected_facelets = size * size  # 9 for a 3×3

    # ── Check all 6 faces exist with correct length ──────────────
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        if face not in cube_dict:
            return False, f"Face {face} is missing."
        if len(cube_dict[face]) != expected_facelets:
            return False, (f"Face {face} has {len(cube_dict[face])} stickers "
                           f"(expected {expected_facelets}).")

    # ── Check for UNKNOWN stickers ───────────────────────────────
    for face, facelets in cube_dict.items():
        for i, color in enumerate(facelets):
            if color == 'UNKNOWN':
                return False, (f"Face {face}, position {i + 1} is still Unknown. "
                               f"Please set all 54 stickers before solving.")

    # ── Count each color — must have exactly 9 of each ──────────
    color_counts = {}
    for face, facelets in cube_dict.items():
        for color in facelets:
            color_counts[color] = color_counts.get(color, 0) + 1

    for color, count in color_counts.items():
        name = COLOR_NAMES.get(color, color)
        if count != expected_facelets:
            return False, (f"{name} ({color}) appears {count} times "
                           f"(must be exactly {expected_facelets}).")

    # ── Must have exactly 6 distinct colors ──────────────────────
    if len(color_counts) != 6:
        return False, (f"Found {len(color_counts)} distinct colors "
                       f"(must be exactly 6).")

    # ── Center stickers must all be different ────────────────────
    centers = []
    for face in ['U', 'R', 'F', 'D', 'L', 'B']:
        center_idx = expected_facelets // 2  # index 4 for 3×3
        centers.append(cube_dict[face][center_idx])
    if len(set(centers)) != 6:
        return False, ("Center stickers must all be different colors. "
                       "Each face has a fixed center that defines its color.")

    return True, "Cube state is valid."
