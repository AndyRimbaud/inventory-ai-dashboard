import streamlit as st
import plotly.express as px
from data.mock_data_generator import generate_mock_data
from services.kpi_engine import (
    calculate_accuracy,
    calculate_mape,
    calculate_rmse,
    get_top_error_skus
)

st.set_page_config(page_title="Prototype Intelligence", layout="wide")

st.title("Prototype Intelligence")
st.markdown("Visualizing AI model performance on inventory reconciliation.")

# Load Data
df_inventory, df_skus, df_warehouses = generate_mock_data()

# Compute Metrics
accuracy = calculate_accuracy(df_inventory)
mape = calculate_mape(df_inventory)
rmse = calculate_rmse(df_inventory)

# Display Metrics
st.subheader("Model Performance KPIs")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Accuracy (%)", value=f"{accuracy}%")

with col2:
    st.metric(label="MAPE (%)", value=f"{mape}%")

with col3:
    st.metric(label="RMSE (units)", value=f"{rmse}")

st.divider()

# Top Error SKUs Table
st.subheader("Top Error SKUs")
top_errors = get_top_error_skus(df_inventory)
st.dataframe(top_errors, use_container_width=True)

st.divider()

# Discrepancy Distribution Chart
st.subheader("Discrepancy Distribution")
st.markdown("Histogram showing the distribution of discrepancy values across the inventory logs.")

fig = px.histogram(
    df_inventory, 
    x="unit_discrepancy", 
    nbins=20,
    title="Unit Discrepancy Frequency",
    labels={'unit_discrepancy': 'Unit Discrepancy', 'count': 'Frequency'},
    color_discrete_sequence=['indigo']
)

st.plotly_chart(fig, use_container_width=True)
