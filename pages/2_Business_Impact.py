import streamlit as st
import pandas as pd
import plotly.express as px

from data.mock_data_generator import generate_mock_data
from services.kpi_engine import calculate_accuracy, format_eur
from services.financial_engine import calculate_financials

st.set_page_config(page_title="Business Impact", layout="wide")

st.title("💼 Business Impact")
st.markdown("Quantifying the financial ROI of the AI validation prototype.")

# Load Data
df_inventory, df_skus, df_warehouses = generate_mock_data()

# Compute Accuracy
accuracy = calculate_accuracy(df_inventory)

# Compute Financial Outputs
financials = calculate_financials(accuracy)

# Display Headline Metrics
st.subheader("Financial Impact Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="ROI (%)", value=f"{financials['roi']:.1f}%")

with col2:
    st.metric(label="Payback (months)", value=f"{financials['payback_months']:.1f}")

with col3:
    st.metric(label="Total Benefit (EUR)", value=format_eur(financials['total_benefit']))

st.divider()

# Breakdown Table & Chart Data Preparation
breakdown_data = {
    "Category": ["Recovered Shrink", "Audit Savings", "Error Savings"],
    "Value (EUR)": [
        financials["recovered_shrink"],
        financials["audit_savings"],
        financials["error_savings"]
    ]
}

df_breakdown = pd.DataFrame(breakdown_data)

# Formatted Display Table
df_display = df_breakdown.copy()
df_display["Value (EUR)"] = df_display["Value (EUR)"].apply(format_eur)

col1, col2 = st.columns(2)

with col1:
    # Display Breakdown Table
    st.subheader("Savings Breakdown")
    st.dataframe(df_display, use_container_width=True, hide_index=True)

with col2:
    # Display Bar Chart
    st.subheader("Savings Contribution")
    fig = px.bar(
        df_breakdown, 
        x="Category", 
        y="Value (EUR)", 
        text_auto=".2s",
        title="Impact by Category",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)
