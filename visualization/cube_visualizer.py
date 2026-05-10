# visualization/cube_visualizer.py
"""
Premium 2D cube net renderer — supports light and dark themes.
"""

COLOR_HEX = {
    'W': '#FFFFFF', 'Y': '#FBBF24', 'R': '#DC2626',
    'O': '#F97316', 'G': '#16A34A', 'B': '#2563EB', 'UNKNOWN': '#E2E8F0'
}
COLOR_BORDER = {
    'W': '#CBD5E1', 'Y': '#D97706', 'R': '#991B1B',
    'O': '#C2410C', 'G': '#166534', 'B': '#1E40AF', 'UNKNOWN': '#94A3B8'
}

def render_face(face_colors, size=3, label=""):
    cell = 38; gap = 3
    html = f"<div style='display:flex;flex-direction:column;align-items:center;'>"
    if label:
        html += f"<span style='font-size:10px;font-weight:700;color:#64748B;margin-bottom:4px;letter-spacing:1px;text-transform:uppercase;font-family:Inter,sans-serif;'>{label}</span>"
    html += f"<div style='display:grid;grid-template-columns:repeat({size},{cell}px);gap:{gap}px;padding:5px;background:#F1F5F9;border-radius:8px;box-shadow:inset 0 1px 3px rgba(0,0,0,0.06);'>"
    for color in face_colors:
        hex_c = COLOR_HEX.get(color, '#E2E8F0')
        bdr = COLOR_BORDER.get(color, '#94A3B8')
        html += (f"<div style='width:{cell}px;height:{cell}px;background:{hex_c};"
                 f"border:2px solid {bdr};border-radius:5px;"
                 f"box-shadow:inset 0 2px 4px rgba(255,255,255,0.35),0 1px 3px rgba(0,0,0,0.1);'></div>")
    html += "</div></div>"
    return html

def render_2d_cube(cube_dict, size=3):
    """Full 2D unfolded cube net: [U] / [L][F][R][B] / [D]"""
    cell = 38; gap = 3
    face_size = size * (cell + gap) + gap + 10
    empty = f"<div style='width:{face_size}px;height:{face_size + 20}px;'></div>"
    html = "<div style='display:inline-grid;grid-template-columns:repeat(4,auto);gap:8px;padding:20px;background:#FFFFFF;border-radius:16px;border:1px solid #E2E8F0;box-shadow:0 4px 16px rgba(0,0,0,0.06);'>"
    html += empty + render_face(cube_dict.get('U',['UNKNOWN']*(size*size)),size,"UP") + empty + empty
    html += render_face(cube_dict.get('L',['UNKNOWN']*(size*size)),size,"LEFT")
    html += render_face(cube_dict.get('F',['UNKNOWN']*(size*size)),size,"FRONT")
    html += render_face(cube_dict.get('R',['UNKNOWN']*(size*size)),size,"RIGHT")
    html += render_face(cube_dict.get('B',['UNKNOWN']*(size*size)),size,"BACK")
    html += empty + render_face(cube_dict.get('D',['UNKNOWN']*(size*size)),size,"DOWN") + empty + empty
    html += "</div>"
    return html

# NOTE: 3D viewer is rendered inline in ui/app.py using the cubing.net CDN twisty-player.
