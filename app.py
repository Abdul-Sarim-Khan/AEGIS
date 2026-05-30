"""
app.py
======
Streamlit frontend for the LLM-powered SAST tool.
Fully wired with Gemini API and PNDC Map-Reduce Architecture.
"""

import streamlit as st
import concurrent.futures
import time
from google import genai
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
def analyze_chunk(chunk_id: int, code_chunk: str, engine: RagEngine, top_k: int, client: genai.Client) -> str:
    """MAP PHASE: Retrieves specific rules for a code chunk and asks LLM to analyze it."""
    results = engine.search(code_chunk, top_k=top_k)
    rules_context = "\n\n".join(r.chunk.text for r in results)
    
    prompt = f"""
    You are an expert Secure Code Reviewer. Review the following code chunk.
    Only report critical security vulnerabilities. If none exist, state "No vulnerabilities found."
    
    OWASP Guidelines to follow:
    {rules_context}
    
    Source Code Chunk:
    {code_chunk}
    """
    
    # Robust Retry Logic for Free-Tier API Limits
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
                time.sleep(2) # Wait 2 seconds and try again if Google servers are busy
                continue
            return f"Error analyzing chunk {chunk_id} after {max_retries} attempts: {e}"

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
        
    client = genai.Client(api_key=api_key)
    
    st.subheader("Uploaded Code")
    st.code(code, language="python")

    # --- PNDC Pipeline Start ---
    code_lines = code.splitlines()
    chunk_size_lines = 150 
    code_chunks = ["\n".join(code_lines[i:i + chunk_size_lines]) for i in range(0, len(code_lines), chunk_size_lines)]
    
    st.info(f"⚡ PNDC Architecture: Code split into {len(code_chunks)} chunks for parallel map-reduce processing.")
    
    chunk_reports = []
    
    # 2. MAP: Process chunks concurrently
    with st.spinner("Map Phase: Analyzing code chunks concurrently..."):
        # Lowered to 5 workers to prevent 503 Overload errors on free-tier keys
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(analyze_chunk, i+1, c, engine, top_k, client): i 
                for i, c in enumerate(code_chunks)
            }
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
        
        # Robust Retry Logic for the final Reduce phase
        max_retries = 3
        final_report = "Error: Could not generate report."
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
                    time.sleep(3) # Wait 3 seconds before retrying the heavy reduce prompt
                else:
                    st.error(f"Google API is currently overloaded (503). Please try running the analysis again.")
                    st.stop()

    st.subheader("🛡️ Final Security Audit Report")
    st.markdown(final_report)
    st.success("Analysis Complete!")