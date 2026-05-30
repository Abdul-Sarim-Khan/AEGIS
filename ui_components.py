import streamlit as st

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