"""
app.py
======
Streamlit frontend for the LLM-powered SAST tool.
Fully wired with Gemini API and PNDC Map-Reduce Architecture.
"""

import streamlit as st
import concurrent.futures
import google.generativeai as genai
from rag_engine import RagEngine

st.set_page_config(page_title="AEGIS", page_icon="🛡️", layout="wide")

# --------------------------------------------------------------------------- #
# Build the ephemeral vector DB once and cache it for the session.
# --------------------------------------------------------------------------- #
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
def analyze_chunk(chunk_id: int, code_chunk: str, engine: RagEngine, top_k: int) -> str:
    """MAP PHASE: Retrieves specific rules for a code chunk and asks LLM to analyze it."""
    # 1. Retrieve RAG context specifically for this chunk
    results = engine.search(code_chunk, top_k=top_k)
    rules_context = "\n\n".join(r.chunk.text for r in results)
    
    # 2. Call LLM
    prompt = f"""
    You are an expert Secure Code Reviewer. Review the following code chunk.
    Only report critical security vulnerabilities. If none exist, state "No vulnerabilities found."
    
    OWASP Guidelines to follow:
    {rules_context}
    
    Source Code Chunk:
    {code_chunk}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return f"### Analysis of Code Chunk {chunk_id}\n" + response.text
    except Exception as e:
        return f"Error analyzing chunk {chunk_id}: {e}"

# --------------------------------------------------------------------------- #
# Main UI
# --------------------------------------------------------------------------- #
st.title("🛡️ AEGIS")
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
        
    genai.configure(api_key=api_key)
    
    st.subheader("Uploaded Code")
    st.code(code, language="python")

    # --- PNDC Pipeline Start ---
    # 1. Chunking the code to avoid LLM token limits
    code_lines = code.splitlines()
    chunk_size_lines = 50 
    code_chunks = ["\n".join(code_lines[i:i + chunk_size_lines]) for i in range(0, len(code_lines), chunk_size_lines)]
    
    st.info(f"⚡ PNDC Architecture: Code split into {len(code_chunks)} chunks for parallel map-reduce processing.")
    
    chunk_reports = []
    
    # 2. MAP: Process chunks concurrently
    with st.spinner("Map Phase: Analyzing code chunks concurrently..."):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit tasks to thread pool
            futures = {
                executor.submit(analyze_chunk, i+1, c, engine, top_k): i 
                for i, c in enumerate(code_chunks)
            }
            # Gather results as they complete
            for future in concurrent.futures.as_completed(futures):
                chunk_reports.append(future.result())

    # 3. REDUCE: Merge findings into a final report
    with st.spinner("Reduce Phase: Synthesizing final vulnerability report..."):
        merge_prompt = f"""
        You are a Lead Security Auditor. Merge the following chunked analysis reports into one cohesive, professional vulnerability report.
        Remove duplicates, organize by vulnerability type (e.g., A03: Injection), and provide actionable mitigations.
        
        Raw Chunk Reports:
        {"\n\n---\n\n".join(chunk_reports)}
        """
        model = genai.GenerativeModel("gemini-3.5-flash")
        final_report = model.generate_content(merge_prompt).text

    st.subheader("🛡️ Final Security Audit Report")
    st.markdown(final_report)
    st.success("Analysis Complete!")