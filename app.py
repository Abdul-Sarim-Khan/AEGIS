import os, time, math, concurrent.futures
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

import streamlit as st
from google import genai
from rag_engine import RagEngine
from ui_components import (
    apply_cyber_theme,
    render_header,
    render_owasp_sidebar,
    render_scan_status_badge,
    render_pndc_performance_dashboard,
)

st.set_page_config(page_title="AEGIS-CODE", page_icon="🛡️", layout="wide")
apply_cyber_theme()

if "scan_metrics" not in st.session_state:
    st.session_state.scan_metrics = None

# ── Build RAG engine (cached) ─────────────────────────────────────────────────
@st.cache_resource(show_spinner="⚡ Building FAISS knowledge base…")
def get_engine() -> RagEngine:
    return RagEngine().build(parallel=False)

engine = get_engine()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # ── Brand mark ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.6rem 0;
        border-bottom:1px solid #0f2540;margin-bottom:1rem;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:1.8rem;
            color:#00ff99;letter-spacing:0.1em;line-height:1;">🛡️ AEGIS-CODE</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;
            color:#2a5a8a;letter-spacing:0.18em;margin-top:3px;">RAG-BASED CODE VULNERABILITY ANALYZER</div>
    </div>
    """, unsafe_allow_html=True)

    # ── API Key ─────────────────────────────────────────────────────────────
    st.markdown("#### ⚙️ Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your key here…",
        help="Free key from Google AI Studio (aistudio.google.com)",
    )
    if api_key:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:6px;
            padding:4px 8px;background:#080f1a;border:1px solid #00ff9933;
            border-radius:4px;margin-top:-4px;">
            <div style="width:6px;height:6px;border-radius:50%;
                background:#00ff99;box-shadow:0 0 6px #00ff99;"></div>
            <span style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;
                color:#00ff99;letter-spacing:0.08em;">API KEY LOADED</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Knowledge base ──────────────────────────────────────────────────────
    st.markdown("#### 📚 Knowledge Base")
    stats = engine.stats()
    c1, c2 = st.columns(2)
    with c1: st.metric("Docs",   stats["documents"])
    with c2: st.metric("Chunks", stats["chunks"])
    st.caption(f"⏱️ Index built in {stats['build_seconds']} s")

    # ── OWASP Top 10 ────────────────────────────────────────────────────────
    st.markdown("#### 🔴 OWASP Top 10 Coverage")
    render_owasp_sidebar()

    # ── Scanner config ──────────────────────────────────────────────────────
    st.markdown("#### 🎛️ Scanner Settings")
    top_k = st.slider("Rules retrieved per chunk (top-k)", 1, 5, 2)
    st.caption("Higher values = richer context, slower analysis")


# ─────────────────────────────────────────────────────────────────────────────
# ANALYZE CHUNK  (map worker)
# ─────────────────────────────────────────────────────────────────────────────
def analyze_chunk(
    chunk_id: int,
    code_chunk: str,
    engine: RagEngine,
    top_k: int,
    client: genai.Client,
) -> str:
    time.sleep(chunk_id * 1.5)
    rules_context = "\n\n".join(r.chunk.text for r in engine.search(code_chunk, top_k=top_k))
    prompt = f"""You are an expert Secure Code Reviewer. Review the following code chunk.
Only report critical security vulnerabilities. Be extremely concise. Use bullet points.
If none exist, state "No vulnerabilities found."

OWASP Guidelines:
{rules_context}

