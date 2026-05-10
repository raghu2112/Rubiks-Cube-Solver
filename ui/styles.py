# ui/styles.py — CSS for light and dark themes
def get_css(dark=False):
    bg = '#0F172A' if dark else '#F8FAFC'
    card = '#1E293B' if dark else '#FFFFFF'
    border = '#334155' if dark else '#E2E8F0'
    text = '#E2E8F0' if dark else '#1E293B'
    muted = '#94A3B8' if dark else '#64748B'
    badge_bg = '#334155' if dark else '#F1F5F9'
    badge_text = '#CBD5E1' if dark else '#334155'
    chip_bg = '#1E293B' if dark else '#FFFFFF'
    chip_n_bg = '#7F1D1D' if dark else '#FEE2E2'
    chip_n_text = '#FCA5A5' if dark else '#DC2626'
    btn_bg = '#1E293B' if dark else '#FFFFFF'
    btn_text = '#E2E8F0' if dark else '#1E293B'
    btn_border = '#475569' if dark else '#E2E8F0'
    scroll_track = '#1E293B' if dark else '#F1F5F9'
    scroll_thumb = '#475569' if dark else '#CBD5E1'
    loader_bg = '#0F172A' if dark else '#FFFFFF'
    loader_text = '#E2E8F0' if dark else '#1E293B'
    sb_bg = 'rgba(22,163,74,0.15)' if dark else 'rgba(22,163,74,0.1)'
    inset = 'rgba(255,255,255,0.05)' if dark else '#F1F5F9'
    hero_p = '#94A3B8' if dark else '#64748B'

    return f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html,body,.stApp,.stMarkdown,.stButton>button,.stSelectbox label,
[data-testid="stWidgetLabel"],[data-testid="stTab"]>button {{
    font-family:'Inter',sans-serif !important; color:{text} !important;
}}
.stApp {{ background:{bg} !important; }}
#MainMenu,footer,.stDeployButton {{ display:none !important; }}
header[data-testid="stHeader"] {{ background:transparent !important; }}

