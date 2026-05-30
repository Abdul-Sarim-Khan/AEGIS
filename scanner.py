import concurrent.futures
import google.generativeai as genai
import time
from rag_engine import RagEngine

def analyze_chunk(chunk_id: int, code_chunk: str, engine: RagEngine, top_k: int) -> tuple:
    """MAP PHASE: Returns chunk_id and the report."""
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
    model = genai.GenerativeModel("gemini-3.5-flash")
    try:
        response = model.generate_content(prompt)
        return chunk_id, f"### Analysis of Code Chunk {chunk_id}\n" + response.text
    except Exception as e:
        return chunk_id, f"Error analyzing chunk {chunk_id}: {e}"

def run_distributed_scan(code_chunks: list, engine: RagEngine, top_k: int, progress_bar, log_placeholder):
    """Executes the Map-Reduce pipeline with LIVE UI updates."""
    chunk_reports = []
    total_chunks = len(code_chunks)
    terminal_log = "[SYSTEM] Initializing ThreadPoolExecutor...\n"
    
    # --- MAP PHASE (Concurrent) ---
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(analyze_chunk, i+1, c, engine, top_k): i 
            for i, c in enumerate(code_chunks)
        }
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            chunk_id, result = future.result()
            chunk_reports.append(result)
            completed += 1
            
            # Live UI Updates!
            progress = int((completed / total_chunks) * 50) # Map phase is 50% of total progress
            progress_bar.progress(progress)
            
            terminal_log += f"[THREAD-{chunk_id}] Code chunk analyzed successfully. Context applied.\n"
            log_placeholder.markdown(f'<div class="terminal-box">{terminal_log}</div>', unsafe_allow_html=True)

    # --- REDUCE PHASE ---
    terminal_log += "[SYSTEM] Map phase complete. Initiating Reducer synthesis...\n"
    log_placeholder.markdown(f'<div class="terminal-box">{terminal_log}</div>', unsafe_allow_html=True)
    progress_bar.progress(75)

    merge_prompt = f"""
    You are a Lead Security Auditor. Merge the following chunked analysis reports into one cohesive, professional vulnerability report.
    Organize by vulnerability type (e.g., A03: Injection), and provide actionable mitigations in Markdown format.
    Raw Chunk Reports:
    {"\n\n---\n\n".join(chunk_reports)}
    """
    model = genai.GenerativeModel("gemini-3.5-flash")
    final_report = model.generate_content(merge_prompt).text
    
    progress_bar.progress(100)
    terminal_log += "[SYSTEM] Synthesis complete. Audit ready.\n"
    log_placeholder.markdown(f'<div class="terminal-box">{terminal_log}</div>', unsafe_allow_html=True)
    
    return final_report, chunk_reports