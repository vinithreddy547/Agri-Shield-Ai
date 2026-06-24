"""
AgriShield AI: Farm Decision Dashboard Entrypoint

This script coordinates the Streamlit frontend layout with the multi-agent backend.
It handles user input events, triggers the background agent orchestration loop under 
a visual spinner, and feeds the resulting expert reports back into the layout panels.

Design Decisions:
- Decoupled Frontend/Backend: Visual presentation logic is isolated in `app_ui.py`, 
  while the agent routing and database lookups reside in `agent_brain.py`.
- Session State Routing: The app routes flows dynamically depending on Streamlit forms' 
  submission status to prevent unneeded backend queries on initial page load.
"""

import streamlit as st
from app_ui import render_sidebar, render_dashboard_layout
from agent_brain import run_multi_agent_pipeline

# Configure application-wide layout geometry
# Needs to run as the first Streamlit command to set browser page details
st.set_page_config(
    page_title="AgriShield AI Dashboard",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Render UI Parameter Form Controls
# sidebar renders the parameters input form and returns a tuple (submit_clicked, inputs_dict)
submit_triggered, form_inputs = render_sidebar()

# 2. Control flow routing logic based on user interaction states
if submit_triggered:
    # Initialize a loading spinner while the Gemini multi-agent loop runs
    with st.spinner("🤖 Engaging Multi-Agent Grid & Extracting Grounded Insights..."):
        try:
            # Query the backend multi-agent pipeline with user-supplied parameter inputs
            live_agent_payload = run_multi_agent_pipeline(form_inputs)
            
            # Map the returned expert data dictionary back into your UI layout components (Task 4.3)
            render_dashboard_layout(live_agent_payload)
            
        except Exception as e:
            # Gracefully catch and display errors occurring during the agent pipeline execution
            st.error(f"Critical execution fault during multi-agent orchestration: {e}")
else:
    # Default initialization state when the user lands on the dashboard
    # Displays welcoming guidelines instead of blank panel layouts
    render_dashboard_layout()
