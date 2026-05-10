import sys; sys.path.insert(0, '.')
import cv2, numpy as np
from utils.colors import get_color_name

# Real-world Rubik's cube HSV test cases (OpenCV: H=0-180, S/V=0-255)
# Expectations based on physical cube sticker measurements under indoor lighting
test_cases = [
    # (H, S, V, expected, description)

    # ── Orange ───────────────────────────────────────────────────────────────
    # H=8-22 is the orange zone; under warm light orange can shift to H=8-10
    (8,  200, 200, 'O', 'Orange H=8  warm-light low shift'),
    (9,  220, 200, 'O', 'Orange H=9  warm-light shifted'),
    (10, 220, 200, 'O', 'Orange H=10 boundary'),
    (12, 220, 200, 'O', 'Orange H=12 solid'),
    (15, 220, 200, 'O', 'Orange H=15 typical Rubiks cube orange'),
    (20, 220, 200, 'O', 'Orange H=20 warm orange'),
    (22, 220, 200, 'O', 'Orange H=22 upper boundary'),

    # ── Red ───────────────────────────────────────────────────────────────────
    # Pure red: H=0-7, high saturation
    (0,  220, 200, 'R', 'Red H=0'),
    (4,  220, 200, 'R', 'Red H=4 typical'),
    (7,  200, 200, 'R', 'Red H=7 upper boundary'),
    (165,220, 200, 'R', 'Red upper H=165'),
    (170,220, 200, 'R', 'Red upper H=170'),
    (175,220, 200, 'R', 'Red upper H=175'),

    # ── Yellow ────────────────────────────────────────────────────────────────
    (23, 200, 200, 'Y', 'Yellow H=23 lower boundary'),
    (27, 200, 200, 'Y', 'Yellow H=27 typical'),
    (30, 200, 200, 'Y', 'Yellow H=30 typical'),
    (35, 200, 200, 'Y', 'Yellow H=35 warm yellow'),
    (37, 200, 200, 'Y', 'Yellow H=37 upper boundary'),

    # ── Green ─────────────────────────────────────────────────────────────────
    (38, 200, 200, 'G', 'Green H=38 lower boundary'),
    (45, 200, 180, 'G', 'Green H=45 typical'),
    (60, 180, 180, 'G', 'Green H=60'),
    (80, 160, 160, 'G', 'Green H=80 dark green'),

    # ── Blue ──────────────────────────────────────────────────────────────────
    (100,200, 180, 'B', 'Blue H=100'),
    (110,200, 180, 'B', 'Blue H=110 typical'),
    (120,200, 180, 'B', 'Blue H=120'),
    (130,180, 160, 'B', 'Blue H=130'),

    # ── White ─────────────────────────────────────────────────────────────────
    (0,  15,  220, 'W', 'White low-sat high-val'),
    (60, 40,  230, 'W', 'White any-hue low-sat'),
    (90, 55,  200, 'W', 'White S=55 warm light'),
    (90, 68,  200, 'W', 'White S=68 upper sat boundary'),
]

issues = []
print("=" * 78)
print("COMPREHENSIVE COLOR DETECTION VERIFICATION (real-world expected values)")
print("=" * 78)
for h, s, v, expected, desc in test_cases:
    got = get_color_name(np.array([h, s, v], dtype=np.float64))
    ok = got == expected
    status = "OK   " if ok else "WRONG"
    if not ok:
        issues.append((h, s, v, got, expected, desc))
    print("  H=%3d S=%3d V=%3d  got=%-8s exp=%-8s  %s  %s" % (h, s, v, got, expected, status, desc))

print()
print("=" * 78)
if issues:
    print("FAILURES (%d / %d):" % (len(issues), len(test_cases)))
    for h, s, v, got, exp, desc in issues:
        print("  * H=%d S=%d V=%d: got '%s' expected '%s' -- %s" % (h, s, v, got, exp, desc))
else:
    print("ALL %d CHECKS PASSED." % len(test_cases))
print("=" * 78)
