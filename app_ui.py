import streamlit as st

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

# Handle form submission state
if submit_button:
    st.sidebar.success(f"Parameters updated! Analyzing {crop_type} in {location or 'default location'}...")

# ==========================================
# 2. MAIN CONTENT AREA
# ==========================================
st.markdown('<div class="main-header">📊 AgriShield AI: Climate Risk & Farm Decision Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="main-description">Mitigating climate risks and optimizing crop yields using collaborative, multi-agent intelligence.</div>', unsafe_allow_html=True)

# ------------------------------------------
# HERO CONTAINER (Master Agent Orchestrator)
# ------------------------------------------
orchestrator_mock = (
    "👉 **[ORCHESTRATOR MOCK DATA]** High priority action required: "
    "Schedule immediate targeted irrigation. High heatwave thresholds expected in the next 48 hours "
    "will compound current vegetative water deficits. Market demand indices remain high (0.90), "
    "making yield protection critical."
)

st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">🤖 Master Farm Decision Orchestrator</div>
    <div class="hero-body">{orchestrator_mock}</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------
# SUB-AGENT CONTAINERS (Structured Grid Layout)
# ------------------------------------------
st.markdown("### 🧩 Specialized Sub-Agent Intelligence Panels")

# Mock data for specialized sub-agents
weather_mock = "🌦️ **[MOCK]** Alert: Incoming extreme heatwave. Temperatures projected to hit 38.2°C. Relative humidity at a dry 20%."
crop_mock = "🌱 **[MOCK]** Target stage: Vegetative. Current daily requirement: 5.5 Liters/plant. Baseline yield benchmark is 4.5 tons/acre."
disease_mock = "🦠 **[MOCK]** Risk Level: Low. Fungal triggers require cool, damp conditions (&lt;25°C), whereas current localized forecast shows high dry heat."
market_mock = "💰 **[MOCK]** Current Valuations: $4,200.00/ton. Trend: Increasing. Strong global export signals due to supply deficits."
resource_mock = "💧 **[MOCK]** Dynamic Directives: Increase drip-line frequency by 25%. Maintain current soil nitrogen metrics to prevent late-stage crop stress."

# Create grid: 3 columns for Row 1, 2 columns for Row 2
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2 = st.columns(2)

# Row 1 - Column 1: Climate & Weather Tracker
with row1_col1:
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-card-title">🌦️ Climate & Weather Tracker</div>
        <div class="agent-card-body">{weather_mock}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 1 - Column 2: Crop Health Analyst
with row1_col2:
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-card-title">🌱 Crop Health Analyst</div>
        <div class="agent-card-body">{crop_mock}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 1 - Column 3: Disease Vector Predictor
with row1_col3:
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-card-title">🦠 Disease Vector Predictor</div>
        <div class="agent-card-body">{disease_mock}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2 - Column 1: Market Price Forecaster
with row2_col1:
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-card-title">💰 Market Price Forecaster</div>
        <div class="agent-card-body">{market_mock}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2 - Column 2: Resource Allocation Planner
with row2_col2:
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-card-title">💧 Resource Allocation Planner</div>
        <div class="agent-card-body">{resource_mock}</div>
    </div>
    """, unsafe_allow_html=True)

# Footer info
st.markdown("---")
st.caption("AgriShield AI • Decision Support System • Powered by Multi-Agent Simulation")
