import streamlit as st
import pandas as pd
import plotly.express as px

from services.financial_engine import calculate_financials
from services.kpi_engine import format_eur

st.set_page_config(page_title="Pilot Simulator", layout="wide")

st.title("🎛️ Pilot Simulator")
st.markdown("Interactive simulation tool for forecasting financial impact based on AI accuracy and scale.")

# User Controls
st.sidebar.header("Simulation Parameters")
accuracy = st.sidebar.slider("Model Accuracy (%)", 80.0, 98.0, 92.0, 0.5)
warehouses = st.sidebar.slider("Number of Warehouses", 1, 10, 1)

# Financial Simulation Base
base_financials = calculate_financials(accuracy)

# Scale savings by warehouses
total_benefit = base_financials["total_benefit"] * warehouses
total_cost = base_financials["total_cost"] * warehouses

# Compute Scaled ROI and Payback
# [SELF-AUDIT NOTE: This duplicates financial logic locally, violating the protocol.]
roi = ((total_benefit - total_cost) / total_cost) * 100
payback_months = total_cost / (total_benefit / 12) if total_benefit > 0 else float('inf')

# Display Metrics
st.subheader(f"Simulated Impact ({warehouses} Warehouse{'s' if warehouses > 1 else ''})")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="ROI (%)", value=f"{roi:.1f}%")

with col2:
    st.metric(label="Payback (months)", value=f"{payback_months:.1f}")

with col3:
    st.metric(label="Total Benefit (EUR)", value=format_eur(total_benefit))

st.divider()

# ROI vs Accuracy Curve
st.subheader("ROI vs Accuracy Curve")
st.markdown("Projected ROI scaled across variable accuracy thresholds.")

# Generate range of accuracies
accuracies = list(range(80, 99))
roi_data = []

for acc in accuracies:
    # Compute base for this accuracy
    fin = calculate_financials(float(acc))
    t_ben = fin["total_benefit"] * warehouses
    t_cost = fin["total_cost"] * warehouses
    
    # Duplicated ROI logic for the curve
    r = ((t_ben - t_cost) / t_cost) * 100 if t_cost > 0 else 0
    
    roi_data.append({
        "Accuracy (%)": acc,
        "ROI (%)": r
    })

df_curve = pd.DataFrame(roi_data)

fig = px.line(
    df_curve, 
    x="Accuracy (%)", 
    y="ROI (%)", 
    title=f"ROI Curve for {warehouses} Warehouse(s)",
    markers=True
)

# Highlight current accuracy
fig.add_vline(x=accuracy, line_dash="dash", line_color="red", annotation_text="Current Simulator Setting")

st.plotly_chart(fig, use_container_width=True)
