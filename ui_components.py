import streamlit as st
import math
import pandas as pd

# ─── OWASP TOP 10 DATA ────────────────────────────────────────────────────────
OWASP_TOP_10 = [
    {"id": "A01", "name": "Broken Access Control",    "icon": "🔓", "color": "#ff4d4d"},
    {"id": "A02", "name": "Cryptographic Failures",   "icon": "🔑", "color": "#ff8c42"},
    {"id": "A03", "name": "Injection",                "icon": "💉", "color": "#ffd166"},
    {"id": "A04", "name": "Insecure Design",          "icon": "🏗️", "color": "#06d6a0"},
    {"id": "A05", "name": "Security Misconfiguration","icon": "⚙️", "color": "#118ab2"},
    {"id": "A06", "name": "Vulnerable Components",    "icon": "📦", "color": "#7b2d8b"},
    {"id": "A07", "name": "Auth Failures",            "icon": "🔐", "color": "#ef476f"},
    {"id": "A08", "name": "Data Integrity Failures",  "icon": "🧬", "color": "#26c485"},
    {"id": "A09", "name": "Logging Failures",         "icon": "📋", "color": "#4cc9f0"},
    {"id": "A10", "name": "SSRF",                     "icon": "🌐", "color": "#f72585"},
]


def apply_cyber_theme():
    st.markdown("""
    <style>
    /* Import required fonts including Material Icons for Streamlit components */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    /* ── Reset & Base Layout ────────────────────────────────────── */
    #MainMenu, footer { visibility: hidden; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #060b14 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1120 0%, #060b14 100%) !important;
        border-right: 1px solid #0f2540 !important;
    }
    [data-testid="stSidebar"] * { font-family: 'Exo 2', sans-serif !important; }

    /* Fix broken text rendering on native Streamlit chevron targets */
    [data-testid="stSidebarCollapseButton"] span, 
    [data-testid="stHeader"] span {
        font-family: 'Material Icons' !important;
    }

    /* ── Cyber Toggle Buttons ───────────────────────────────────── */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stHeader"] button {
        color: #00ff99 !important;
        background-color: #0a1828 !important;
        border: 1px solid #0f3060 !important;
        border-radius: 4px !important;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stHeader"] button:hover {
        border-color: #00ff99 !important;
        background-color: #0f2540 !important;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.3) !important;
    }

    /* ── Scanline overlay ──────────────────────────────────────── */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 153, 0.012) 2px,
            rgba(0, 255, 153, 0.012) 4px
        );
        pointer-events: none;
        z-index: 9999;
    }

    /* ── Typography & Markdown ──────────────────────────────────── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        font-family: 'Exo 2', sans-serif !important;
        color: #a8c0d6 !important;
    }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        font-family: 'Exo 2', sans-serif !important;
        color: #e0f0ff !important;
    }

    .main .block-container {
        padding-top: 2.5rem !important;
        max-width: 1200px !important;
    }

    /* ── Sidebar Typography Headers ─────────────────────────────── */
    [data-testid="stSidebar"] h4 {
        color: #00ff99 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid #0f2540 !important;
        padding-bottom: 5px !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
    }

    /* ── Control Inputs & Form Elements ──────────────────────────── */
    [data-testid="stTextInput"] input {
        background: #0a1828 !important;
        border: 1px solid #0f3060 !important;
        color: #00ff99 !important;
        font-family: 'Share Tech Mono', monospace !important;
        border-radius: 4px !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #00ff99 !important;
        box-shadow: 0 0 10px rgba(0,255,153,0.2) !important;
    }

    [data-testid="stSlider"] .stSlider > div > div > div {
        background: #00ff99 !important;
    }

    [data-testid="stFileUploader"] {
        background: #0a1220 !important;
        border: 1px dashed #1a3a5c !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #00ff99 !important;
        background: #091825 !important;
    }

    [data-testid="stTextArea"] textarea {
        background: #080f1a !important;
        border: 1px solid #0f2540 !important;
        color: #a8c0d6 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.85rem !important;
        border-radius: 4px !important;
    }

    /* ── Buttons ────────────────────────────────────────────────── */
    div.stButton > button[kind="primary"] {
        background: transparent !important;
        border: 1px solid #00ff99 !important;
        color: #00ff99 !important;
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        margin-top: 0.5rem;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #00ff99 !important;
        color: #060b14 !important;
        box-shadow: 0 0 20px rgba(0,255,153,0.4) !important;
    }

    /* ── Tabs Style Correction ──────────────────────────────────── */
    [data-testid="stTabs"] [role="tab"] {
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 600 !important;
        color: #4a6a8a !important;
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: #00ff99 !important;
    }
    [data-testid="stTabs"] [role="tablist"] {
        border-bottom: 1px solid #0f2540 !important;
    }

    /* ── Cyber Metrics & Indicators ──────────────────────────────── */
    [data-testid="stMetric"] {
        background: #080f1a !important;
        border: 1px solid #0f2540 !important;
        border-radius: 6px !important;
    }
    [data-testid="stMetric"]:hover {
        border-color: #00ff99 !important;
    }
    [data-testid="stMetricLabel"] > div {
        color: #4a6a8a !important;
        font-size: 0.72rem !important;
    }
    [data-testid="stMetricValue"] > div {
        color: #00ff99 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* ── Grid Layout Components ─────────────────────────────────── */
    .owasp-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin: 8px 0;
    }
    .owasp-pill {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 8px;
        border-radius: 5px;
        background: #0a1828;
        border: 1px solid #0f2540;
    }
    .owasp-pill:hover {
        background: #0d1f35;
        border-color: #2a5a8a;
    }
    .owasp-pill-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .owasp-pill-id {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: #00ff99;
    }
    .owasp-pill-name {
        font-family: 'Exo 2', sans-serif;
        font-size: 0.65rem;
        color: #a8c0d6;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Radar/Ping Animations */
    @keyframes pulse-radar {
        0% { transform: scale(0.95); opacity: 1; box-shadow: 0 0 0 0 rgba(0, 255, 153, 0.7); }
        70% { transform: scale(1); opacity: 0.8; box-shadow: 0 0 0 6px rgba(0, 255, 153, 0); }
        100% { transform: scale(0.95); opacity: 1; box-shadow: 0 0 0 0 rgba(0, 255, 153, 0); }
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <style>
    .aegis-header {
        padding: 0.5rem 0 1rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #0f2540;
    }
    .aegis-title-row {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .aegis-pulse-ring {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #00ff99;
        box-shadow: 0 0 10px #00ff99;
        animation: pulse-radar 1.8s infinite;
    }
    .aegis-title {
        font-family: 'Exo 2', sans-serif;
        font-weight: 900;
        font-size: 2.2rem;
        color: #e8f4ff;
        letter-spacing: 0.05em;
        margin: 0 !important;
        line-height: 1;
    }
    .aegis-title span {
        color: #00ff99;
    }

    .aegis-sub {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: #4a6a8a;
        letter-spacing: 0.16em;
        margin-top: 6px !important;
        text-transform: uppercase;
    }
    .aegis-sub .blink {
        color: #00ff99;
        animation: blink 1.2s step-end infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }
    </style>

    <div class="aegis-header">
        <div class="aegis-title-row">
            <div class="aegis-pulse-ring"></div>
            <h1 class="aegis-title"><span>AEGIS-CODE</span></h1>
        </div>
        <p class="aegis-sub">Adaptive · Engine · Guard · Intelligence · Scanner <span class="blink">_</span></p>
    </div>
    """, unsafe_allow_html=True)


