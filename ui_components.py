import streamlit as st
import math
import pandas as pd

def apply_cyber_theme():
    st.markdown("""
    <style>
    /* Hide Streamlit Clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Cyberpunk Button Hover */
    div.stButton > button:first-child {
        border: 1px solid #00ff99;
        background-color: transparent;
        color: #00ff99;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.2);
    }
    div.stButton > button:first-child:hover {
        background-color: #00ff99;
        color: #0a0e17;
        box-shadow: 0 0 20px rgba(0, 255, 153, 0.6);
        transform: scale(1.02);
    }

    /* Animated Radar Header */
    .radar-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }
    .radar {
        width: 20px;
        height: 20px;
        background-color: #00ff99;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(0, 255, 153, 0.7);
        animation: pulse-radar 1.5s infinite;
    }
    @keyframes pulse-radar {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 153, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 15px rgba(0, 255, 153, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 153, 0); }
    }
    
    /* Terminal Output Box */
    .terminal-box {
        background-color: #050505;
        border-left: 3px solid #00ff99;
        padding: 15px;
        font-family: 'Courier New', Courier, monospace;
        color: #00ff99;
        border-radius: 0 5px 5px 0;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="radar-container">
        <div class="radar"></div>
        <h1 style='margin: 0; padding: 0; color: #f8fafc;'>AEGIS Core</h1>
    </div>
    <p style='color: #94a3b8; font-size: 1.1rem; border-bottom: 1px solid #1e293b; padding-bottom: 10px;'>
        Distributed SAST Analysis Engine // v3.0
    </p>
    """, unsafe_allow_html=True)

