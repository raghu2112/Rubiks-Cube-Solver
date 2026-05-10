# ui/app.py – Premium AI Rubik's Cube Solver (Light Theme SPA)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import streamlit.components.v1 as components
import cv2, numpy as np
from config.settings import DEFAULT_SIZE, FACES
from detection.color_detection import extract_colors_from_frame
from solver.engine import CubeSolver
from validation.validator import validate_cube_state
from visualization.cube_visualizer import render_2d_cube
from utils.colors import COLOR_TO_FACE_3X3, classify_color_debug

FACE_LABELS={'U':'⬆️ Up (White)','D':'⬇️ Down (Yellow)','F':'🟩 Front (Green)',
             'B':'🟦 Back (Blue)','L':'🟧 Left (Orange)','R':'🟥 Right (Red)'}
COLOR_LABELS=[("UNKNOWN","❓ Unknown"),("W","⬜ White"),("Y","🟨 Yellow"),
              ("R","🟥 Red"),("O","🟧 Orange"),("G","🟩 Green"),("B","🟦 Blue")]
COLOR_NAMES={'W':'White','Y':'Yellow','R':'Red','O':'Orange','G':'Green','B':'Blue','UNKNOWN':'Unknown'}
MOVE_DESC={'U':'Up ↻',"U'":'Up ↺','U2':'Up 180°','D':'Down ↻',"D'":'Down ↺','D2':'Down 180°',
           'R':'Right ↻',"R'":'Right ↺','R2':'Right 180°','L':'Left ↻',"L'":'Left ↺','L2':'Left 180°',
           'F':'Front ↻',"F'":'Front ↺','F2':'Front 180°','B':'Back ↻',"B'":'Back ↺','B2':'Back 180°'}

# ═══════════════════════════════════════════════════════════
CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* Base Styles */
html, body, .stApp, .stMarkdown, .stButton>button, .stSelectbox label,
[data-testid="stWidgetLabel"], [data-testid="stTab"]>button { 
    font-family: 'Inter', sans-serif !important; 
    color: #1E293B !important; 
}
.stApp {
    background: #F8FAFC !important;
}

/* Hide defaults */
#MainMenu, footer, .stDeployButton { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

