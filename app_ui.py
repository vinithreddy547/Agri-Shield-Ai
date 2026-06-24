"""
AgriShield AI: Streamlit Frontend Layout & Style Sheet Component

This module manages the visual rendering and presentation styling for the dashboard.
It implements a premium, custom dark-mode aesthetic utilizing CSS injection directly 
into Streamlit's web-view context.

Key Design Decisions:
1. Glassmorphism: Cards represent standalone AI agents using high-fidelity transparent 
   slate backgrounds (#10b981 border with backdrop filter blur) for depth.
2. Custom Typography: Injects 'Urbanist' and 'Inter' font faces from Google Fonts for 
   optimal readability.
3. Clean Grid Structure: Organizes the orchestrator's summary in a prominent top-level 
   Hero banner followed by a 2-column grid layout for the 5 specialized sub-agent cards.
4. Input Containment: Embeds parameters inside a Streamlit sidebar form block to bundle 
   input state updates, preventing unneeded rerun requests.
"""

import streamlit as st

def inject_premium_styles():
    """Injects high-end, dark-mode cinematic dashboard aesthetics."""
    st.markdown(
        """
        <style>
        /* Base configuration and background */
        .stApp {
            background-color: #0f172a;
            color: #f8fafc;
        }
        
        /* Glassmorphic Cards for Agents */
        .agent-card {
            background: rgba(30, 41, 59, 0.45);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
        }
        
        /* Master Orchestrator Hero Banner */
        .orchestrator-hero {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
            border-left: 6px solid #10b981;
            border-top: 1px solid rgba(16, 185, 129, 0.3);
            border-right: 1px solid rgba(16, 185, 129, 0.1);
            border-bottom: 1px solid rgba(16, 185, 129, 0.1);
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.2);
        }
        
        /* Typography Polish */
        h1, h2, h3 {
            font-family: 'Urbanist', sans-serif !important;
            font-weight: 700 !important;
        }
        
        .agent-title {
            color: #10b981;
            font-size: 1.25rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .hero-title {
            color: #f59e0b;
            font-size: 1.6rem;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_sidebar():
    """Renders the operational control form inside the sidebar."""
    st.sidebar.markdown("## 🚜 AgriShield Control Center")
    st.sidebar.markdown("Configure real-time environmental parameters down below to run grounding checks.")
    
    with st.sidebar.form(key="farm_parameter_form"):
        location = st.selectbox(
            "📍 Select Target Location",
            ["California Central Valley", "Mekong Delta", "Andhra Pradesh Hub", "Iowa Corn Belt", "Bordeaux Region"]
        )
        soil_type = st.selectbox(
            "🧪 Soil Taxonomy Profile", 
            ["Loam", "Clay", "Sandy Loam", "Silt Loam"]
        )
        crop_type = st.selectbox(
            "🌾 Cultivated Crop Type", 
            ["Corn", "Rice", "Almonds", "Wheat", "Soybeans"]
        )
        growth_stage = st.selectbox(
            "📈 Current Phenological Stage", 
            ["Germination", "Vegetative", "Flowering", "Yield Formation", "Ripening"]
        )
        
        submit_btn = st.form_submit_button(label="⚡ Run Risk Analysis")
        
    return submit_btn, {"location": location, "soil_type": soil_type, "crop_type": crop_type, "growth_stage": growth_stage}

def render_dashboard_layout(data=None):
    """Renders the global metrics grid, master hero container, and the sub-agent analysis layout."""
    inject_premium_styles()
    
    # Header Area
    st.markdown("# 🛡️ AgriShield AI: Climate Risk & Farm Decision Platform")
    st.markdown("---")
    
    # Fallback to Mock Data strings if live backend dictionary data isn't active yet (Task 2.3)
    if data is None:
        data = {
            "orchestrator": "Configure farm parameters in the sidebar control panel and trigger the 'Run Risk Analysis' sequence to engage the multi-agent decision grid.",
            "weather": "Awaiting atmospheric data initialization.",
            "crop": "Awaiting crop vegetative index calculations.",
            "disease": "Awaiting fungal/bacterial spore risk vector evaluations.",
            "market": "Awaiting supply-chain terminal price forecasting metrics.",
            "resource": "Awaiting resource conservation planning updates."
        }
        
    # 1. Top Executive Summary Container (Master Agent Hero)
    st.markdown(
        f"""
        <div class="orchestrator-hero">
            <div class="hero-title">👑 Master Farm Decision Orchestrator</div>
            <p style="margin: 0; line-height: 1.6; color: #cbd5e1;">{data['orchestrator']}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("### 🎛️ Specialized Agent Intelligence Panels")
    
    # 2. Sub-Agent Response Grid (2 Columns layout mapping 5 sub-agents)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-title">🌦️ Climate & Weather Tracker</div>
                <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">{data['weather']}</p>
            </div>
            <div class="agent-card">
                <div class="agent-title">🦠 Disease Vector Predictor</div>
                <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">{data['disease']}</p>
            </div>
            <div class="agent-card">
                <div class="agent-title">💧 Resource Allocation Planner</div>
                <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">{data['resource']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="agent-card">
                <div class="agent-title">🌱 Crop Health Analyst</div>
                <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">{data['crop']}</p>
            </div>
            <div class="agent-card">
                <div class="agent-title">💰 Market Price Forecaster</div>
                <p style="margin: 0; font-size: 0.95rem; color: #94a3b8;">{data['market']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    # Allows Partner B to execute standalone visual layout testing (Task 2.3)
    st.set_page_config(page_title="AgriShield AI", layout="wide")
    render_sidebar()
    render_dashboard_layout()
