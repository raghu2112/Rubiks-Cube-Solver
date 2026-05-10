# ui/app.py – Premium AI Rubik's Cube Solver (Light/Dark SPA + Walkthrough + History)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import cv2, numpy as np
from config.settings import DEFAULT_SIZE, FACES
from detection.color_detection import extract_colors_from_frame
from solver.engine import CubeSolver
from validation.validator import validate_cube_state
from visualization.cube_visualizer import render_2d_cube
from utils.colors import COLOR_TO_FACE_3X3, classify_color_debug
from ui.styles import get_css
from ui.session_history import add_record, get_history, clear_history

FACE_LABELS={'U':'⬆️ Up (White)','D':'⬇️ Down (Yellow)','F':'🟩 Front (Green)',
             'B':'🟦 Back (Blue)','L':'🟧 Left (Orange)','R':'🟥 Right (Red)'}
COLOR_LABELS=[("UNKNOWN","❓ Unknown"),("W","⬜ White"),("Y","🟨 Yellow"),
              ("R","🟥 Red"),("O","🟧 Orange"),("G","🟩 Green"),("B","🟦 Blue")]
COLOR_NAMES={'W':'White','Y':'Yellow','R':'Red','O':'Orange','G':'Green','B':'Blue','UNKNOWN':'Unknown'}
COLOR_HEX_MAP={'W':'#FFFFFF','Y':'#FBBF24','R':'#DC2626','O':'#F97316','G':'#16A34A','B':'#2563EB','UNKNOWN':'#94A3B8'}
MOVE_DESC={'U':'Up ↻',"U'":'Up ↺','U2':'Up 180°','D':'Down ↻',"D'":'Down ↺','D2':'Down 180°',
           'R':'Right ↻',"R'":'Right ↺','R2':'Right 180°','L':'Left ↻',"L'":'Left ↺','L2':'Left 180°',
           'F':'Front ↻',"F'":'Front ↺','F2':'Front 180°','B':'Back ↻',"B'":'Back ↺','B2':'Back 180°'}
MOVE_INSTRUCT={
    'U':'Hold the cube steady. Rotate the TOP face 90° clockwise (when viewed from above).',
    "U'":'Hold the cube steady. Rotate the TOP face 90° counter-clockwise.',
    'U2':'Rotate the TOP face 180°.',
    'D':'Rotate the BOTTOM face 90° clockwise (viewed from below).',
    "D'":'Rotate the BOTTOM face 90° counter-clockwise.',
    'D2':'Rotate the BOTTOM face 180°.',
    'R':'Rotate the RIGHT face 90° clockwise (viewed from the right).',
    "R'":'Rotate the RIGHT face 90° counter-clockwise.',
    'R2':'Rotate the RIGHT face 180°.',
    'L':'Rotate the LEFT face 90° clockwise (viewed from the left).',
    "L'":'Rotate the LEFT face 90° counter-clockwise.',
    'L2':'Rotate the LEFT face 180°.',
    'F':'Rotate the FRONT face 90° clockwise (viewed from the front).',
    "F'":'Rotate the FRONT face 90° counter-clockwise.',
    'F2':'Rotate the FRONT face 180°.',
    'B':'Rotate the BACK face 90° clockwise (viewed from the back).',
    "B'":'Rotate the BACK face 90° counter-clockwise.',
    'B2':'Rotate the BACK face 180°.',
}

# ═══════════════════════════════════════════════════════════
def _extract(frame_rgb, size=3):
    h,w=frame_rgb.shape[:2]; cs=min(h,w)//(size+2)
    sx=(w-size*cs)//2; sy=(h-size*cs)//2
    return extract_colors_from_frame(frame_rgb,size=size,start_x=sx,start_y=sy,cell_size=cs)

def _extract_confidence(frame_rgb, size=3):
    """Extract colors WITH confidence scores for each cell."""
    h,w=frame_rgb.shape[:2]; cs=min(h,w)//(size+2)
    sx=(w-size*cs)//2; sy=(h-size*cs)//2
    hsv=cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
    results=[]
    offset=int(cs*0.2)
    for row in range(size):
        for col in range(size):
            cx=sx+col*cs+cs//2; cy=sy+row*cs+cs//2
            y1=max(0,cy-offset); y2=min(hsv.shape[0],cy+offset)
            x1=max(0,cx-offset); x2=min(hsv.shape[1],cx+offset)
            roi=hsv[y1:y2,x1:x2]
            if roi.size==0:
                results.append(('UNKNOWN',0.0)); continue
            med=np.median(roi.reshape(-1,3),axis=0)
            color,_=classify_color_debug(med)
            # Confidence: how consistent the ROI is (lower std = higher confidence)
            std=np.mean(np.std(roi.reshape(-1,3),axis=0))
            conf=max(0.0,min(1.0,1.0-(std/60.0)))
            results.append((color,conf))
    return results

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

