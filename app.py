"""
app.py
======
ClusterScan AI Frontend Dashboard.
Built using isolated component fragments, asynchronous thread management, and custom CSS theme layouts.
"""

import streamlit as st
import concurrent.futures
import google.generativeai as genai
from rag_engine import build_engine

# --- Core Matrix Dashboard Configurations ---
st.set_page_config(
    page_title="ClusterScan AI // THREAT MATRIX CONTROL", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Cyberpunk Dark Mode Palette Injection ---
st.markdown("""
    <style>
    /* Global Workspace Layout Customization */
    .block-container {padding-top: 1.5rem; padding-bottom: 1.5rem; max-width: 95%;}
    
    /* Sidebar Layout Custom Styling overrides */
    section[data-testid="stSidebar"] {
        background-color: #060b13 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Telemetry Visual Cards Grid */
    .telemetry-card {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #1e293b;
        border-left: 5px solid #00FFC2;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
    }
    .stat-val {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        color: #00FFC2;
        text-shadow: 0 0 10px rgba(0, 255, 194, 0.2);
    }
    
    /* Interactive Terminal Window Elements */
    .terminal-header {
        background-color: #1e293b;
        color: #94a3b8;
        font-family: monospace;
        padding: 6px 12px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        border-bottom: 2px solid #0f172a;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
    }
    .terminal-body {
        background-color: #020617;
        border: 1px solid #1e293b;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    /* Status Badge Matrix */
    .phase-badge {
        background-color: #1e1b4b;
        color: #818cf8;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        border: 1px solid #4338ca;
    }
    </style>
""", unsafe_allow_html=True)

# --- Ephemeral Vector Database Context Ingestion ---
@st.cache_resource(show_spinner=False)
def get_engine():
    return build_engine(parallel=False)

engine = get_engine()
stats = engine.stats()

# --------------------------------------------------------------------------- #
# ENHANCED CONTROL PANEL SIDEBAR
# --------------------------------------------------------------------------- #
with st.sidebar:
    # App Branding Block
    st.markdown("""
        <div style="text-align: center; padding: 10px 0px 20px 0px;">
            <span style="font-size: 2rem; font-weight: 800; letter-spacing: 2px; color: #ffffff;">🛡️ CLUSTERSCAN AI</span><br>
            <span style="font-size: 0.72rem; color: #38bdf8; font-family: monospace; letter-spacing: 1px;">PARALLEL CLOUD CODE AUDITOR</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. API Credentials Management Panel
    st.markdown("### 🔑 CREDENTIAL MANAGER")
    api_key = st.text_input(
        "Gemini API Gateway Access Token", 
        type="password", 
        placeholder="AIzaSy...",
        label_visibility="collapsed"
    )
    st.caption("🔒 Tokens are isolated securely in localized execution memory variables.")
    st.markdown("---")
    
    # 2. Pipeline Controls
    st.markdown("### 🎛️ ENGINE HYPERPARAMETERS")
    with st.container(border=True):
        top_k = st.slider("Vector Context Retrieval Depth (Top-K)", 1, 5, 3, 
                          help="Number of background OWASP context fragments bound to each thread execution context.")
        chunk_size_lines = st.slider("Map Thread Scan Volume (Lines)", 20, 100, 50, step=10,
                          help="Specifies code line segmentation parameters assigned per thread task execution.")
    st.markdown("---")
    
    # 3. Local Hardware and Matrix Analytics Cards
    st.markdown("### 📊 VECTOR DB MATRIX STATS")
    st.markdown(f"""
        <div class="telemetry-card" style="border-left-color: #38bdf8;">
            <div style="color: #64748b; font-size: 0.75rem; font-weight: bold; letter-spacing: 0.5px;">KNOWLEDGE MODULES INGESTED</div>
            <div class="stat-val" style="color: #38bdf8;">{stats["documents"]} <span style="font-size:1rem; color:#64748b;">Frameworks</span></div>
        </div>
        <div class="telemetry-card" style="border-left-color: #a855f7;">
            <div style="color: #64748b; font-size: 0.75rem; font-weight: bold; letter-spacing: 0.5px;">COMPILED VECTOR EMBEDDINGS</div>
            <div class="stat-val" style="color: #a855f7;">{stats["chunks"]} <span style="font-size:1rem; color:#64748b;">Nodes</span></div>
        </div>
        <div class="telemetry-card" style="border-left-color: #e2e8f0;">
            <div style="color: #64748b; font-size: 0.75rem; font-weight: bold; letter-spacing: 0.5px;">FAISS FILE INDEX DISK LATENCY</div>
            <div class="stat-val" style="font-size: 1.5rem; color: #e2e8f0;">{stats["build_seconds"]} <span style="font-size:1rem; color:#64748b;">seconds</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Purge System Cache & Re-Index", use_container_width=True):
        build_engine(parallel=False, force_rebuild=True)
        st.rerun()

# --------------------------------------------------------------------------- #
# CONCURRENT THREAD WORKER PROCESSING ROUTINE
# --------------------------------------------------------------------------- #
def analyze_chunk(chunk_id: int, code_chunk: str, top_k: int) -> str:
    """MAP PHASE: Processes specific slices and cross-references vector storage targets."""
    results = engine.search(code_chunk, top_k=top_k)
    rules_context = "\n\n".join(f"[{r.chunk.source}]: {r.chunk.text}" for r in results)
    
    prompt = f"""
    You are an expert Secure Code Reviewer. Review the following code chunk.
    Only report critical security vulnerabilities. If none exist, state "No vulnerabilities found."
    
    OWASP Guidelines to follow:
    {rules_context}
    
    Source Code Chunk under Review:
    {code_chunk}
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(prompt)
        return f"### Analysis of Code Chunk {chunk_id}\n" + response.text
    except Exception as e:
        return f"Error analyzing chunk {chunk_id}: {e}"

# --------------------------------------------------------------------------- #
# MAIN DASHBOARD INTERACTIVE AREA
# --------------------------------------------------------------------------- #
st.markdown("""
    <div style="margin-bottom: 25px;">
        <h1 style="font-weight: 800; font-size: 2.3rem; margin-bottom: 0px;">🛡️ CLUSTERSCAN AI // OPERATIONAL SECURITY HUB</h1>
        <p style="color: #64748b; font-size: 1.02rem;">Distributed Map-Reduce Processing // Concurrent Threat Ingestion Pipeline</p>
    </div>
""", unsafe_allow_html=True)

# Application Main Content Split Grid
col_workspace, col_telemetry = st.columns([5, 3], gap="large")

with col_workspace:
    st.markdown("### 🛠️ TARGET SOURCE SELECTION")
    tabs = st.tabs(["📁 Local Script Asset Ingestion", "📝 Live Code Text Input Workspace"])
    
    with tabs[0]:
        uploaded = st.file_uploader("Drop target raw system validation scripts", type=["py", "js", "java", "php", "cpp", "c"], label_visibility="collapsed")
    with tabs[1]:
        pasted = st.text_area("Direct String Data Input Buffer Area", height=180, placeholder="def active_endpoint_handler(request):\n    ...", label_visibility="collapsed")

    code = ""
    if uploaded is not None:
        code = uploaded.read().decode("utf-8", errors="replace")
    elif pasted.strip():
        code = pasted

with col_telemetry:
    st.markdown("### ⚡ LIVE PIPELINE METRICS")
    if code:
        code_lines = code.splitlines()
        total_chunks = -(-len(code_lines) // chunk_size_lines)
        
        st.markdown(f"""
            <div class="telemetry-card" style="border-left-color: #00FFC2; margin-bottom: 10px;">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: bold;">TOTAL INTEGRATED COMPONENT LINE COUNT</div>
                <div style="font-size: 1.8rem; font-family: monospace; font-weight: bold; color: #ffffff;">{len(code_lines)} <span style="font-size:1rem; color:#64748b;">Lines</span></div>
            </div>
            <div class="telemetry-card" style="border-left-color: #f59e0b; margin-bottom: 10px;">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: bold;">CONCURRENT WORKER BALANCING SLOTS</div>
                <div style="font-size: 1.8rem; font-family: monospace; font-weight: bold; color: #ffffff;">{total_chunks} <span style="font-size:1rem; color:#64748b;">Map Nodes</span></div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Awaiting file payload upload to build target telemetry profiles.")

# --------------------------------------------------------------------------- #
# ISOLATED GRAPHICAL FRAGMENT COMPILATION LAYER
# --------------------------------------------------------------------------- #
@st.fragment
def run_analysis_pipeline(source_code: str, line_limit: int, rule_matches: int):
    st.markdown("---")
    
    if st.button("⚡ INITIATE HIGH-THROUGHPUT SYSTEM AUDIT", type="primary", use_container_width=True):
        if not api_key:
            st.error("💥 PIPELINE ABORTED: Missing key parameters. Configure authentication strings inside the Credential Manager side panel.")
            return
            
        genai.configure(api_key=api_key)
        
        lines = source_code.splitlines()
        chunks = ["\n".join(lines[i:i + line_limit]) for i in range(0, len(lines), line_limit)]
        
        st.markdown("### 📡 PIPELINE REAL-TIME LOG BUFFER FEED")
        
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        chunk_reports = []
        
        # 1. PARALLEL COMPILATION MAP STEP
        with status_placeholder.container():
            st.markdown("""
                <div class="terminal-header"><span>BUFFER LOG PATH // MAP_CLUSTER_INVOCATION</span><span class="phase-badge">MAP PHASE ACTIVE</span></div>
                <div class="terminal-body"><code style="color: #38bdf8;">[SYSTEM INFO] Deploying Map Workers. Initializing concurrent thread allocation pool...</code></div>
            """, unsafe_allow_html=True)
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(chunks))) as executor:
            futures = {
                executor.submit(analyze_chunk, i+1, chunk, rule_matches): i 
                for i, chunk in enumerate(chunks)
            }
            
            for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                chunk_reports.append(future.result())
                percent_complete = int(((idx + 1) / len(chunks)) * 100)
                progress_bar.progress(percent_complete)
                
                with status_placeholder.container():
                    st.markdown(f"""
                        <div class="terminal-header"><span>BUFFER LOG PATH // MAP_CLUSTER_INVOCATION</span><span class="phase-badge">MAP PHASE ACTIVE</span></div>
                        <div class="terminal-body">
                            <code style="color: #38bdf8;">[SYSTEM INFO] Processing parallel segments...</code><br>
                            <code style="color: #00FFC2;">[TELEMETRY] Successfully compiled data module response block tasks: {idx + 1} of {len(chunks)}</code>
                        </div>
                    """, unsafe_allow_html=True)

        # 2. REDUCE COMBINATION STEP
        with status_placeholder.container():
            st.markdown("""
                <div class="terminal-header"><span>BUFFER LOG PATH // REDUCE_SYNTHESIS_ENGINE</span><span class="phase-badge" style="background-color:#7c2d12; color:#fdba74; border-color:#b45309;">REDUCE PHASE ACTIVE</span></div>
                <div class="terminal-body"><code style="color: #f59e0b;">[SYSTEM WARNING] All parallel worker fragments joined. Executing synthesis schemas to format vulnerabilities...</code></div>
            """, unsafe_allow_html=True)
            
        merge_prompt = f"""
        You are a Lead Security Auditor. Merge the following chunked analysis reports into one cohesive, professional vulnerability report.
        Remove duplicates, organize by vulnerability type (e.g., A03: Injection), and provide actionable mitigations.
        
        Raw Chunk Reports:
        {"\n\n---\n\n".join(chunk_reports)}
        """
        
        reducer_model = genai.GenerativeModel("gemini-2.5-flash")
        try:
            final_report = reducer_model.generate_content(merge_prompt).text
            
            progress_bar.empty()
            status_placeholder.empty()
            
            st.toast("Static scanning execution pipeline completed successfully!", icon="🛡️")
            st.markdown("### 📋 CONSOLIDATED SYSTEM RISK AUDIT REPORT")
            
            view_left, view_right = st.columns([1, 1], gap="medium")
            
            with view_left:
                with st.expander("🔍 INSPECT INGESTED ASSET RAW CODES", expanded=False):
                    st.code(source_code, language="python")
                    
            with view_right:
                with st.expander("🛠️ INSPECT INDIVIDUAL MAP WORKER SCHEMAS", expanded=False):
                    for idx, report in enumerate(chunk_reports):
                        st.markdown(f"#### Fragment Analysis Window {idx + 1}")
                        st.info(report)
                        st.markdown("---")
            
            st.markdown("""<div style="background-color: #090d16; border: 1px solid #1e293b; padding: 25px; border-radius: 8px;">""", unsafe_allow_html=True)
            st.markdown(final_report)
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Failed parsing consolidation logic payload: {e}")

if code:
    run_analysis_pipeline(code, chunk_size_lines, top_k)