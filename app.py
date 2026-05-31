"""
app.py
======
Streamlit frontend for the LLM-powered SAST tool.
Fully wired with Gemini API and PNDC Map-Reduce Architecture.
"""

import os
# Kill the transformers warning spam that freezes the Windows terminal
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
# Fix the HF Hub unauthenticated warning and load instantly
os.environ["HF_HUB_OFFLINE"] = "1" 

import streamlit as st
import concurrent.futures
import time
import math
from google import genai
from rag_engine import RagEngine
from ui_components import apply_cyber_theme, render_header, render_pndc_performance_dashboard

st.set_page_config(page_title="AEGIS", page_icon="🛡️", layout="wide")
apply_cyber_theme()

if "scan_metrics" not in st.session_state:
    st.session_state.scan_metrics = None

@st.cache_resource(show_spinner="Building in-memory knowledge base (FAISS)...")
def get_engine() -> RagEngine:
    return RagEngine().build(parallel=False)

engine = get_engine()

# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get a free key from Google AI Studio")
    
    st.header("📚 Knowledge Base")
    stats = engine.stats()
    st.metric("OWASP documents", stats["documents"])
    st.metric("Vector chunks", stats["chunks"])
    st.caption(f"Index build time: {stats['build_seconds']} s")
    top_k = st.slider("Rules to retrieve per code chunk (top-k)", 1, 5, 2)

# --------------------------------------------------------------------------- #
# PNDC: Map-Reduce Worker Function
# --------------------------------------------------------------------------- #
def analyze_chunk(chunk_id: int, code_chunk: str, engine: RagEngine, top_k: int, client: genai.Client) -> str:
    """MAP PHASE: Retrieves specific rules for a code chunk and asks LLM to analyze it."""
    
    # Micro-delay to stagger thread requests and avoid instant 429 Rate Limits
    time.sleep(chunk_id * 1.5) 
    
    results = engine.search(code_chunk, top_k=top_k)
    rules_context = "\n\n".join(r.chunk.text for r in results)
    
    # Prompt is instructed to be highly concise to save tokens for the Reduce phase
    prompt = f"""
    You are an expert Secure Code Reviewer. Review the following code chunk.
    Only report critical security vulnerabilities. Be extremely concise. Use bullet points.
    If none exist, state "No vulnerabilities found."
    
    OWASP Guidelines to follow:
    {rules_context}
    
    Source Code Chunk:
    {code_chunk}
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
            )
            return f"### Analysis of Code Chunk {chunk_id}\n" + response.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(10) # 10 second backoff if we hit a rate limit
                continue
            return f"Error analyzing chunk {chunk_id} after {max_retries} attempts: {e}"

# --------------------------------------------------------------------------- #
# Main UI
# --------------------------------------------------------------------------- #
render_header()

tab_scan, tab_pndc = st.tabs(["🔒 Vulnerability Scanner", "⚡ PNDC Performance Dashboard"])

with tab_scan:
    st.write("Upload source code. The system uses a Map-Reduce pipeline to concurrently analyze chunks of code against the OWASP Top 10.")

    uploaded = st.file_uploader("Upload a source file", type=["py", "js", "java", "php", "cpp", "c"])
    pasted = st.text_area("…or paste code here", height=150)

    code = ""
    if uploaded is not None:
        code = uploaded.read().decode("utf-8", errors="replace")
    elif pasted.strip():
        code = pasted

    analyze = st.button("Run Security Analysis", type="primary", disabled=not code)

    if analyze and code:
        if not api_key:
            st.error("⚠️ Please enter your Gemini API Key in the sidebar to proceed.")
            st.stop()
            
        client = genai.Client(api_key=api_key)
        
        st.subheader("Uploaded Code")
        st.code(code, language="python")

        # --- PNDC Pipeline Start ---
        code_lines = code.splitlines()
        # MASSIVE CHUNKS: Reduces total API requests. A 1500 line file becomes just 2 requests.
        chunk_size_lines = 800 
        code_chunks = ["\n".join(code_lines[i:i + chunk_size_lines]) for i in range(0, len(code_lines), chunk_size_lines)]
        
        total_code_lines = len(code_lines)
        num_workers = min(len(code_chunks), 3) # Max 3 workers to respect free tier
        
        st.info(f"⚡ PNDC Architecture: Code split into {len(code_chunks)} massive chunks for map-reduce processing.")
        
        chunk_reports = []
        
        # 2. MAP PHASE
        start_map_time = time.time()
        with st.spinner("Map Phase: Analyzing code chunks concurrently..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = {
                    executor.submit(analyze_chunk, i+1, c, engine, top_k, client): i 
                    for i, c in enumerate(code_chunks)
                }
                for future in concurrent.futures.as_completed(futures):
                    chunk_reports.append(future.result())
        end_map_time = time.time()
        map_wall_time = end_map_time - start_map_time

        # --- EXPLICIT RATE LIMIT COOLDOWN FOR FREE TIER ---
        st.warning("⏱️ API Rate Limit Protection: Initiating 20-second cooldown before Reduce Phase synthesis...")
        cooldown_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.2) # Total 20 seconds
            cooldown_bar.progress(i + 1)
        cooldown_bar.empty()

        # 3. REDUCE PHASE
        start_reduce_time = time.time()
        with st.spinner("Reduce Phase: Synthesizing final vulnerability report..."):
            merge_prompt = f"""
            You are a Lead Security Auditor. Merge the following chunked analysis reports into one cohesive, professional vulnerability report.
            Remove duplicates, organize by vulnerability type (e.g., A03: Injection), and provide actionable mitigations.
            Keep the synthesis concise and professional.
            
            Raw Chunk Reports:
            {"\n\n---\n\n".join(chunk_reports)}
            """
            
            max_retries = 3
            final_report = ""
            for attempt in range(max_retries):
                try:
                    final_response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=merge_prompt,
                    )
                    final_report = final_response.text
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(15) # Heavy 15-second backoff for synthesis failure
                    else:
                        st.error("⚠️ Google API Reduce Synthesis overloaded. Falling back to un-synthesized raw Map reports.")
                        final_report = "## ⚠️ Raw Analysis Reports (Synthesis Skipped)\n\n" 
                        final_report += "The API could not synthesize this massive amount of vulnerabilities due to Free Tier limits. Below are the raw concurrent Map results:\n\n"
                        final_report += "\n\n---\n\n".join(chunk_reports)

        end_reduce_time = time.time()
        reduce_wall_time = end_reduce_time - start_reduce_time
        
        waves = math.ceil(len(code_chunks) / num_workers) if num_workers > 0 else 1
        avg_map_time_per_chunk = map_wall_time / waves if waves > 0 else 0

        st.session_state.scan_metrics = {
            "lines": total_code_lines,
            "chunk_size": chunk_size_lines,
            "chunks": len(code_chunks),
            "workers": num_workers,
            "avg_map_time": avg_map_time_per_chunk,
            "reduce_time": reduce_wall_time,
            "actual_parallel_time": map_wall_time + reduce_wall_time
        }

        st.subheader("🛡️ Final Security Audit Report")
        st.markdown(final_report)
        st.success("Analysis Complete! Head to the PNDC Dashboard tab to view the mathematical breakdown.")

# --------------------------------------------------------------------------- #
# The PNDC Mathematical Proof Dashboard Tab
# --------------------------------------------------------------------------- #
with tab_pndc:
    render_pndc_performance_dashboard(scan_metrics=st.session_state.scan_metrics)