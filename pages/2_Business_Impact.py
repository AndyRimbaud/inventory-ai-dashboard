import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data.mock_data_generator import generate_mock_data
from services.kpi_engine import calculate_accuracy, format_eur
from services.financial_engine import calculate_financials


st.set_page_config(page_title="Business Impact", layout="wide")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df_inventory, df_skus, df_warehouses = generate_mock_data()

accuracy = calculate_accuracy(df_inventory)
financials = calculate_financials(accuracy)

# ---------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------

st.title("💼 Business Impact")

st.markdown(
"""
Quantifiable return on investment, operational savings, and multi-year
cash-flow projections for the AI inventory reconciliation system.
"""
)

st.divider()

# ---------------------------------------------------
# EXECUTIVE KPI SUMMARY
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Year 1 Total Benefit",
        format_eur(financials["total_benefit"]),
        "Recovered shrink + operational savings"
    )

with col2:
    st.metric(
        "Year 1 Investment",
        format_eur(financials["total_cost"]),
        "Hardware + SaaS + deployment"
    )

with col3:
    st.metric(
        "Blended ROI (Year 1)",
        f"{financials['roi']:.1f}%"
    )

with col4:
    st.metric(
        "Capital Payback Time",
        f"{financials['payback_months']:.1f} months"
    )

st.divider()

# ---------------------------------------------------
# VALUE CREATION WATERFALL
# ---------------------------------------------------

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
    connector={"line": {"color": "gray"}}
))

fig.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# PAYBACK CURVE
# ---------------------------------------------------

st.subheader("Cumulative Cost vs Savings (36 Months)")

months = list(range(1, 37))

monthly_savings = financials["total_benefit"] / 12
investment = financials["total_cost"]

cumulative_savings = []
cumulative_cost = []

for m in months:
    cumulative_savings.append(monthly_savings * m)
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
    name="Initial Investment",
    line=dict(color="red", dash="dash")
))

fig.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# 3 YEAR PROJECTION
# ---------------------------------------------------

st.subheader("3-Year Value Projection")

years = ["Year 1 (Pilot)", "Year 2 (Optimized)", "Year 3 (Scaled)"]

benefits = [
    financials["total_benefit"],
    financials["total_benefit"] * 1.8,
    financials["total_benefit"] * 2.5
]

fig = px.bar(
    x=years,
    y=benefits,
    labels={"x": "Year", "y": "Total Value (EUR)"},
    text_auto=".2s",
    template="plotly_dark"
)

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# ROI EXPLANATION
# ---------------------------------------------------

st.subheader("ROI Sensitivity Explanation")

st.markdown(
"""
### Financial Mechanics

**AI Accuracy Linkage**

Gross savings scale with detection accuracy.  
Higher accuracy leads directly to increased shrink recovery.

---

**Operational Ramp**

Year 1 models a learning phase while warehouse operators
adopt the system.

---

**CapEx vs OpEx**

Hardware deployment is a one-time capital expense.  
The SaaS platform is an operational cost.

---

**Compounding Value**

Years 2 and 3 capture additional value as the AI model
improves and operational processes stabilize.
"""
)