def render_owasp_sidebar():
    """Renders compact OWASP Top 10 pill cards in the sidebar."""
    pills_html = '<div class="owasp-grid">'
    for item in OWASP_TOP_10:
        pills_html += f"""
        <div class="owasp-pill" title="{item['name']}">
            <div class="owasp-pill-dot" style="background:{item['color']};box-shadow:0 0 6px {item['color']};"></div>
            <span class="owasp-pill-id">{item['id']}</span>
            <span class="owasp-pill-name">{item['name']}</span>
        </div>"""
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)


def render_scan_status_badge(text: str, kind: str = "active"):
    """Renders a live status badge."""
    colors = {
        "active":  ("#00ff99", "SCANNING"),
        "idle":    ("#4cc9f0", "STANDBY"),
        "error":   ("#ff4d4d", "ERROR"),
        "success": ("#00ff99", "COMPLETE"),
    }
    col, label = colors.get(kind, ("#4a6a8a", "UNKNOWN"))
    st.markdown(f"""
    <div style="display:inline-flex;align-items:center;gap:8px;
        background:#080f1a;border:1px solid {col}33;border-radius:4px;
        padding:5px 12px;margin:8px 0;">
        <div style="width:6px;height:6px;border-radius:50%;background:{col};
            box-shadow:0 0 8px {col};"></div>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;
            color:{col};letter-spacing:0.1em;">{label} — {text}</span>
    </div>
    """, unsafe_allow_html=True)