Source Code Chunk:
{code_chunk}"""
    for attempt in range(3):
        try:
            resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            return f"### Analysis of Code Chunk {chunk_id}\n{resp.text}"
        except Exception as e:
            if attempt < 2:
                time.sleep(10)
            else:
                return f"Error analyzing chunk {chunk_id} after 3 attempts: {e}"


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────
render_header()

tab_scan, tab_pndc = st.tabs(["🔒  Vulnerability Scanner", "⚡  Performance Dashboard"])

# ── TAB 1 : Scanner ──────────────────────────────────────────────────────────
with tab_scan:
    st.markdown("""
    <p style="font-family:'Exo 2',sans-serif;color:#4a6a8a;font-size:0.9rem;
        margin-bottom:1.2rem;border-left:2px solid #0f2540;padding-left:10px;">
        Upload source code or paste a snippet. AEGIS-CODE decomposes it into chunks and runs
        a concurrent Map-Reduce analysis pipeline against the OWASP Top 10 knowledge base.
    </p>
    """, unsafe_allow_html=True)

    col_upload, col_paste = st.columns([1, 1], gap="medium")
    with col_upload:
        uploaded = st.file_uploader(
            "Upload source file",
            type=["py", "js", "java", "php", "cpp", "c"],
            label_visibility="visible",
        )
    with col_paste:
        pasted = st.text_area("…or paste code directly", height=130, placeholder="// Paste code here…")

    code = ""
    if uploaded is not None:
        code = uploaded.read().decode("utf-8", errors="replace")
    elif pasted.strip():
        code = pasted

    run_btn = st.button(
        "⚡  Run Security Analysis",
        type="primary",
        disabled=not code,
        use_container_width=True,
    )

    if run_btn and code:
        if not api_key:
            st.error("⚠️  Enter your Gemini API Key in the sidebar first.")
            st.stop()

        client = genai.Client(api_key=api_key)

        # ── Code preview ─────────────────────────────────────────────────────
        with st.expander("📄 Uploaded Code Preview", expanded=False):
            st.code(code, language="python")

        code_lines     = code.splitlines()
        total_lines    = len(code_lines)
        chunk_size_ln  = max(1, math.ceil(total_lines / 2))
        code_chunks    = [
            "\n".join(code_lines[i : i + chunk_size_ln])
            for i in range(0, total_lines, chunk_size_ln)
        ]
        num_workers    = len(code_chunks)

        # ── Pipeline status ───────────────────────────────────────────────────
        st.markdown(f"""
        <div style="background:#080f1a;border:1px solid #0f2540;border-radius:6px;
            padding:0.9rem 1.2rem;margin:0.8rem 0;display:grid;
            grid-template-columns:repeat(3,1fr);gap:12px;text-align:center;">
            <div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1.4rem;color:#ffd166;">{total_lines}</div>
                <div style="font-family:'Exo 2',sans-serif;font-size:0.68rem;color:#2a5a8a;letter-spacing:0.1em;">TOTAL LINES</div>
            </div>
            <div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1.4rem;color:#4cc9f0;">{num_workers}</div>
                <div style="font-family:'Exo 2',sans-serif;font-size:0.68rem;color:#2a5a8a;letter-spacing:0.1em;">WORKER THREADS</div>
            </div>
            <div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1.4rem;color:#00ff99;">{chunk_size_ln}</div>
                <div style="font-family:'Exo 2',sans-serif;font-size:0.68rem;color:#2a5a8a;letter-spacing:0.1em;">LINES / CHUNK</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        render_scan_status_badge("Concurrent map phase initializing…", "active")

        # ── MAP Phase ─────────────────────────────────────────────────────────
        chunk_reports = []
        start_map = time.time()

        map_progress = st.progress(0, text="Map Phase — distributing chunks…")

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = {
                executor.submit(analyze_chunk, i + 1, c, engine, top_k, client): i
                for i, c in enumerate(code_chunks)
            }
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                chunk_reports.append(future.result())
                completed += 1
                pct = int((completed / num_workers) * 100)
                map_progress.progress(pct, text=f"Map Phase — {completed}/{num_workers} chunks done")

        map_progress.empty()
        map_wall = time.time() - start_map

        # ── REDUCE Phase ──────────────────────────────────────────────────────
        reports_combined = "\n\n---\n\n".join(chunk_reports)

        merge_prompt = f"""You are a Lead Security Auditor. Merge the chunk reports below into one
cohesive, professional vulnerability report. Remove duplicates, organize by OWASP category
(e.g. A03: Injection), and provide actionable mitigations in clean Markdown.

Raw Chunk Reports:
{reports_combined}"""

        final_report = ""
        start_reduce = time.time()

        with st.spinner("Reduce Phase — synthesizing final report…"):
            for attempt in range(3):
                try:
                    resp = client.models.generate_content(model="gemini-2.5-flash", contents=merge_prompt)
                    final_report = resp.text
                    break
                except Exception as e:
                    if attempt < 2:
                        time.sleep(15)
                    else:
                        st.error("⚠️  Synthesis failed — showing raw map results.")
                        final_report = (
                            "## ⚠️ Raw Analysis Reports (Synthesis Skipped)\n\n"
                            + "\n\n---\n\n".join(chunk_reports)
                        )

        reduce_wall = time.time() - start_reduce

        # ── Save metrics ──────────────────────────────────────────────────────
        waves = math.ceil(len(code_chunks) / num_workers) if num_workers > 0 else 1
        st.session_state.scan_metrics = {
            "lines":               total_lines,
            "chunk_size":          chunk_size_ln,
            "chunks":              len(code_chunks),
            "workers":             num_workers,
            "avg_map_time":        map_wall / waves if waves > 0 else 0,
            "reduce_time":         reduce_wall,
            "actual_parallel_time": map_wall + reduce_wall,
        }

        # ── Report output ─────────────────────────────────────────────────────
        render_scan_status_badge("Analysis complete", "success")
        st.markdown("""
        <div style="font-family:'Exo 2',sans-serif;font-size:0.7rem;letter-spacing:0.2em;
            color:#2a5a8a;text-transform:uppercase;border-bottom:1px solid #0f2540;
            padding-bottom:5px;margin:1.2rem 0 0.8rem 0;">🛡️ Security Audit Report</div>
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div style="background:#070e1a;border:1px solid #0f2540;border-top:2px solid #00ff99;'
            f'border-radius:6px;padding:1.5rem 1.8rem;">{final_report}</div>',
            unsafe_allow_html=True,
        )
        st.success("✅ Analysis complete — check the Performance Dashboard tab for metrics.")


# ── TAB 2 : Performance Dashboard ───────────────────────────────────────────
with tab_pndc:
    render_pndc_performance_dashboard(scan_metrics=st.session_state.scan_metrics)