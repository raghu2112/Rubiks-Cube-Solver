# utils/colors.py
import cv2
import numpy as np

# HSV Color ranges for Rubik's Cube colors
# OpenCV HSV scale: H=0-180, S=0-255, V=0-255
#
# KEY INSIGHT: Orange and Red share the low-hue region (H=0-22).
# Under warm/incandescent indoor lighting, orange stickers shift toward H=5-10
# which overlaps with pure red. The ONLY reliable differentiator in that zone
# is that orange has a distinctly HIGHER hue center than red.
#
# Strategy used here:
#   1. White is checked first (unique: low saturation, high brightness)
#   2. Orange is checked BEFORE Red — range H=8-22, S≥100
#   3. Red lower covers H=0-7 only, S≥130 (genuine reds are deeply saturated)
#   4. Yellow: H=22-38, slightly relaxed lower S for typical yellow stickers
#   5. Green: H=35-90 — starts before the ambiguous H=40 zone
#   6. Blue: H=95-135 — slightly widened for dark/indoor-lit blue
#   7. Red upper: H=158-180 — catches upper-hue wraparound reds
#
# SATURATION strategy:
#   White:  S 0–90, V 120–255  (permissive to handle dim/indoor lighting & camera noise)
#   Others: S ≥ 80  (real stickers can read S as low as 80-90 under certain lighting)

COLOR_RANGES = {
    # key:  [lower (H, S, V)], [upper (H, S, V)]
    'W':  [(0,   0, 120), (180,  90, 255)],   # White  — any hue, S 0-90, V 120-255
    'O':  [(8,  80, 100), ( 22, 255, 255)],   # Orange — H 8-22  (checked before Red!)
    'R':  [(0, 130, 100), (  7, 255, 255)],   # Red lower — H 0-7, must be highly saturated
    'R2': [(158, 130, 80), (180, 255, 255)],  # Red upper — H 158-180
    'Y':  [(23,  80, 100), ( 37, 255, 255)],  # Yellow — H 23-37
    'G':  [(38,  60,  60), ( 85, 255, 255)],  # Green  — H 38-85
    'B':  [(95,  80,  60), (135, 255, 255)],  # Blue   — H 95-135
}

# Explicit check order — Orange MUST come before Red to prevent orange-at-low-hue
# being swallowed by the Red lower range.
_CHECK_ORDER = ['W', 'O', 'R', 'Y', 'G', 'B']

# Standard mapping: colour name → face notation used by the solver
COLOR_TO_FACE_3X3 = {
    'W': 'U',   # White  → Up
    'R': 'R',   # Red    → Right
    'G': 'F',   # Green  → Front
    'Y': 'D',   # Yellow → Down
    'O': 'L',   # Orange → Left
    'B': 'B',   # Blue   → Back
}


def get_color_name(hsv_val):
    """
    Classify a single HSV pixel value into a Rubik's cube colour name.

    hsv_val : array-like [H, S, V] in OpenCV scale (H=0-180, S/V=0-255).
    Returns  : one of 'W', 'Y', 'R', 'O', 'G', 'B', 'UNKNOWN'

    Detection notes
    ---------------
    * Orange is tested before Red in `_CHECK_ORDER` so that orange stickers
      that shift to H=8-10 under warm lighting are captured correctly.
    * Upper-hue red (H=158-180) is tested last as a dedicated fallback because
      it wraps around the hue wheel and overlaps with nothing else.
    """
    pixel = np.uint8([[hsv_val]])

    for color in _CHECK_ORDER:
        lo = np.array(COLOR_RANGES[color][0], dtype=np.uint8)
        hi = np.array(COLOR_RANGES[color][1], dtype=np.uint8)
        if cv2.inRange(pixel, lo, hi)[0][0] == 255:
            return color

    # Upper-hue red — wraps around H=180, tested separately
    lo_r2 = np.array(COLOR_RANGES['R2'][0], dtype=np.uint8)
    hi_r2 = np.array(COLOR_RANGES['R2'][1], dtype=np.uint8)
    if cv2.inRange(pixel, lo_r2, hi_r2)[0][0] == 255:
        return 'R'

    return 'UNKNOWN'


def classify_color_debug(hsv_val):
    """
    Same as get_color_name but returns a debug string showing which range matched.
    Useful for tuning — call this from the Streamlit UI color-test tool.
    """
    pixel = np.uint8([[hsv_val]])
    h, s, v = int(hsv_val[0]), int(hsv_val[1]), int(hsv_val[2])
    for color in _CHECK_ORDER:
        lo = np.array(COLOR_RANGES[color][0], dtype=np.uint8)
        hi = np.array(COLOR_RANGES[color][1], dtype=np.uint8)
        if cv2.inRange(pixel, lo, hi)[0][0] == 255:
            return color, f"H={h} S={s} V={v} → matched {color}"
    lo_r2 = np.array(COLOR_RANGES['R2'][0], dtype=np.uint8)
    hi_r2 = np.array(COLOR_RANGES['R2'][1], dtype=np.uint8)
    if cv2.inRange(pixel, lo_r2, hi_r2)[0][0] == 255:
        return 'R', f"H={h} S={s} V={v} → matched R2 (upper red)"
    return 'UNKNOWN', f"H={h} S={s} V={v} → no range matched"