def render_pndc_performance_dashboard(scan_metrics=None):
    st.markdown("""
    <style>
    .dash-section-head {
        font-family: 'Exo 2', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.22em;
        color: #4a6a8a;
        text-transform: uppercase;
        margin: 1.8rem 0 0.8rem 0;
        border-bottom: 1px solid #0f2540;
        padding-bottom: 5px;
    }
    .speedup-hero {
        background: #040810;
        border: 1px solid #00ff99;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        box-shadow: 0 0 25px rgba(0,255,153,0.05);
    }
    .speedup-number {
        font-family: 'Share Tech Mono', monospace;
        font-size: 3.2rem;
        color: #00ff99;
        line-height: 1;
    }
    .speedup-label {
        font-family: 'Exo 2', sans-serif;
        font-size: 0.75rem;
        color: #4a6a8a;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="dash-section-head">Mathematical Validation — AEGIS Map-Reduce Pipeline</p>', unsafe_allow_html=True)

    mode = st.radio(
        "Dashboard Mode",
        ["📡 Live Scan Results", "🔬 Scalability Simulator"],
        horizontal=True,
    )

    if mode == "🔬 Scalability Simulator":
        st.markdown('<p class="dash-section-head">Simulator Parameters</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            lines = st.slider("Lines of Code (L)", 50, 20000, 5000, 50)
        with c2:
            chunk_size = st.slider("Chunk Size (C)", 10, 500, 150, 10)
        with c3:
            workers = st.slider("Worker Threads (P)", 1, 16, 5, 1)

        c4, c5 = st.columns(2)
        with c4:
            map_time = st.number_input("Map Task Time / chunk (s)", 0.5, 10.0, 3.0, 0.5)
        with c5:
            reduce_time = st.number_input("Reduce Phase Time (s)", 1.0, 20.0, 5.0, 1.0)

        total_chunks = math.ceil(lines / chunk_size)
        ts = (total_chunks * map_time) + reduce_time
        waves = math.ceil(total_chunks / workers) if workers > 0 else 1
        tp = (waves * map_time) + reduce_time + 1.0

    else:
        if not scan_metrics:
            st.markdown("""
            <div style="background:#080f1a;border:1px dashed #0f2540;border-radius:8px;
                padding:2rem;text-align:center;margin-top:1rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">📡</div>
                <p style="font-family:'Exo 2',sans-serif;color:#2a5a8a;font-size:0.9rem;
                    letter-spacing:0.05em;">Awaiting scan data — run a scan in the Vulnerability Scanner tab first.</p>
            </div>
            """, unsafe_allow_html=True)
            return

        lines      = scan_metrics["lines"]
        chunk_size = scan_metrics["chunk_size"]
        workers    = scan_metrics["workers"]
        map_time   = scan_metrics["avg_map_time"]
        reduce_time= scan_metrics["reduce_time"]
        actual_time= scan_metrics["actual_parallel_time"]
        total_chunks = scan_metrics["chunks"]
        ts = (total_chunks * map_time) + reduce_time
        tp = actual_time

        st.markdown(f"""
        <div style="background:#080f1a;border:1px solid #00ff9933;border-radius:6px;
            padding:0.9rem 1.2rem;margin-bottom:0.8rem;display:flex;align-items:center;gap:10px;">
            <div style="width:8px;height:8px;border-radius:50%;background:#00ff99;
                box-shadow:0 0 8px #00ff99;"></div>
            <span style="font-family:'Exo 2',sans-serif;color:#a8c0d6;font-size:0.9rem;">
                Analyzed <strong style="color:#00ff99;">{lines} lines</strong> across
                <strong style="color:#4cc9f0;">{total_chunks} chunks</strong> in
                <strong style="color:#00ff99;">{actual_time:.2f}s</strong>
                using <strong style="color:#ffd166;">{workers} concurrent workers</strong>
            </span>
        </div>
        """, unsafe_allow_html=True)

    # ── Derived metrics ─────────────────────────────────────────────────────
    speedup  = ts / tp if tp > 0 else 1
    total_map_work = total_chunks * map_time
    f = total_map_work / ts if ts > 0 else 0
    s = 1.0 - f
    amdahl  = 1.0 / (s + (f / workers)) if workers > 0 else 1
    efficiency = (speedup / workers) * 100 if workers > 0 else 0

    # ── Hero speedup ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="speedup-hero">
        <div class="speedup-number">{speedup:.2f}×</div>
        <div class="speedup-label">Empirical Speedup  ·  S = T<sub>s</sub> / T<sub>p</sub></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Core metric cards ────────────────────────────────────────────────────
    st.markdown('<p class="dash-section-head">System Metrics</p>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Chunks (N)",          f"{total_chunks}")
    with m2: st.metric("Serial Time Tₛ",      f"{ts:.2f}s",       delta="baseline",         delta_color="off")
    with m3: st.metric("Parallel Time Tₚ",    f"{tp:.2f}s",       delta=f"−{ts-tp:.1f}s",   delta_color="normal")
    with m4: st.metric("Core Efficiency (E)", f"{efficiency:.1f}%")

    # ── Amdahl's Law ─────────────────────────────────────────────────────────
    st.markdown('<p class="dash-section-head">Amdahl\'s Law Breakdown</p>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    with a1: st.metric("Parallel Fraction (f)", f"{f*100:.1f}%")
    with a2: st.metric("Serial Fraction (s)",   f"{s*100:.1f}%")
    with a3: st.metric("Theoretical Max Speedup", f"{amdahl:.2f}×")

    # ── Charts ───────────────────────────────────────────────────────────────
    st.markdown('<p class="dash-section-head">Visual Analysis</p>', unsafe_allow_html=True)
    ch1, ch2 = st.columns([2, 1])
    with ch1:
        st.caption("**Execution Time Comparison** — Lower is Better")
        chart_df = pd.DataFrame({
            "Mode": ["Sequential Tₛ", "Parallel Tₚ"],
            "Time (s)": [round(ts, 2), round(tp, 2)]
        })
        st.bar_chart(chart_df, x="Mode", y="Time (s)", height=260, color="#00ff99")

    with ch2:
        st.caption("**Core Efficiency**")
        st.markdown(f"""
        <div class="speedup-hero" style="margin-top:0.2rem;">
            <div class="speedup-number" style="font-size:2rem;">{efficiency:.0f}%</div>
            <div class="speedup-label">utilization</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(max(int(efficiency), 0), 100))
        st.caption(f"Amdahl ceiling: **{amdahl:.2f}×** with {workers} workers")

    # ── Formal derivations ────────────────────────────────────────────────────
    with st.expander("📐 Formal Mathematical Derivations"):
        st.markdown('<div class="formula-label">1 · Task Decomposition</div>', unsafe_allow_html=True)
        st.latex(r"N = \left\lceil \frac{L}{C} \right\rceil")
        st.markdown('<div class="formula-label">2 · Time Complexity Models</div>', unsafe_allow_html=True)
        st.latex(r"T_s = (N \times t_{map}) + t_{reduce}")
        st.latex(r"T_p = \left(\left\lceil \frac{N}{P} \right\rceil \times t_{map}\right) + t_{reduce} + \mathcal{O}")
        st.markdown('<div class="formula-label">3 · Amdahl\'s Law</div>', unsafe_allow_html=True)
        st.latex(r"S_{max} = \frac{1}{s + \frac{f}{P}}")
        st.markdown('<div class="formula-label">4 · Efficiency</div>', unsafe_allow_html=True)
        st.latex(r"E = \frac{S}{P} \times 100\%")