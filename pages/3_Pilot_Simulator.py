import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data.mock_data_generator import generate_mock_data
from services.kpi_engine import calculate_accuracy, format_eur
from services.financial_engine import calculate_financials

st.set_page_config(page_title="Business Impact", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------

df_inventory, df_skus, df_warehouses = generate_mock_data()

accuracy = calculate_accuracy(df_inventory)
financials = calculate_financials(accuracy)

# -----------------------------
# PAGE HEADER
# -----------------------------

st.title("Business Impact")

st.markdown(
"""
Quantifiable return on investment, operational savings, and multi-year
financial projections generated from the AI inventory reconciliation system.
"""
)

st.divider()

# -----------------------------
# EXECUTIVE SUMMARY
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Year 1 Total Benefit",
        format_eur(financials["total_benefit"])
    )

with col2:
    st.metric(
        "Year 1 Investment",
        format_eur(financials["total_cost"])
    )

with col3:
    st.metric(
        "Blended ROI",
        f"{financials['roi']:.1f}%"
    )

with col4:
    st.metric(
        "Payback Time",
        f"{financials['payback_months']:.1f} months"
    )

st.divider()

# -----------------------------
# WATERFALL
# -----------------------------

st.subheader("Year 1 Value Creation")

fig = go.Figure(go.Waterfall(
    orientation="v",
    measure=["absolute", "relative", "relative", "relative", "total"],
    x=[
        "Investment",
        "Recovered Shrink",
        "Audit Savings",
        "Error Reduction",
        "Net Value"
    ],
    y=[
        -financials["total_cost"],
        financials["recovered_shrink"],
        financials["audit_savings"],
        financials["error_savings"],
        0
    ],
))

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# PAYBACK CURVE
# -----------------------------

st.subheader("Cumulative Cost vs Savings (36 Months)")

months = list(range(1,37))

monthly_savings = financials["total_benefit"] / 12
investment = financials["total_cost"]

cumulative_savings = []
cumulative_cost = []

for m in months:
    cumulative_savings.append(monthly_savings*m)
    cumulative_cost.append(investment)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=months,
    y=cumulative_savings,
    name="Cumulative Savings",
    line=dict(color="green", width=3)
))

fig.add_trace(go.Scatter(
    x=months,
    y=cumulative_cost,
    name="Investment",
    line=dict(color="red", dash="dash")
))

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# 3 YEAR PROJECTION
# -----------------------------

st.subheader("3-Year Value Projection")

years = ["Year 1", "Year 2", "Year 3"]

values = [
    financials["total_benefit"],
    financials["total_benefit"]*1.8,
    financials["total_benefit"]*2.5
]

fig = px.bar(
    x=years,
    y=values,
    text_auto=".2s",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# ROI EXPLANATION
# -----------------------------

st.subheader("ROI Sensitivity Explanation")

st.markdown("""
**AI Accuracy Linkage**

Financial value scales proportionally with detection accuracy.

---

**Operational Ramp**

Year 1 models adoption and training inside the warehouse.

---

**CapEx vs OpEx**

Hardware is upfront investment while SaaS costs are operational.

---

**Compounding Value**

Years 2 and 3 benefit from improved models and optimized processes.
""")
