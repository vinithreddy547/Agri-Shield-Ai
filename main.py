import streamlit as st
from app_ui import render_sidebar, render_dashboard_layout
from agent_brain import run_multi_agent_pipeline

# Configure application-wide layout geometry
st.set_page_config(
    page_title="AgriShield AI Dashboard",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Render UI Parameter Form Controls
submit_triggered, form_inputs = render_sidebar()

# 2. Control flow routing logic based on user interaction states
if submit_triggered:
    # Initialize a loading spinner while the Gemini multi-agent loop runs
    with st.spinner("🤖 Engaging Multi-Agent Grid & Extracting Grounded Insights..."):
        try:
            # Query the backend engine
            live_agent_payload = run_multi_agent_pipeline(form_inputs)
            
            # Map values back into your UI layout components (Task 4.3)
            render_dashboard_layout(live_agent_payload)
            
        except Exception as e:
            st.error(f"Critical execution fault during multi-agent orchestration: {e}")
else:
    # Default initialization state when the user lands on the dashboard
    render_dashboard_layout()