def _twisty_html(sol, size=3):
    a=" ".join(sol); s=" ".join(_invert(sol))
    puzzle = '2x2x2' if size == 2 else '3x3x3'
    return f"""<!DOCTYPE html><html><head><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{display:flex;justify-content:center;align-items:center;height:520px;background:transparent}}
twisty-player{{width:100%;max-width:520px;height:100%}}
</style></head><body>
<script type="module">
import{{TwistyPlayer}}from"https://cdn.cubing.net/js/cubing/twisty";
const p=new TwistyPlayer({{puzzle:"{puzzle}",alg:`{a}`,experimentalSetupAlg:`{s}`,
controlPanel:"bottom-row",background:"none",visualization:"3D",tempoScale:2}});
p.style.width="100%";p.style.height="100%";document.body.appendChild(p);
</script></body></html>"""

def _get_size():
    return st.session_state.get('cube_size', 3)

def _cells():
    return _get_size() ** 2

def _reset():
    n = _cells()
    st.session_state.cube_state={f:['UNKNOWN']*n for f in FACES}
    st.session_state.current_face_idx=0
    st.session_state.solution=None; st.session_state.solve_msg=None
    st.session_state.walk_step=0

def _load_random():
    sz = _get_size()
    if sz == 2:
        # Generate a random 2x2 scramble by applying random moves
        import random
        from solver.pocket_cube import ALL_MOVES, MOVE_NAMES
        state = tuple('W'*4 + 'R'*4 + 'G'*4 + 'Y'*4 + 'O'*4 + 'B'*4)
        for _ in range(20):
            m = random.choice(MOVE_NAMES)
            state = tuple(state[ALL_MOVES[m][i]] for i in range(24))
        for i, face in enumerate(['U','R','F','D','L','B']):
            st.session_state.cube_state[face] = list(state[i*4:(i+1)*4])
    else:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'solver'))
        from pykociemba.tools import randomCube
        rc = randomCube(); m = {'U':'W','R':'R','F':'G','D':'Y','L':'O','B':'B'}
        for i, face in enumerate(['U','R','F','D','L','B']):
            st.session_state.cube_state[face] = [m[rc[i*9+j]] for j in range(9)]
    st.session_state.current_face_idx = len(FACES)
    st.session_state.solution = None; st.session_state.solve_msg = None

def _load_solved():
    n = _cells()
    solved = {'U':['W']*n,'R':['R']*n,'F':['G']*n,'D':['Y']*n,'L':['O']*n,'B':['B']*n}
    st.session_state.cube_state = solved
    st.session_state.current_face_idx = len(FACES)
    st.session_state.solution = None; st.session_state.solve_msg = None

