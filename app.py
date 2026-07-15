"""
AI Company — Streamlit Dashboard (v2 — Premium UI)
====================================================
A stunning, premium dark-themed dashboard with glassmorphism,
micro-animations, and modern design to run the AI Company.
"""

import os
import time
import requests
import streamlit as st
from config import AVAILABLE_MODELS

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Company — Multi-Agent Startup Engine",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
    /* ── Import Fonts ──────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── ROOT VARIABLES ────────────────────────────── */
    :root {
        --bg-primary: #06070f;
        --bg-secondary: #0c0e1a;
        --bg-card: rgba(14, 17, 35, 0.7);
        --bg-card-hover: rgba(20, 24, 48, 0.85);
        --bg-glass: rgba(255, 255, 255, 0.03);
        --border-glass: rgba(255, 255, 255, 0.06);
        --border-glow: rgba(99, 102, 241, 0.3);
        --text-primary: #e8eaed;
        --text-secondary: #8b8fa3;
        --text-muted: #5a5e73;
        --accent-1: #6366f1;
        --accent-2: #818cf8;
        --accent-3: #a78bfa;
        --accent-4: #c084fc;
        --gradient-1: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7);
        --gradient-2: linear-gradient(135deg, #06b6d4, #3b82f6, #6366f1);
        --gradient-3: linear-gradient(135deg, #f59e0b, #ef4444, #ec4899);
        --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
        --radius-lg: 20px;
        --radius-md: 14px;
        --radius-sm: 10px;
    }

    /* ── GLOBAL RESET ──────────────────────────────── */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
    }

    .stApp > header { background: transparent !important; }

    .stMainBlockContainer { padding-top: 1rem !important; }

    /* ── SIDEBAR ───────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080a18 0%, #0c0e1a 40%, #10132a 100%) !important;
        border-right: 1px solid var(--border-glass) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: var(--text-secondary) !important;
        font-size: 0.88rem;
    }

    /* ── SCROLLBAR ─────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: #2a2d4a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-1); }

    /* ── HERO HEADER ───────────────────────────────── */
    .hero-container {
        position: relative;
        padding: 3rem 2.5rem 2.5rem;
        border-radius: var(--radius-lg);
        background: linear-gradient(145deg, #0e1025 0%, #151937 50%, #0e1025 100%);
        border: 1px solid var(--border-glass);
        margin-bottom: 2rem;
        overflow: hidden;
        box-shadow: var(--shadow-glow);
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent-2), transparent);
    }
    .hero-container::after {
        content: '';
        position: absolute;
        top: -100px; right: -100px;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 50px;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--accent-2);
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin-bottom: 0.6rem;
        background: linear-gradient(135deg, #fff 0%, #c7d2fe 40%, #818cf8 70%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-desc {
        font-size: 1.05rem;
        color: var(--text-secondary);
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
    }

    /* ── METRIC CARDS ──────────────────────────────── */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 1.4rem 1.2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-3px);
        box-shadow: var(--shadow-glow);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 2px 2px 0 0;
    }
    .metric-card:nth-child(1)::before { background: var(--gradient-1); }
    .metric-card:nth-child(2)::before { background: var(--gradient-2); }
    .metric-card:nth-child(3)::before { background: var(--gradient-3); }
    .metric-card:nth-child(4)::before { background: linear-gradient(135deg, #10b981, #06b6d4); }
    .metric-icon {
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #fff;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* ── INPUT SECTION ─────────────────────────────── */
    .input-section {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
    }
    .input-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(6,182,212,0.4), transparent);
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.3rem;
    }
    .section-subtitle {
        font-size: 0.88rem;
        color: var(--text-muted);
        margin-bottom: 1.2rem;
    }

    /* Streamlit text area styling */
    .stTextArea textarea {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 14px !important;
        transition: border-color 0.3s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
    }
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }

    /* ── BUTTONS ────────────────────────────────────── */
    .stButton > button[kind="primary"] {
        background: var(--gradient-1) !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        padding: 0.65rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99,102,241,0.45) !important;
    }

    .stButton > button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid var(--border-glow) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--accent-2) !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(99,102,241,0.1) !important;
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-secondary) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--accent-1) !important;
        color: var(--accent-2) !important;
        background: rgba(99,102,241,0.08) !important;
    }

    /* ── AGENT SIDEBAR CARDS ───────────────────────── */
    .agent-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: var(--radius-sm);
        padding: 12px 14px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.25s ease;
    }
    .agent-card:hover {
        background: rgba(99,102,241,0.06);
        border-color: rgba(99,102,241,0.15);
    }
    .agent-avatar {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .agent-avatar.ceo    { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
    .agent-avatar.research { background: linear-gradient(135deg, #06b6d4, #3b82f6); }
    .agent-avatar.dev    { background: linear-gradient(135deg, #10b981, #06b6d4); }
    .agent-avatar.mkt    { background: linear-gradient(135deg, #f43f5e, #ec4899); }
    .agent-avatar.support { background: linear-gradient(135deg, #f59e0b, #ef4444); }
    .agent-info { flex: 1; }
    .agent-name {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    .agent-role {
        font-size: 0.7rem;
        color: var(--text-muted);
    }
    .agent-status {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
        flex-shrink: 0;
        box-shadow: 0 0 6px rgba(34,197,94,0.4);
    }

    /* ── WORKFLOW PIPELINE ──────────────────────────── */
    .pipeline-container {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
    }
    .pipeline-steps {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0;
        position: relative;
    }
    .pipeline-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        position: relative;
        z-index: 1;
        flex: 1;
    }
    .pipeline-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        border: 2px solid var(--border-glass);
        background: var(--bg-secondary);
        transition: all 0.3s ease;
    }
    .pipeline-icon.active {
        border-color: var(--accent-1);
        box-shadow: 0 0 20px rgba(99,102,241,0.3);
    }
    .pipeline-label {
        font-size: 0.7rem;
        font-weight: 500;
        color: var(--text-muted);
        text-align: center;
    }
    .pipeline-connector {
        flex: 1;
        height: 2px;
        background: var(--border-glass);
        margin-top: -24px;
        position: relative;
    }
    .pipeline-connector.active {
        background: linear-gradient(90deg, var(--accent-1), var(--accent-3));
    }

    /* ── RESULTS SECTION ───────────────────────────── */
    .results-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .results-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #fff;
    }
    .results-count {
        background: rgba(34,197,94,0.1);
        border: 1px solid rgba(34,197,94,0.2);
        color: #22c55e;
        padding: 2px 10px;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 700;
    }

    .dept-result-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .dept-result-card:hover {
        border-color: var(--border-glow);
        box-shadow: var(--shadow-glow);
    }
    .dept-result-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
    }
    .dept-result-card.ceo::before    { background: var(--gradient-1); }
    .dept-result-card.research::before { background: var(--gradient-2); }
    .dept-result-card.dev::before    { background: linear-gradient(180deg, #10b981, #06b6d4); }
    .dept-result-card.mkt::before    { background: linear-gradient(180deg, #f43f5e, #ec4899); }
    .dept-result-card.support::before { background: linear-gradient(180deg, #f59e0b, #ef4444); }

    .dept-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 0.5rem;
    }
    .dept-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .dept-icon.ceo    { background: rgba(99,102,241,0.12); }
    .dept-icon.research { background: rgba(6,182,212,0.12); }
    .dept-icon.dev    { background: rgba(16,185,129,0.12); }
    .dept-icon.mkt    { background: rgba(244,63,94,0.12); }
    .dept-icon.support { background: rgba(245,158,11,0.12); }
    .dept-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #fff;
    }
    .dept-tag {
        font-size: 0.7rem;
        color: var(--text-muted);
    }

    /* ── STATUS BADGES ─────────────────────────────── */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-pill.running {
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.25);
        color: var(--accent-2);
    }
    .status-pill.running::before {
        content: '';
        width: 7px; height: 7px;
        border-radius: 50%;
        background: var(--accent-1);
        animation: blink 1.5s infinite;
    }
    .status-pill.completed {
        background: rgba(34,197,94,0.1);
        border: 1px solid rgba(34,197,94,0.25);
        color: #22c55e;
    }
    .status-pill.failed {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.25);
        color: #ef4444;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* ── TABS ──────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255,255,255,0.02);
        border-radius: var(--radius-sm);
        padding: 4px;
        border: 1px solid var(--border-glass);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        color: var(--text-secondary) !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,102,241,0.12) !important;
        color: var(--accent-2) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem !important;
    }

    /* ── EXPANDERS ──────────────────────────────────── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.02) !important;
        border-radius: var(--radius-sm) !important;
        border: 1px solid var(--border-glass) !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }

    /* ── ALERTS ─────────────────────────────────────── */
    .stAlert {
        border-radius: var(--radius-sm) !important;
    }

    /* ── PROGRESS BAR ──────────────────────────────── */
    .stProgress > div > div {
        background: var(--gradient-1) !important;
    }

    /* ── SIDEBAR DIVIDER ───────────────────────────── */
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-glass), transparent);
        margin: 16px 0;
    }

    /* ── SIDEBAR LOGO ──────────────────────────────── */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0 20px;
    }
    .sidebar-logo-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: var(--gradient-1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 16px rgba(99,102,241,0.3);
    }
    .sidebar-logo-text {
        font-size: 1.1rem;
        font-weight: 800;
        color: #fff;
        letter-spacing: -0.3px;
    }
    .sidebar-logo-version {
        font-size: 0.65rem;
        color: var(--text-muted);
        font-weight: 500;
    }

    /* ── FOOTER ─────────────────────────────────────── */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: var(--text-muted);
        font-size: 0.78rem;
    }
    .footer a {
        color: var(--accent-2);
        text-decoration: none;
    }

    /* ── HIDE STREAMLIT DEFAULTS ───────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── API Config ───────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://localhost:8000")


def api_available() -> bool:
    try:
        r = requests.get(f"{API_URL}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# ── Session State ────────────────────────────────────────
if "current_job_id" not in st.session_state:
    st.session_state.current_job_id = None
if "results" not in st.session_state:
    st.session_state.results = None
if "mode" not in st.session_state:
    st.session_state.mode = "direct"


# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🏢</div>
        <div>
            <div class="sidebar-logo-text">AI Company</div>
            <div class="sidebar-logo-version">v2.0 · Multi-Agent Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Mode selector
    st.markdown("##### ⚡ Execution Mode")
    mode = st.radio(
        "mode_select",
        ["⚡ Direct Mode", "🌐 API Mode"],
        index=0,
        label_visibility="collapsed",
        help="Direct Mode runs agents in-process. API Mode requires FastAPI server."
    )
    st.session_state.mode = "api" if "API" in mode else "direct"

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Agent cards
    st.markdown("##### 🤖 AI Agents")

    agents_data = [
        ("👔", "CEO", "Business Strategy & Vision", "ceo"),
        ("🔬", "Research Analyst", "Market Analysis & Competitors", "research"),
        ("💻", "Developer", "Product Code & MVP", "dev"),
        ("📢", "Marketing Lead", "Campaigns & Content", "mkt"),
        ("🎧", "Support Lead", "FAQ & Customer Service", "support"),
    ]

    for icon, name, role, cls in agents_data:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-avatar {cls}">{icon}</div>
            <div class="agent-info">
                <div class="agent-name">{name}</div>
                <div class="agent-role">{role}</div>
            </div>
            <div class="agent-status"></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Tech stack
    st.markdown("##### 🧰 Powered By")
    st.caption("CrewAI · Groq · LLaMA 3.1 · FastAPI · Streamlit")

    st.markdown("""
    <div style="text-align:center; padding:1rem 0; color:var(--text-muted); font-size:0.72rem;">
        Built with ❤️ by AI Company Engine
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  HERO HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">
        <span>🔮</span> MULTI-AGENT AI STARTUP ENGINE
    </div>
    <div class="hero-title">Build Your Startup<br>With AI Agents</div>
    <div class="hero-desc">
        5 specialized AI agents collaborate to generate a complete startup package — from business strategy to product code to marketing campaigns. Just describe your idea.
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  METRICS ROW
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-icon">🤖</div>
        <div class="metric-value">5</div>
        <div class="metric-label">AI Agents</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">🏗️</div>
        <div class="metric-value">5</div>
        <div class="metric-label">Departments</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">&lt;3m</div>
        <div class="metric-label">Generation</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-value">∞</div>
        <div class="metric-label">Ideas</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  WORKFLOW PIPELINE
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="pipeline-container">
    <div style="font-size:0.78rem; font-weight:600; color:var(--text-muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:1rem;">
        Agent Pipeline
    </div>
    <div class="pipeline-steps">
        <div class="pipeline-step">
            <div class="pipeline-icon active">💡</div>
            <div class="pipeline-label">Your Idea</div>
        </div>
        <div class="pipeline-connector active"></div>
        <div class="pipeline-step">
            <div class="pipeline-icon">👔</div>
            <div class="pipeline-label">CEO</div>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🔬</div>
            <div class="pipeline-label">Research</div>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-step">
            <div class="pipeline-icon">💻</div>
            <div class="pipeline-label">Developer</div>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-step">
            <div class="pipeline-icon">📢</div>
            <div class="pipeline-label">Marketing</div>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-step">
            <div class="pipeline-icon">🎧</div>
            <div class="pipeline-label">Support</div>
        </div>
        <div class="pipeline-connector"></div>
        <div class="pipeline-step">
            <div class="pipeline-icon">📊</div>
            <div class="pipeline-label">Report</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  INPUT SECTION
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="input-section">
    <div class="section-title">🚀 Launch Your Startup</div>
    <div class="section-subtitle">Describe your startup idea and our AI agents will generate everything you need</div>
</div>
""", unsafe_allow_html=True)

startup_idea = st.text_area(
    "startup_input",
    placeholder='e.g., "Create an AI-powered platform that helps students study more effectively using personalized learning paths, flashcard generation, and smart quiz creation..."',
    height=130,
    label_visibility="collapsed",
    key="startup_input",
)

selected_model = st.selectbox("🤖 Select AI Model", AVAILABLE_MODELS)

col_btn, col_space = st.columns([1, 3])
with col_btn:
    launch_btn = st.button(
        "🚀 Launch AI Company",
        type="primary",
        use_container_width=True,
    )


# ══════════════════════════════════════════════════════════
#  LAUNCH LOGIC
# ══════════════════════════════════════════════════════════
if launch_btn and startup_idea.strip():
    if st.session_state.mode == "api":
        if not api_available():
            st.error(
                "❌ FastAPI server not running! Start it with:\n\n"
                "```\nuvicorn api:app --reload --port 8000\n```\n\n"
                "Or switch to **⚡ Direct Mode** in the sidebar."
            )
        else:
            with st.spinner("📡 Sending to AI Company..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/api/run",
                        json={"startup_idea": startup_idea.strip(), "model": selected_model},
                        timeout=10,
                    )
                    data = resp.json()
                    st.session_state.current_job_id = data["job_id"]
                    st.success(f"✅ Job started! ID: `{data['job_id']}`")
                except Exception as e:
                    st.error(f"Failed to start job: {e}")
    else:
        # Direct mode
        st.session_state.results = None

        dept_steps = [
            ("👔 CEO", "Crafting business strategy & vision...", 15),
            ("🔬 Research", "Analyzing market & competitors...", 35),
            ("💻 Developer", "Building product prototype...", 55),
            ("📢 Marketing", "Creating campaigns & content...", 75),
            ("🎧 Support", "Preparing FAQ & customer support...", 90),
        ]

        progress_bar = st.progress(0, text="🏢 Initializing AI Company...")
        status_container = st.empty()

        try:
            from crew import run_company as direct_run

            for name, msg, pct in dept_steps:
                progress_bar.progress(pct, text=f"{name} — {msg}")
                with status_container.container():
                    st.markdown(
                        f'<span class="status-pill running">{name} agent is working...</span>',
                        unsafe_allow_html=True,
                    )
                time.sleep(0.3)

            results = direct_run(startup_idea.strip(), model_name=selected_model)
            progress_bar.progress(100, text="✅ All agents completed!")
            status_container.empty()
            st.session_state.results = results
            st.balloons()

        except Exception as e:
            progress_bar.progress(100, text="❌ Error occurred")
            st.error(f"Error: {e}")

elif launch_btn:
    st.warning("⚠️ Please describe your startup idea first!")


# ══════════════════════════════════════════════════════════
#  POLL API RESULTS
# ══════════════════════════════════════════════════════════
if st.session_state.mode == "api" and st.session_state.current_job_id:
    job_id = st.session_state.current_job_id
    if api_available():
        try:
            status_resp = requests.get(f"{API_URL}/api/status/{job_id}", timeout=5)
            status_data = status_resp.json()
            status = status_data["status"]

            cls = status
            st.markdown(
                f'<span class="status-pill {cls}">{status.upper()}</span> '
                f'<span style="color:var(--text-muted);font-size:0.82rem;margin-left:8px;">'
                f'Job ID: {job_id}</span>',
                unsafe_allow_html=True,
            )

            if status == "running":
                st.info("⏳ Your AI agents are working... Click refresh to check.")
                if st.button("🔄 Refresh Status"):
                    st.rerun()
            elif status == "completed":
                result_resp = requests.get(f"{API_URL}/api/results/{job_id}", timeout=10)
                st.session_state.results = result_resp.json().get("results", {})
            elif status == "failed":
                st.error(f"❌ Job failed: {status_data.get('error', 'Unknown error')}")
        except Exception as e:
            st.warning(f"Could not fetch status: {e}")


# ══════════════════════════════════════════════════════════
#  DISPLAY RESULTS
# ══════════════════════════════════════════════════════════
if st.session_state.results:
    results = st.session_state.results

    st.markdown('<hr style="border-color:var(--border-glass);margin:2rem 0;">', unsafe_allow_html=True)

    st.markdown("""
    <div class="results-header">
        <div class="results-title">📊 Deliverables</div>
        <div class="results-count">5 REPORTS GENERATED</div>
    </div>
    """, unsafe_allow_html=True)

    # Department config
    dept_config = {
        "ceo_strategy": {
            "icon": "👔", "name": "CEO", "title": "Business Strategy",
            "tag": "Vision · Roadmap · Revenue Model", "cls": "ceo",
        },
        "market_research": {
            "icon": "🔬", "name": "Research", "title": "Market Analysis",
            "tag": "Competitors · SWOT · Market Size", "cls": "research",
        },
        "product_development": {
            "icon": "💻", "name": "Developer", "title": "Product & Code",
            "tag": "Architecture · MVP · Landing Page", "cls": "dev",
        },
        "marketing_plan": {
            "icon": "📢", "name": "Marketing", "title": "Go-to-Market",
            "tag": "Social Media · Ads · SEO Blog", "cls": "mkt",
        },
        "customer_support": {
            "icon": "🎧", "name": "Support", "title": "Customer Experience",
            "tag": "FAQ · Templates · Onboarding", "cls": "support",
        },
    }

    # Tabs
    tab_labels = [f"{c['icon']} {c['name']}" for c in dept_config.values()]
    tabs = st.tabs(tab_labels)

    for (key, cfg), tab in zip(dept_config.items(), tabs):
        with tab:
            content = results.get(key, "No data available.")

            st.markdown(f"""
            <div class="dept-result-card {cfg['cls']}">
                <div class="dept-header">
                    <div class="dept-icon {cfg['cls']}">{cfg['icon']}</div>
                    <div>
                        <div class="dept-name">{cfg['title']}</div>
                        <div class="dept-tag">{cfg['tag']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(content)

            st.download_button(
                label=f"📥 Download {cfg['name']} Report",
                data=content,
                file_name=f"{key}.md",
                mime="text/markdown",
                key=f"dl_{key}",
            )

    # Full report
    if "full_report" in results:
        with st.expander("📋 View Full Combined Report"):
            st.markdown(results["full_report"])

    st.markdown('<hr style="border-color:var(--border-glass);margin:2rem 0;">', unsafe_allow_html=True)

    col_new, _ = st.columns([1, 3])
    with col_new:
        if st.button("🔄 Start New Run", type="secondary", use_container_width=True):
            st.session_state.results = None
            st.session_state.current_job_id = None
            st.rerun()

# ── Footer ───────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with <a href="https://crewai.com">CrewAI</a> · <a href="https://groq.com">Groq</a> · <a href="https://streamlit.io">Streamlit</a>
</div>
""", unsafe_allow_html=True)