def render_pndc_performance_dashboard(scan_metrics=None):
    """
    Renders an interactive PNDC mathematical proof dashboard. 
    It defaults to the LIVE empirical scan data, or allows scalable simulation.
    """
    st.markdown("---")
    st.header("📊 PNDC Performance Metrics & Mathematical Proof")
    st.markdown(
        "This panel provides the foundational **Parallel & Distributed Computing (PDC)** "
        "mathematical validation for the AEGIS Map-Reduce architecture, proving its performance "
        "gains over traditional sequential SAST analysis tools."
    )

    mode = st.radio(
        "Select Dashboard Mode:",
        ["Live Scan Context", "Interactive Scalability Simulator"],
        horizontal=True,
        help="Switch to Simulator Mode during your presentation to showcase how the system handles massive multi-thousand line files."
    )

    if mode == "Interactive Scalability Simulator":
        st.subheader("⚙️ Simulator Parameters")
        col_input1, col_input2, col_input3 = st.columns(3)
        with col_input1:
            lines = st.slider("Total Lines of Code (L)", min_value=50, max_value=20000, value=5000, step=50)
        with col_input2:
            chunk_size = st.slider("Chunk Size (C)", min_value=10, max_value=500, value=150, step=10)
        with col_input3:
            workers = st.slider("Worker Threads (P)", min_value=1, max_value=16, value=5, step=1)
            
        map_time = st.number_input("Est. Map Task Time per Chunk (seconds)", min_value=0.5, max_value=10.0, value=3.0, step=0.5)
        reduce_time = st.number_input("Est. Reduce Phase Aggregation Time (seconds)", min_value=1.0, max_value=20.0, value=5.0, step=1.0)
        
        # Theoretical Calculations
        total_chunks = math.ceil(lines / chunk_size)
        ts = (total_chunks * map_time) + reduce_time
        execution_waves = math.ceil(total_chunks / workers) if workers > 0 else 1
        tp = (execution_waves * map_time) + reduce_time + 1.0  # Added theoretical overhead
        
    else:
        if not scan_metrics:
            st.info("⚠️ Upload and scan a source file in the 'Vulnerability Scanner' tab to generate live empirical insights!")
            return
        
        # Empirical Data Extraction
        lines = scan_metrics["lines"]
        chunk_size = scan_metrics["chunk_size"]
        workers = scan_metrics["workers"]
        map_time = scan_metrics["avg_map_time"]
        reduce_time = scan_metrics["reduce_time"]
        actual_time = scan_metrics["actual_parallel_time"]
        total_chunks = scan_metrics["chunks"]

        st.success(f"✅ **Live Scan Empirical Data:** Successfully analyzed **{lines} lines** of code in **{actual_time:.2f} seconds**.")
        st.info(f"**Execution Breakdown:** The code was decomposed into **{total_chunks} blocks** (max {chunk_size} lines each) and processed across **{workers} concurrent worker threads**.")

        # Real-World Calculations
        ts = (total_chunks * map_time) + reduce_time
        tp = actual_time

    # 4. Speedup (S)
    speedup = ts / tp if tp > 0 else 1
    
    # 5. Amdahl's Law
    total_map_work = total_chunks * map_time
    parallelizable_fraction = total_map_work / ts if ts > 0 else 0
    sequential_fraction = 1.0 - parallelizable_fraction
    amdahl_speedup = 1.0 / (sequential_fraction + (parallelizable_fraction / workers)) if workers > 0 else 1
    
    # 6. Efficiency
    efficiency = (speedup / workers) * 100 if workers > 0 else 0

    st.subheader("📈 System Scaling & Metrics")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric(label="Total Generated Chunks (N)", value=f"{total_chunks} blocks")
    with metric_col2:
        st.metric(label="Projected Serial Time ($T_s$)", value=f"{ts:.2f}s", delta="Slow Serial Loop", delta_color="inverse", help="How long it would take to process this file one chunk at a time.")
    with metric_col3:
        st.metric(label="AEGIS Parallel Time ($T_p$)", value=f"{tp:.2f}s", delta=f"-{(ts-tp):.1f}s Faster", delta_color="normal", help="The actual time taken using Map-Reduce concurrency.")
    with metric_col4:
        st.metric(label="Empirical Speedup ($S$)", value=f"{speedup:.2f}x", help="How many times faster the parallel design is compared to a single-threaded execution.")

    st.markdown("### 🧬 Amdahl's Law Validation")
    amd_col1, amd_col2, amd_col3 = st.columns(3)
    with amd_col1:
        st.metric(label="Parallel Portion ($f$)", value=f"{parallelizable_fraction * 100:.1f}%")
    with amd_col2:
        st.metric(label="Sequential Portion ($s$)", value=f"{sequential_fraction * 100:.1f}%")
    with amd_col3:
        st.metric(label="Amdahl Theoretical Max", value=f"{amdahl_speedup:.2f}x", help="The absolute limit of speedup achievable on this allocation of processors.")

    chart_col1, chart_col2 = st.columns([2, 1])
    with chart_col1:
        st.write("**Execution Time Comparison (Lower is Better)**")
        chart_data = pd.DataFrame({
            'Execution Mode': ['Projected Sequential Time (Ts)', 'Map-Reduce Time (Tp)'],
            'Time (Seconds)': [ts, tp]
        })
        st.bar_chart(data=chart_data, x='Execution Mode', y='Time (Seconds)', height=300)
    with chart_col2:
        st.write("**Core Hardware Efficiency**")
        st.metric(label="Compute Core Efficiency ($E$)", value=f"{efficiency:.1f}%", help="Measures how effectively the active worker threads are utilized.")
        st.progress(min(max(int(efficiency), 0), 100))

    with st.expander("📝 View Formal Mathematical Derivations (For Presentation Panel)"):
        st.markdown("#### 1. Task Decomposition Formula")
        st.latex(r"N = \left\lceil \frac{L}{C} \right\rceil")
        st.markdown("#### 2. Sequential vs. Parallel Time Complexity Models")
        st.latex(r"T_s = (N \times t_{map}) + t_{reduce}")
        st.latex(r"T_p = \left( \left\lceil \frac{N}{P} \right\rceil \times t_{map} \right) + t_{reduce} + \mathcal{O}")
        st.markdown("#### 3. Theoretical Speedup Bound (Amdahl's Law)")
        st.latex(r"S_{max} = \frac{1}{s + \frac{f}{P}}")