# ═══════════════════════════════════════════════════════════
def run_app():
    st.set_page_config(layout="wide", page_title="AI Rubik's Solver", page_icon="🧊")
    if 'cube_size' not in st.session_state: st.session_state.cube_size = 3
    n = st.session_state.cube_size ** 2
    defaults={'cube_state':{f:['UNKNOWN']*n for f in FACES},'current_face_idx':0,
              'solution':None,'solve_msg':None,'dark_mode':False,'walk_step':0}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v

    # ── Sidebar: Settings ──
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        dark = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dm_toggle")
        if dark != st.session_state.dark_mode:
            st.session_state.dark_mode = dark
            st.rerun()
        st.markdown("---")
        st.markdown("### 🧩 Cube Type")
        new_size = st.radio("Select cube size", [2, 3], index=[2,3].index(st.session_state.cube_size),
                            format_func=lambda x: f"{x}×{x} {'(Pocket Cube)' if x==2 else '(Standard)'}")
        if new_size != st.session_state.cube_size:
            st.session_state.cube_size = new_size
            _reset(); st.rerun()
        st.markdown("---")
        st.markdown("### 🧊 Rubik's Solver")
        algo = 'IDA* Search' if st.session_state.cube_size == 2 else 'Kociemba Two-Phase'
        limit = '≤ 11 moves' if st.session_state.cube_size == 2 else '≤ 22 moves'
        st.caption(f"{algo}")
        st.caption(f"{limit} • Near-optimal")

    st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

    # ── Loading Screen ──
    st.markdown("""<div class="loader-overlay">
        <div class="loader-cube">🧊</div>
        <div class="loader-text">Initializing AI Solver...</div>
    </div>""", unsafe_allow_html=True)

    # ── Hero / Landing ──
    sz = st.session_state.cube_size
    algo_name = 'IDA* Search' if sz == 2 else "Kociemba's Two-Phase Algorithm"
    move_limit = '≤11' if sz == 2 else '≤22'
    st.markdown(f"""<div class="hero">
        <h1>Rubik's Cube Solver</h1>
        <p>Powered by {algo_name} · {sz}×{sz} Mode</p>
        <div class="badges">
            <span class="badge">⚡ {move_limit} moves</span>
            <span class="badge">🎯 Near-optimal</span>
            <span class="badge">🧠 AI-powered detection</span>
            <span class="badge">🎮 3D visualization</span>
            <span class="badge">🧩 {sz}×{sz} cube</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ═══ SECTION 1: Camera Capture ═══
    st.markdown('<div class="stitle"><span class="num">1</span><span>Camera Capture</span></div>', unsafe_allow_html=True)
    cube_sz = st.session_state.cube_size
    c1, c2 = st.columns([1, 1], gap="large")
    fi = st.session_state.current_face_idx
    done = fi >= len(FACES)
    cf = FACES[fi] if not done else None

    with c1:
        with st.container(border=True):
            if not done:
                st.progress(fi/len(FACES), text=f"Face {fi+1}/6 — **{FACE_LABELS.get(cf,cf)}** ({cube_sz}×{cube_sz})")
                st.caption(f"Align the {cube_sz}×{cube_sz} cube inside the grid overlay.")
                cam = st.camera_input(f"Capture {cf}", key=f"cam_{cf}_{fi}_{cube_sz}")
                if cam:
                    fb = np.frombuffer(cam.getvalue(), dtype=np.uint8)
                    fr = cv2.cvtColor(cv2.imdecode(fb, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
                    st.image(_grid_overlay(fr, cube_sz), caption=f"{cf} face captured", width="stretch")
                    # Color detection with confidence
                    conf_results = _extract_confidence(fr, cube_sz)
                    colors = [c for c,_ in conf_results]
                    # Display confidence grid
                    st.markdown("**Detected Colors & Confidence:**")
                    for row in range(cube_sz):
                        cols_ui = st.columns(cube_sz)
                        for ci in range(cube_sz):
                            idx = row*cube_sz+ci
                            clr, conf = conf_results[idx]
                            hex_c = COLOR_HEX_MAP.get(clr,'#94A3B8')
                            pct = int(conf*100)
                            bar_color = '#16A34A' if conf>0.7 else '#FBBF24' if conf>0.4 else '#DC2626'
                            with cols_ui[ci]:
                                st.markdown(f"""<div style="text-align:center;font-size:0.8rem;font-weight:600;">
                                    <span style="color:{hex_c}">●</span> {COLOR_NAMES.get(clr,clr)}
                                    <div class="conf-bar"><div class="conf-fill" style="width:{pct}%;background:{bar_color};"></div></div>
                                    <span style="font-size:0.7rem;color:#94A3B8">{pct}%</span>
                                </div>""", unsafe_allow_html=True)
                    low_conf = [i for i,(c,conf) in enumerate(conf_results) if conf<0.5]
                    if low_conf:
                        st.warning(f"⚠️ Low confidence on cells: {', '.join(str(i+1) for i in low_conf)}. Consider retaking or manually editing.")
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
                    _reset(); st.rerun()

    with c2:
        with st.container(border=True):
            qa, qb = st.columns(2)
            with qa:
                if st.button("🎲 Random Scramble", use_container_width=True):
                    _load_random(); st.rerun()
            with qb:
                if st.button("✨ Solved State", use_container_width=True):
                    _load_solved(); st.rerun()
            st.markdown("---")
            st.markdown("**Cube Preview**")
            st.markdown(render_2d_cube(st.session_state.cube_state, size=cube_sz), unsafe_allow_html=True)

    # ═══ SECTION 2: Edit & Validate ═══
    st.markdown('<div class="stitle"><span class="num">2</span><span>Edit & Validate</span></div>', unsafe_allow_html=True)
    e1, e2 = st.columns([1, 1], gap="large")
    with e1:
        with st.container(border=True):
            fe = st.selectbox("Select Face to Edit", FACES, format_func=lambda f: f"{f} — {FACE_LABELS.get(f,f)}")
            ll=[l for _,l in COLOR_LABELS]; cl=[c for c,_ in COLOR_LABELS]; lc={l:c for c,l in COLOR_LABELS}
            nf=[]
            for row in range(cube_sz):
                cols=st.columns(cube_sz)
                for ci in range(cube_sz):
                    idx=row*cube_sz+ci
                    while len(st.session_state.cube_state[fe])<=idx:
                        st.session_state.cube_state[fe].append("UNKNOWN")
                    cur=st.session_state.cube_state[fe][idx]
                    if cur not in cl: cur="UNKNOWN"
                    clbl=next(l for c,l in COLOR_LABELS if c==cur)
                    with cols[ci]:
                        s=st.selectbox(f"C{idx}",ll,index=ll.index(clbl),key=f"g_{fe}_{idx}",label_visibility="collapsed")
                        nf.append(lc[s])
            if st.button(f"💾 Save {fe} Face", use_container_width=True):
                st.session_state.cube_state[fe]=nf
                st.session_state.solution=None; st.session_state.solve_msg=None; st.rerun()

    with e2:
        with st.container(border=True):
            st.markdown("**Ready to Solve?**")
            st.write("Ensure all faces are correctly captured. Click below when ready.")
            if st.button("🧠 Solve Cube", type="primary", use_container_width=True):
                if cube_sz == 2:
                    from solver.pocket_cube import validate_2x2
                    ok, msg = validate_2x2(st.session_state.cube_state)
                else:
                    ok, msg = validate_cube_state(st.session_state.cube_state, size=cube_sz)
                if not ok:
                    st.session_state.solve_msg=("error",msg); st.session_state.solution=None
                else:
                    algo_label = 'IDA*' if cube_sz == 2 else 'Kociemba'
                    with st.spinner(f"🔄 Solving with {algo_label} algorithm..."):
                        solver=CubeSolver(size=cube_sz)
                        ok2,res=solver.solve_dispatch(st.session_state.cube_state, COLOR_TO_FACE_3X3)
                    if ok2:
                        st.session_state.solution=res
                        st.session_state.walk_step=0
                        if not res:
                            st.session_state.solve_msg=("solved","already")
                        else:
                            st.session_state.solve_msg=("solved",f"{len(res)} moves")
                            add_record(st.session_state.cube_state, res, len(res))
                    else:
                        st.session_state.solve_msg=("error",res); st.session_state.solution=None
                st.rerun()

            if st.session_state.solve_msg:
                kind,msg=st.session_state.solve_msg
                if kind=="error": st.error(f"❌ {msg}")
                elif kind=="solved" and msg=="already": st.success("🎉 Already solved!"); st.balloons()
                elif kind=="solved": st.success(f"✅ Solved in {msg}! Scroll down.")

    # ═══ SECTION 3: Solution + Walkthrough ═══
    if st.session_state.solution and len(st.session_state.solution)>0:
        st.markdown('<div class="stitle"><span class="num">3</span><span>Solution Results</span></div>', unsafe_allow_html=True)
        sol=st.session_state.solution

        st.markdown(f"""<div class="sbanner">
            <h2>✅ Solved in {len(sol)} moves!</h2>
            <p>Follow the sequence below or use the 3D player.</p>
        </div>""", unsafe_allow_html=True)

        sc1, sc2 = st.columns([2, 3], gap="large")
        with sc1:
            st.markdown("**Move Sequence**")
            st.code(" ".join(sol), language=None)
            chips='<div class="moves-wrap">'
            for i,m in enumerate(sol):
                d=MOVE_DESC.get(m,m); delay=i*0.05
                act=' active' if i==st.session_state.walk_step else ''
                chips+=f'<div class="mchip{act}" style="animation-delay:{delay}s"><span class="n">{i+1}</span>{m} <span class="d">{d}</span></div>'
            chips+='</div>'
            st.markdown(chips, unsafe_allow_html=True)

        with sc2:
            st.markdown("**3D Interactive Cube**")
            with st.container(border=True):
                import streamlit.components.v1 as components
                components.html(_twisty_html(sol, cube_sz), height=520)

        # ── Step-by-Step Walkthrough ──
        st.markdown('<div class="stitle"><span class="num">4</span><span>Step-by-Step Walkthrough</span></div>', unsafe_allow_html=True)
        with st.container(border=True):
            step=st.session_state.walk_step
            cur_move=sol[step]
            st.markdown(f"**Step {step+1} of {len(sol)}**")
            st.progress((step+1)/len(sol))
            st.markdown(f"""<div class="step-desc">
                <span class="step-move">{cur_move}</span> — {MOVE_DESC.get(cur_move, cur_move)}
                <br><br>{MOVE_INSTRUCT.get(cur_move, 'Perform the indicated rotation.')}
            </div>""", unsafe_allow_html=True)
            p1,p2,p3=st.columns([1,1,1])
            with p1:
                if st.button("⬅️ Previous", use_container_width=True, disabled=step<=0):
                    st.session_state.walk_step=max(0,step-1); st.rerun()
            with p2:
                if st.button("🔄 Reset", use_container_width=True):
                    st.session_state.walk_step=0; st.rerun()
            with p3:
                if st.button("➡️ Next", use_container_width=True, disabled=step>=len(sol)-1):
                    st.session_state.walk_step=min(len(sol)-1,step+1); st.rerun()

    # ═══ SECTION 5: Famous Patterns ═══
    st.markdown('<div class="stitle"><span class="num">5</span><span>Famous Patterns</span></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("Want to make your solved cube look cool? Try these famous patterns! (Best on 3×3)")
        patterns = {
            "🏁 Checkerboard": "U2 D2 F2 B2 L2 R2",
            "🌀 Superflip (Every edge flipped)": "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2",
            "🧊 Cube in a Cube": "F L F U' R U F2 L2 U' L' B D' B' L2 U",
            "➕ The Cross": "U F B' L2 U2 L2 F' B U2 L2 U",
            "🐍 Anaconda": "L U B' U' R L' B R' F B' D R D' F'"
        }
        pat_name = st.selectbox("Select a pattern", list(patterns.keys()))
        pat_alg = patterns[pat_name]
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(f"**Algorithm:**")
            st.code(pat_alg, language=None)
            st.info("Start with a completely solved cube, and perform these moves.")
        with c2:
            import streamlit.components.v1 as components
            # We use experimentalSetupAlg to put the cube in the pattern state
            html = f"""<!DOCTYPE html><html><head><style>
            *{{margin:0;padding:0;box-sizing:border-box}}
            body{{display:flex;justify-content:center;align-items:center;height:300px;background:transparent}}
            twisty-player{{width:100%;max-width:300px;height:100%}}
            </style></head><body>
            <script type="module">
            import{{TwistyPlayer}}from"https://cdn.cubing.net/js/cubing/twisty";
            const p=new TwistyPlayer({{puzzle:"3x3x3",alg:"",experimentalSetupAlg:"{pat_alg}",
            controlPanel:"none",background:"none",visualization:"3D",tempoScale:2}});
            document.body.appendChild(p);
            </script></body></html>"""
            components.html(html, height=300)

    # ═══ SECTION 6: Solve Analytics & History ═══
    st.markdown('<div class="stitle"><span class="num">6</span><span>Solve Analytics & History</span></div>', unsafe_allow_html=True)
    with st.container(border=True):
        history=get_history()
        if not history:
            st.info("No solves recorded yet. Solve a cube to see your analytics!")
        else:
            # Analytics Dashboard
            m1, m2 = st.columns(2)
            total_solves = len(history)
            avg_moves = sum(r.get('move_count',0) for r in history) / total_solves
            m1.metric("Total Solves Recorded", total_solves)
            m2.metric("Average Move Count", f"{avg_moves:.1f}")
            
            if total_solves > 1:
                st.markdown("**Move Count Trend**")
                import pandas as pd
                # Reverse history to chronological for the chart
                chronological = list(reversed(history))
                chart_data = pd.DataFrame({
                    'Moves': [r.get('move_count', 0) for r in chronological],
                    'Solve #': range(1, total_solves + 1)
                }).set_index('Solve #')
                st.line_chart(chart_data, height=200, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"**Recent Solves**")
            for i,rec in enumerate(history[:10]):
                ts=rec.get('timestamp','')[:19].replace('T',' ')
                mc=rec.get('move_count',0)
                moves_str=' '.join(rec.get('solution',[]))
                st.markdown(f"""<div class="history-row">
                    <span class="ts">🕐 {ts}</span>
                    <span class="mc">{mc} moves</span>
                </div>""", unsafe_allow_html=True)
                with st.expander(f"View solution #{i+1}"):
                    st.code(moves_str, language=None)
            if st.button("🗑️ Clear History"):
                clear_history(); st.rerun()

    # ── Footer ──
    tc = '#94A3B8'
    bc = '#334155' if st.session_state.dark_mode else '#E2E8F0'
    st.markdown(f"""<div style="text-align:center;margin-top:4rem;padding:2rem;color:{tc};font-size:0.9rem;border-top:1px solid {bc};">
        <p>Built with ❤️ using Streamlit & OpenCV · Kociemba Two-Phase Algorithm</p>
    </div>""", unsafe_allow_html=True)

if __name__=="__main__":
    run_app()