/* Custom Sections */
.hero {
    text-align: center;
    padding: 6rem 1rem;
    background: #FFFFFF;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    margin-bottom: 3rem;
}
.hero h1 {
    font-size: 3.5rem;
    font-weight: 900;
    margin: 0;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #DC2626, #F97316, #FBBF24, #16A34A, #2563EB);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 5s ease infinite;
    background-size: 200% auto;
}
@keyframes gradientShift { 0% { background-position: 0% center; } 50% { background-position: 100% center; } 100% { background-position: 0% center; } }
.hero p {
    font-size: 1.2rem;
    color: #64748B;
    margin-top: 1rem;
}
.badges {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.badge {
    padding: 8px 16px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
    background: #F1F5F9;
    color: #334155;
    border: 1px solid #E2E8F0;
}

/* Glass Card */
.glass {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}

/* Section Titles */
.stitle {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.5rem;
    padding-top: 2rem;
}
.stitle .num {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1rem;
    color: #FFFFFF;
    background: linear-gradient(135deg, #2563EB, #16A34A);
    box-shadow: 0 4px 10px rgba(37,99,235,0.3);
}
.stitle span:last-child {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1E293B;
}

/* Move Chips */
.moves-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.mchip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 0.95rem;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    animation: chipIn 0.3s ease-out both;
}
.mchip .n { color: #DC2626; font-size: 0.8rem; background: #FEE2E2; padding: 2px 6px; border-radius: 6px; }
.mchip .d { color: #64748B; font-weight: 500; font-size: 0.85rem; }
@keyframes chipIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Buttons */
.stButton>button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    border: 1px solid #E2E8F0 !important;
    background: #FFFFFF !important;
    color: #1E293B !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    border-color: #CBD5E1 !important;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #DC2626, #F97316) !important;
    color: #FFFFFF !important;
    border: none !important;
}
.stButton>button[kind="primary"]:hover {
    box-shadow: 0 6px 16px rgba(220, 38, 38, 0.3) !important;
}

/* Progress */
.stProgress>div>div { background: linear-gradient(90deg, #DC2626, #F97316, #FBBF24, #16A34A, #2563EB) !important; }

/* Camera Grid (SQUARE) */
[data-testid="stCameraInputWebcamComponent"] { position: relative !important; border-radius: 16px; overflow: hidden; }
[data-testid="stCameraInputWebcamComponent"]::after {
    content:''; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
    width:min(58%,240px); aspect-ratio:1/1; pointer-events:none; z-index:10;
    background:
        repeating-linear-gradient(to right,transparent,transparent calc(33.33% - 1px),
        rgba(37,99,235,0.4) calc(33.33% - 1px),rgba(37,99,235,0.4) calc(33.33% + 1px),transparent calc(33.33% + 1px)),
        repeating-linear-gradient(to bottom,transparent,transparent calc(33.33% - 1px),
        rgba(37,99,235,0.4) calc(33.33% - 1px),rgba(37,99,235,0.4) calc(33.33% + 1px),transparent calc(33.33% + 1px));
    border: 3px solid rgba(37,99,235,0.8); border-radius: 8px;
    box-shadow: 0 0 0 9999px rgba(0,0,0,0.3); /* darkens outside of grid */
}

/* Loading Screen */
.loader-overlay {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: #FFFFFF; z-index: 9999; display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    animation: fadeOut 0.5s ease 2.5s forwards;
    pointer-events: none;
}
.loader-cube { font-size: 5rem; animation: spin 2s infinite linear; }
.loader-text {
    margin-top: 1.5rem; font-size: 1.2rem; font-weight: 700; color: #1E293B;
    background: linear-gradient(135deg, #DC2626, #F97316, #FBBF24, #16A34A, #2563EB);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
@keyframes spin { 100% { transform: rotate(360deg); } }
@keyframes fadeOut { to { opacity: 0; visibility: hidden; } }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
</style>"""

# ═══════════════════════════════════════════════════════════
def _extract(frame_rgb, size=3):
    h,w=frame_rgb.shape[:2]; cs=min(h,w)//(size+2)
    sx=(w-size*cs)//2; sy=(h-size*cs)//2
    return extract_colors_from_frame(frame_rgb,size=size,start_x=sx,start_y=sy,cell_size=cs)

def _grid_overlay(img, size=3):
    h,w=img.shape[:2]; cs=min(h,w)//(size+2)
    sx=(w-size*cs)//2; sy=(h-size*cs)//2; o=img.copy()
    for i in range(size+1):
        cv2.line(o,(sx,sy+i*cs),(sx+size*cs,sy+i*cs),(37,99,235),2)
        cv2.line(o,(sx+i*cs,sy),(sx+i*cs,sy+size*cs),(37,99,235),2)
    return o

def _invert(moves):
    r=[]
    for m in reversed(moves):
        if m.endswith("'"): r.append(m[:-1])
        elif m.endswith("2"): r.append(m)
        else: r.append(m+"'")
    return r

def _twisty_html(sol):
    a=" ".join(sol); s=" ".join(_invert(sol))
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{display:flex;justify-content:center;align-items:center;height:100vh;background:transparent}}
twisty-player{{width:100%;max-width:520px;height:100%}}
</style></head><body>
<script type="module">
import{{TwistyPlayer}}from"https://cdn.cubing.net/js/cubing/twisty";
const p=new TwistyPlayer({{puzzle:"3x3x3",alg:`{a}`,experimentalSetupAlg:`{s}`,
controlPanel:"bottom-row",background:"none",visualization:"3D",tempoScale:2}});
p.style.width="100%";p.style.height="100%";document.body.appendChild(p);
</script></body></html>"""

def _reset():
    st.session_state.cube_state={f:['UNKNOWN']*9 for f in FACES}
    st.session_state.current_face_idx=0
    st.session_state.solution=None; st.session_state.solve_msg=None

def _load_random():
    sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'solver'))
    from pykociemba.tools import randomCube
    rc=randomCube(); m={'U':'W','R':'R','F':'G','D':'Y','L':'O','B':'B'}
    for i,face in enumerate(['U','R','F','D','L','B']):
        st.session_state.cube_state[face]=[m[rc[i*9+j]] for j in range(9)]
    st.session_state.current_face_idx=len(FACES)
    st.session_state.solution=None; st.session_state.solve_msg=None

def _load_solved():
    st.session_state.cube_state={'U':['W']*9,'R':['R']*9,'F':['G']*9,'D':['Y']*9,'L':['O']*9,'B':['B']*9}
    st.session_state.current_face_idx=len(FACES)
    st.session_state.solution=None; st.session_state.solve_msg=None

# ═══════════════════════════════════════════════════════════
def run_app():
    st.set_page_config(layout="wide", page_title="AI Rubik's Solver", page_icon="🧊")
    for k, v in {'cube_state': {f: ['UNKNOWN'] * 9 for f in FACES}, 'current_face_idx': 0, 'solution': None, 'solve_msg': None, 'loaded': False}.items():
        if k not in st.session_state: st.session_state[k] = v
    st.markdown(CSS, unsafe_allow_html=True)
    
    # Loading screen (only shows once per session, handled purely via CSS animations for smooth UI)
    st.markdown("""<div class="loader-overlay">
        <div class="loader-cube">🧊</div>
        <div class="loader-text">Initializing AI Solver...</div>
    </div>""", unsafe_allow_html=True)

    # Hero / Landing Section
    st.markdown("""
    <div class="hero">
        <h1>Rubik's Cube Solver</h1>
        <p>Powered by Kociemba's Two-Phase Algorithm</p>
        <div class="badges">
            <span class="badge">⚡ ≤22 moves</span>
            <span class="badge">🎯 Near-optimal</span>
            <span class="badge">🧠 AI-powered detection</span>
            <span class="badge">🎮 3D visualization</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Rest of the content instead of tabs
    st.markdown('<div class="stitle"><span class="num">1</span><span>Camera Capture</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="large")
    fi = st.session_state.current_face_idx
    done = fi >= len(FACES)
    cf = FACES[fi] if not done else None
    
    with c1:
        with st.container(border=True):
            if not done:
                st.progress(fi/len(FACES), text=f"Face {fi+1}/6 — **{FACE_LABELS.get(cf,cf)}**")
                st.caption("Align the cube inside the grid overlay.")
                cam = st.camera_input(f"Capture {cf}", key=f"cam_{cf}_{fi}")
                if cam:
                    fb = np.frombuffer(cam.getvalue(), dtype=np.uint8)
                    fr = cv2.cvtColor(cv2.imdecode(fb, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
                    st.image(_grid_overlay(fr, DEFAULT_SIZE), caption=f"{cf} face captured", use_container_width=True)
                    colors = _extract(fr, DEFAULT_SIZE)
                    st.markdown("Detected: " + " ".join(f"**{COLOR_NAMES.get(c,c)}**" for c in colors))
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("✅ Accept", type="primary", key=f"acc_{cf}", use_container_width=True):
                            st.session_state.cube_state[cf] = colors
                            st.session_state.current_face_idx += 1
                            st.rerun()
                    with b2:
                        if st.button("🔄 Retake", key=f"ret_{cf}", use_container_width=True):
                            st.rerun()
            else:
                st.success("✅ All 6 faces captured!")
                if st.button("↩️ Reset All Captures", use_container_width=True):
                    _reset()
                    st.rerun()
                    
    with c2:
        with st.container(border=True):
            qa, qb = st.columns(2)
            with qa:
                if st.button("🎲 Random Scramble", use_container_width=True):
                    _load_random()
                    st.rerun()
            with qb:
                if st.button("✨ Solved State", use_container_width=True):
                    _load_solved()
                    st.rerun()
            st.markdown("---")
            st.markdown('<div style="font-weight:700; margin-bottom: 10px; color: #1E293B;">Cube Preview</div>', unsafe_allow_html=True)
            st.markdown(render_2d_cube(st.session_state.cube_state, size=DEFAULT_SIZE), unsafe_allow_html=True)

    st.markdown('<div class="stitle"><span class="num">2</span><span>Edit & Validate</span></div>', unsafe_allow_html=True)
    e1, e2 = st.columns([1, 1], gap="large")
    with e1:
        with st.container(border=True):
            fe = st.selectbox("Select Face to Edit", FACES, format_func=lambda f: f"{f} — {FACE_LABELS.get(f,f)}")
            ll = [l for _, l in COLOR_LABELS]
            cl = [c for c, _ in COLOR_LABELS]
            lc = {l: c for c, l in COLOR_LABELS}
            nf = []
            for row in range(3):
                cols = st.columns(3)
                for ci in range(3):
                    idx = row * 3 + ci
                    while len(st.session_state.cube_state[fe]) <= idx:
                        st.session_state.cube_state[fe].append("UNKNOWN")
                    cur = st.session_state.cube_state[fe][idx]
                    if cur not in cl: cur = "UNKNOWN"
                    clbl = next(l for c, l in COLOR_LABELS if c == cur)
                    with cols[ci]:
                        s = st.selectbox(f"C{idx}", ll, index=ll.index(clbl), key=f"g_{fe}_{idx}", label_visibility="collapsed")
                        nf.append(lc[s])
            if st.button(f"💾 Save {fe} Face", use_container_width=True):
                st.session_state.cube_state[fe] = nf
                st.session_state.solution = None
                st.session_state.solve_msg = None
                st.rerun()
                
    with e2:
        with st.container(border=True):
            st.markdown('<div style="font-weight:700; margin-bottom: 15px; color: #1E293B; font-size: 1.2rem;">Ready to Solve?</div>', unsafe_allow_html=True)
            st.write("Ensure all faces are fully captured and colors are correct. Click below when ready.")
            if st.button("🧠 Solve Cube", type="primary", use_container_width=True):
                ok, msg = validate_cube_state(st.session_state.cube_state, size=DEFAULT_SIZE)
                if not ok:
                    st.session_state.solve_msg = ("error", msg)
                    st.session_state.solution = None
                else:
                    with st.spinner("🔄 Solving with Kociemba algorithm..."):
                        solver = CubeSolver(size=DEFAULT_SIZE)
                        cs = solver.build_cube_string(st.session_state.cube_state, COLOR_TO_FACE_3X3)
                        ok2, res = solver.solve(cs)
                    if ok2:
                        st.session_state.solution = res
                        st.session_state.solve_msg = ("solved", "already") if not res else ("solved", f"{len(res)} moves")
                    else:
                        st.session_state.solve_msg = ("error", res)
                        st.session_state.solution = None
                st.rerun()
            
            if st.session_state.solve_msg:
                kind, msg = st.session_state.solve_msg
                if kind == "error":
                    st.error(f"❌ {msg}")
                elif kind == "solved" and msg == "already":
                    st.success("🎉 Already solved!")
                    st.balloons()
                elif kind == "solved":
                    st.success(f"✅ Solved in {msg}! Scroll down for the solution.")

    if st.session_state.solution and len(st.session_state.solution) > 0:
        st.markdown('<div class="stitle" id="solution-section"><span class="num">3</span><span>Solution Results</span></div>', unsafe_allow_html=True)
        sol = st.session_state.solution
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(22,163,74,0.1), rgba(37,99,235,0.05)); border: 1px solid rgba(22,163,74,0.2); border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 2rem;">
            <h2 style="margin: 0; color: #16A34A; font-weight: 900; font-size: 2.5rem;">✅ Solved in {len(sol)} moves!</h2>
            <p style="color: #64748B; margin-top: 0.5rem; font-size: 1.1rem;">Follow the sequence below or use the 3D player.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sc1, sc2 = st.columns([2, 3], gap="large")
        with sc1:
            st.markdown('<div style="font-weight:700; margin-bottom: 10px; color: #1E293B;">Move Sequence</div>', unsafe_allow_html=True)
            st.code(" ".join(sol), language=None)
            chips = '<div class="moves-wrap">'
            for i, m in enumerate(sol):
                d = MOVE_DESC.get(m, m)
                delay = i * 0.05
                chips += f'<div class="mchip" style="animation-delay:{delay}s"><span class="n">{i+1}</span>{m} <span class="d">{d}</span></div>'
            chips += '</div>'
            st.markdown(chips, unsafe_allow_html=True)
            
        with sc2:
            st.markdown('<div style="font-weight:700; margin-bottom: 10px; color: #1E293B;">3D Interactive Cube</div>', unsafe_allow_html=True)
            with st.container(border=True):
                components.html(_twisty_html(sol), height=520)
                
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 4rem; padding: 2rem; color: #94A3B8; font-size: 0.9rem; border-top: 1px solid #E2E8F0;">
        <p>Built with ❤️ using Streamlit & OpenCV.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__=="__main__":
    run_app()