.hero {{
    text-align:center;padding:5rem 1rem;background:{card};
    border-radius:24px;box-shadow:0 10px 40px rgba(0,0,0,0.05);margin-bottom:3rem;
    border:1px solid {border};
}}
.hero h1 {{
    font-size:3.5rem;font-weight:900;margin:0;letter-spacing:-1.5px;
    background:linear-gradient(135deg,#DC2626,#F97316,#FBBF24,#16A34A,#2563EB);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    animation:gradientShift 5s ease infinite;background-size:200% auto;
}}
@keyframes gradientShift {{ 0%{{background-position:0% center}} 50%{{background-position:100% center}} 100%{{background-position:0% center}} }}
.hero p {{ font-size:1.2rem;color:{hero_p};margin-top:1rem; }}
.badges {{ display:flex;justify-content:center;gap:12px;margin-top:1.5rem;flex-wrap:wrap; }}
.badge {{ padding:8px 16px;border-radius:9999px;font-size:0.85rem;font-weight:600;
    background:{badge_bg};color:{badge_text};border:1px solid {border}; }}

.stitle {{ display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;padding-top:2rem; }}
.stitle .num {{ width:36px;height:36px;border-radius:50%;display:flex;align-items:center;
    justify-content:center;font-weight:800;font-size:1rem;color:#FFF;
    background:linear-gradient(135deg,#2563EB,#16A34A);box-shadow:0 4px 10px rgba(37,99,235,0.3); }}
.stitle span:last-child {{ font-size:1.5rem;font-weight:800;color:{text}; }}

.moves-wrap {{ display:flex;flex-wrap:wrap;gap:8px;margin-top:10px; }}
.mchip {{ display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:12px;
    font-weight:700;font-size:0.95rem;background:{chip_bg};color:{text};
    border:1px solid {border};box-shadow:0 2px 8px rgba(0,0,0,0.04);animation:chipIn 0.3s ease-out both; }}
.mchip.active {{ border-color:#DC2626;box-shadow:0 0 12px rgba(220,38,38,0.3); }}
.mchip .n {{ color:{chip_n_text};font-size:0.8rem;background:{chip_n_bg};padding:2px 6px;border-radius:6px; }}
.mchip .d {{ color:{muted};font-weight:500;font-size:0.85rem; }}
@keyframes chipIn {{ from{{opacity:0;transform:translateY(10px)}} to{{opacity:1;transform:translateY(0)}} }}

.stButton>button {{ border-radius:12px !important;font-weight:600 !important;
    transition:all 0.2s ease !important;border:1px solid {btn_border} !important;
    background:{btn_bg} !important;color:{btn_text} !important; }}
.stButton>button:hover {{ transform:translateY(-2px) !important;
    box-shadow:0 4px 12px rgba(0,0,0,0.08) !important; }}
.stButton>button[kind="primary"] {{ background:linear-gradient(135deg,#DC2626,#F97316) !important;
    color:#FFF !important;border:none !important; }}
.stButton>button[kind="primary"]:hover {{ box-shadow:0 6px 16px rgba(220,38,38,0.3) !important; }}

.stProgress>div>div {{ background:linear-gradient(90deg,#DC2626,#F97316,#FBBF24,#16A34A,#2563EB) !important; }}

[data-testid="stCameraInputWebcamComponent"] {{ position:relative !important;border-radius:16px;overflow:hidden; }}
[data-testid="stCameraInputWebcamComponent"]::after {{
    content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
    width:min(58%,240px);aspect-ratio:1/1;pointer-events:none;z-index:10;
    background:
        repeating-linear-gradient(to right,transparent,transparent calc(33.33% - 1px),
        rgba(37,99,235,0.4) calc(33.33% - 1px),rgba(37,99,235,0.4) calc(33.33% + 1px),transparent calc(33.33% + 1px)),
        repeating-linear-gradient(to bottom,transparent,transparent calc(33.33% - 1px),
        rgba(37,99,235,0.4) calc(33.33% - 1px),rgba(37,99,235,0.4) calc(33.33% + 1px),transparent calc(33.33% + 1px));
    border:3px solid rgba(37,99,235,0.8);border-radius:8px;
    box-shadow:0 0 0 9999px rgba(0,0,0,0.3);
}}

.loader-overlay {{ position:fixed;top:0;left:0;width:100vw;height:100vh;
    background:{loader_bg};z-index:9999;display:flex;flex-direction:column;
    justify-content:center;align-items:center;animation:fadeOut 0.5s ease 2.5s forwards;pointer-events:none; }}
.loader-cube {{ font-size:5rem;animation:spin 2s infinite linear; }}
.loader-text {{ margin-top:1.5rem;font-size:1.2rem;font-weight:700;color:{loader_text};
    background:linear-gradient(135deg,#DC2626,#F97316,#FBBF24,#16A34A,#2563EB);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent; }}
@keyframes spin {{ 100%{{transform:rotate(360deg)}} }}
@keyframes fadeOut {{ to{{opacity:0;visibility:hidden}} }}

::-webkit-scrollbar {{ width:8px; }}
::-webkit-scrollbar-track {{ background:{scroll_track}; }}
::-webkit-scrollbar-thumb {{ background:{scroll_thumb};border-radius:4px; }}

.conf-bar {{ height:6px;border-radius:3px;background:#E2E8F0;overflow:hidden;margin-top:2px; }}
.conf-fill {{ height:100%;border-radius:3px;transition:width 0.3s ease; }}

.step-desc {{ background:{card};border:1px solid {border};border-radius:12px;padding:1.2rem;
    margin-top:1rem;font-size:1rem; }}
.step-move {{ font-size:1.5rem;font-weight:900;color:#DC2626; }}

.sbanner {{ text-align:center;padding:2rem;border-radius:16px;
    background:{sb_bg};border:1px solid rgba(22,163,74,0.2);margin-bottom:2rem; }}
.sbanner h2 {{ margin:0;color:#16A34A;font-weight:900;font-size:2.5rem; }}
.sbanner p {{ color:{muted};margin-top:0.5rem;font-size:1.1rem; }}

.history-row {{ display:flex;justify-content:space-between;align-items:center;padding:10px 14px;
    border-radius:10px;background:{card};border:1px solid {border};margin-bottom:6px; }}
.history-row .ts {{ color:{muted};font-size:0.8rem; }}
.history-row .mc {{ font-weight:700;color:#DC2626; }}
</style>"""
