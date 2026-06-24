import streamlit as st
import os
from agent_brain import run_master_orchestrator

# Configure the Streamlit page
st.set_page_config(
    page_title="AgriShield AI: Farm Decision Dashboard",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich, modern agricultural dashboard aesthetics (Glassmorphism & Clean Typography)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Font Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
    }

    /* Main App Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .main-description {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }

    /* Hero Banner for Master Orchestrator */
    .hero-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.15) 100%);
        border-left: 6px solid #10B981;
        border-radius: 12px;
        padding: 1.75rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    .hero-title {
        color: #065F46;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .hero-body {
        color: #047857;
        font-size: 1.05rem;
        line-height: 1.6;
        font-weight: 500;
    }

    /* Sub-Agent Cards */
    .agent-card {
        background-color: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(229, 231, 235, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        min-height: 160px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    /* Dark-mode compatibility adjustment */
    @media (prefers-color-scheme: dark) {
        .agent-card {
            background-color: rgba(31, 41, 55, 0.7);
            border-color: rgba(75, 85, 99, 0.4);
        }
        .main-description {
            color: #9CA3AF;
        }
        .hero-title {
            color: #34D399;
        }
        .hero-body {
            color: #A7F3D0;
        }
    }
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #10B981;
    }
    .agent-card-title {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .agent-card-body {
        font-size: 0.95rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. STREAMLIT SIDEBAR (Form Inputs)
# ==========================================
st.sidebar.markdown("## 🚜 AgriShield AI Parameters")
st.sidebar.markdown("Configure your farm parameters below to trigger a multi-agent risk assessment.")

with st.sidebar.form(key="farm_parameters_form"):
    location = st.text_input(
        "Location", 
        value="California Central Valley",
        placeholder="e.g., California Central Valley"
    )
    
    soil_type = st.selectbox(
        "Soil Type", 
        options=["Loam", "Clay", "Sandy", "Silt"]
    )
    
    crop_type = st.selectbox(
        "Crop Type", 
        options=["Corn", "Rice", "Almonds", "Wheat", "Soybeans"]
    )
    
    crop_stage = st.selectbox(
        "Current Crop Stage", 
        options=["Germination", "Vegetative", "Flowering", "Yield Formation", "Ripening"]
    )
    
    submit_button = st.form_submit_button(label="Analyze Farm Risk")

# ==========================================
# 2. MAIN CONTENT AREA
# ==========================================
st.markdown('<div class="main-header">📊 AgriShield AI: Climate Risk & Farm Decision Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="main-description">Mitigating climate risks and optimizing crop yields using collaborative, multi-agent intelligence.</div>', unsafe_allow_html=True)

# Check if the user has clicked "Analyze Farm Risk"
if submit_button:
    # Display loading spinner during orchestration
    with st.spinner("Orchestrating AI Sub-Agents & Evaluating Climate Risks..."):
        # Trigger backend multi-agent evaluation
        results = run_master_orchestrator(location, crop_type, crop_stage, soil_type)
        
    st.sidebar.success(f"Analysis complete for {crop_type} in {location}!")
    
    # ------------------------------------------
    # HERO CONTAINER (Master Agent Orchestrator - Dynamic)
    # ------------------------------------------
    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-title">🤖 Master Farm Decision Orchestrator</div>
        <div class="hero-body">{results['orchestrator']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------
    # SUB-AGENT CONTAINERS (Dynamic Grid Layout)
    # ------------------------------------------
    st.markdown("### 🧩 Specialized Sub-Agent Intelligence Panels")

    # Create grid: 3 columns for Row 1, 2 columns for Row 2
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2 = st.columns(2)

    # Row 1 - Climate & Weather Tracker
    with row1_col1:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-card-title">🌦️ Climate & Weather Tracker</div>
            <div class="agent-card-body">{results['weather']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Row 1 - Crop Health Analyst
    with row1_col2:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-card-title">🌱 Crop Health Analyst</div>
            <div class="agent-card-body">{results['crop']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Row 1 - Disease Vector Predictor
    with row1_col3:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-card-title">🦠 Disease Vector Predictor</div>
            <div class="agent-card-body">{results['disease']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Row 2 - Market Price Forecaster
    with row2_col1:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-card-title">💰 Market Price Forecaster</div>
            <div class="agent-card-body">{results['market']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Row 2 - Resource Allocation Planner
    with row2_col2:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-card-title">💧 Resource Allocation Planner</div>
            <div class="agent-card-body">{results['resource']}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    # 4. INITIALIZATION STATE: Friendly message instructing user to analyze
    st.info("👋 Welcome to AgriShield AI! Please configure your farm parameters in the sidebar and click **'Analyze Farm Risk'** to orchestrate the sub-agent simulation and view localized intelligence panels.")
    
    # Beautiful visual guidance banner
    st.markdown("""
    <div style="background-color: rgba(16, 185, 129, 0.05); border: 1px dashed rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 3rem; text-align: center; margin-top: 2rem;">
        <h3 style="color: #047857; margin-bottom: 0.75rem; font-size: 1.5rem;">Awaiting Farm Parameter Setup</h3>
        <p style="color: #6B7280; font-size: 1.05rem; max-width: 650px; margin: 0 auto; line-height: 1.6;">
            Once you press <b>'Analyze Farm Risk'</b>, the Master Decision Orchestrator will query localized weather data, examine crop benchmarks, evaluate disease indicators, check global market trends, and return customized resource action directives.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer info
st.markdown("---")
st.caption("AgriShield AI • Decision Support System • Powered by Multi-Agent Simulation")
