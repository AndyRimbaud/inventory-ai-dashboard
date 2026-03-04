import streamlit as st

st.set_page_config(
    page_title="AI Inventory Intelligence",
    layout="wide"
)

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>

.main {
    background-color:#0e1117;
}

.metric-card{
    background-color:#111111;
    border:1px solid #2a2a2a;
    border-radius:12px;
    padding:22px;
}

.metric-title{
    font-size:14px;
    color:#9aa0a6;
}

.metric-value{
    font-size:36px;
    font-weight:700;
}

.metric-tag{
    font-size:12px;
    color:#4ade80;
}

.section-title{
    font-size:22px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

st.title("📦 AI Inventory Intelligence Platform")

st.markdown("""
Operational analytics platform for validating AI-powered inventory reconciliation.

Use the navigation sidebar to explore:

• **Prototype Intelligence** — Model performance diagnostics  
• **Business Impact** — Financial ROI modeling  
• **Pilot Simulator** — Interactive scenario simulation
""")

st.divider()

st.subheader("Platform Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🤖 Prototype Intelligence
    Diagnose AI detection performance across SKUs, warehouses and time.

    Includes:
    - Accuracy metrics
    - Error heatmaps
    - Detection distributions
    """)

with col2:
    st.markdown("""
    ### 💼 Business Impact
    Quantify the economic value of AI deployment.

    Includes:
    - ROI modelling
    - Payback curves
    - Financial breakdown
    """)

with col3:
    st.markdown("""
    ### 🎛 Pilot Simulator
    Test different deployment scenarios.

    Includes:
    - Accuracy simulation
    - Multi-warehouse scaling
    - ROI sensitivity
    """)