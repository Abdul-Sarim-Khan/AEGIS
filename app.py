"""
app.py
======
Enhanced Streamlit Frontend for AEGIS.
Includes cleaner layouts, metrics tracker, and corrected parameter references.
"""

import streamlit as st
import concurrent.futures
import google.generativeai as genai
from rag_engine import build_engine

st.set_page_config(
    page_title="AEGIS - AI Secure Code Reviewer", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design Tweaks
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .stMetric {background-color: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;}
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Vector Database Initialization (Cached via disk binary loading)
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner="Booting Ephemeral Knowledge Base Vector DB...")
def get_engine():
    return build_engine(parallel=False)

engine = get_engine()

# --------------------------------------------------------------------------- #
# Sidebar Panel
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.title("🛡️ AEGIS Engine")
    st.markdown("---")
    
    st.subheader("🔑 Authentication")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
    st.caption("[Get an API key via Google AI Studio](https://aistudio.google.com/)")
    
    st.markdown("---")
    st.subheader("⚙️ Hyperparameters")
    top_k = st.slider("Rules retrieved per code block", 1, 5, 3)
    chunk_size_lines = st.slider("Lines per analysis window", 20, 100, 50, step=10)
    
    st.markdown("---")
    st.subheader("📊 Local Metadata")
    stats = engine.stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("OWASP Modules", stats["documents"])
    with col2:
        st.metric("Total Embeddings", stats["chunks"])
    
    st.metric("DB Boot Latency", f"{stats['build_seconds']}s")
    
    if st.button("🔄 Clear & Force Rebuild Cache"):
        build_engine(parallel=False, force_rebuild=True)
        st.rerun()

# --------------------------------------------------------------------------- #
# Thread Worker Execution Block
# --------------------------------------------------------------------------- #
def analyze_chunk(chunk_id: int, code_chunk: str, top_k: int) -> str:
    """MAP PHASE: Processes specific slices and references vectors."""
    results = engine.search(code_chunk, top_k=top_k)
    rules_context = "\n\n".join(f"[{r.chunk.source}]: {r.chunk.text}" for r in results)
    
    prompt = f"""
    You are an expert Secure Code Reviewer. Review the following code chunk.
    Only report critical security vulnerabilities. If none exist, state "No vulnerabilities found."
    
    OWASP Reference Framework Guidelines:
    {rules_context}
    
    Source Code Chunk under Review:
    {code_chunk}
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    try:
        response = model.generate_content(prompt)
        return f"### Analysis Report Window {chunk_id}\n" + response.text
    except Exception as e:
        return f"Error executing analysis on validation window {chunk_id}: {e}"

# --------------------------------------------------------------------------- #
# Target App Main Layout Space
# --------------------------------------------------------------------------- #
st.title("🛡️ AEGIS: Map-Reduce Static Code Analyzer")
st.write("Leveraging an elite Retrieval-Augmented Generation context map and concurrent computing to scan target source blocks against the OWASP framework.")

uploaded = st.file_uploader("Drop target source scripts here", type=["py", "js", "java", "php", "cpp", "c"])
pasted = st.text_area("Or input plaintext system strings directly", height=150, placeholder="def vulnerable_func()...")

code = ""
if uploaded is not None:
    code = uploaded.read().decode("utf-8", errors="replace")
elif pasted.strip():
    code = pasted

if st.button("⚡ Run Security Analysis Pipeline", type="primary", disabled=not code):
    if not api_key:
        st.error("⚠️ Authentication Key missing. Please input your Gemini API token in the panel layout context.")
        st.stop()
        
    genai.configure(api_key=api_key)
    
    # Text Token segmentation via structural Line Splits
    code_lines = code.splitlines()
    code_chunks = ["\n".join(code_lines[i:i + chunk_size_lines]) for i in range(0, len(code_lines), chunk_size_lines)]
    
    # Layout Breakdown Display
    view_col, metrics_col = st.columns([2, 1])
    
    with view_col:
        st.subheader("📁 Inspected Source Target")
        st.code(code, language="python")
        
    with metrics_col:
        st.subheader("⚡ Map-Reduce Architecture")
        st.info(f"The asset has been split into **{len(code_chunks)} distinct execution chunks** for structural parallel tracking.")
        
    st.markdown("---")
    chunk_reports = []
    
    # 1. MAP STEP (Processing elements across localized thread pool)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("Executing Map Operations: Invoking models across parallel clusters...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(code_chunks))) as executor:
        futures = {
            executor.submit(analyze_chunk, i+1, c, top_k): i 
            for i, c in enumerate(code_chunks)
        }
        
        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            chunk_reports.append(future.result())
            percent_complete = int(((idx + 1) / len(code_chunks)) * 100)
            progress_bar.progress(percent_complete)
            status_text.text(f"Processed chunks: {idx + 1}/{len(code_chunks)}")
            
    # 2. REDUCE STEP (Combining the distributed segments into an output matrix)
    with st.spinner("Executing Reduce Operations: Consolidating threat audit telemetry logs..."):
        merge_prompt = f"""
        You are a Lead Security Auditor. Merge the following chunked analysis reports into one cohesive, professional vulnerability report.
        Remove duplicates, organize by vulnerability type (e.g., A03: Injection), and provide actionable mitigations.
        
        Raw Chunk Reports:
        {"\n\n---\n\n".join(chunk_reports)}
        """
        reducer_model = genai.GenerativeModel("gemini-2.5-flash")
        final_report = reducer_model.generate_content(merge_prompt).text

    progress_bar.empty()
    status_text.empty()

    st.subheader("📋 Final Consolidated Security Audit Report")
    st.markdown(final_report)
    st.success("Static Code Map Analysis Sequence Completed successfully.")