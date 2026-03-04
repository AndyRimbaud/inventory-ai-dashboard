# pages/3_Pilot_Simulator.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from services.financial_engine import calculate_financials
from services.kpi_engine import format_eur, calculate_accuracy
from data.mock_data_generator import generate_mock_data

# -------------------------
# Page config & helpers
# -------------------------
st.set_page_config(page_title="Pilot Simulator", layout="wide")

@st.cache_data
def load_data():
    return generate_mock_data()

def safe_payback_display(payback):
    """Return friendly string for payback (handle infinity)."""
    if payback is None or payback == float("inf"):
        return "N/A"
    try:
        return f"{payback:.1f} months"
    except Exception:
        return str(payback)

def scenario_summary_to_df(label, financials, accuracy, warehouses):
    return {
        "scenario": label,
        "accuracy_pct": accuracy,
        "warehouses": warehouses,
        "total_benefit": financials["total_benefit"],
        "total_cost": financials["total_cost"],
        "roi_pct": financials["roi"],
        "payback_months": financials["payback_months"],
        "recovered_shrink": financials["recovered_shrink"],
        "audit_savings": financials["audit_savings"],
        "error_savings": financials["error_savings"]
    }

# -------------------------
# Load baseline dataset
# -------------------------
df_inventory, df_skus, df_warehouses = load_data()

dataset_accuracy = calculate_accuracy(df_inventory)

# -------------------------
# Sidebar - controls
# -------------------------
st.sidebar.header("Pilot Simulator — Controls")

# Option to use dataset-derived accuracy as default
use_dataset_accuracy = st.sidebar.checkbox(
    "Start from dataset accuracy (recommended)", value=True
)

default_acc = float(dataset_accuracy) if use_dataset_accuracy and dataset_accuracy > 0 else 92.0

# Primary scenario controls (A)
st.sidebar.markdown("### Scenario A (Primary)")
acc_a = st.sidebar.slider("Model Accuracy (%) — A", 80.0, 98.0, default_acc, 0.5)
wh_a = st.sidebar.slider("Warehouses — A", 1, 50, 1, 1)

# Comparison scenario controls (B)
st.sidebar.markdown("### Scenario B (Comparison)")
enable_b = st.sidebar.checkbox("Enable comparison scenario (B)", value=False)
if enable_b:
    acc_b = st.sidebar.slider("Model Accuracy (%) — B", 80.0, 98.0, 90.0, 0.5, key="acc_b")
    wh_b = st.sidebar.slider("Warehouses — B", 1, 50, 3, 1, key="wh_b")
else:
    acc_b = None
    wh_b = None

# Simulation horizon
st.sidebar.markdown("### Simulation Horizon")
horizon_months = st.sidebar.selectbox("Projection months", [12, 24, 36, 60], index=2)

# Quick presets
st.sidebar.markdown("---")
if st.sidebar.button("Preset: conservative (80% / 1 wh)"):
    acc_a, wh_a = 80.0, 1
if st.sidebar.button("Preset: optimistic (95% / 5 wh)"):
    acc_a, wh_a = 95.0, 5

st.sidebar.markdown("---")
st.sidebar.caption("All financial calculations are centralized in services/financial_engine.py")

# -------------------------
# Compute financials via engine (single source of truth)
# -------------------------
fin_a = calculate_financials(acc_a, warehouses=wh_a)
if enable_b:
    fin_b = calculate_financials(acc_b, warehouses=wh_b)

# -------------------------
# Top-level layout & KPIs
# -------------------------
st.title("🎛️ Pilot Simulator — Scenario Modeling")

st.markdown(
    f"**Dataset-derived accuracy:** {dataset_accuracy:.2f}% — "
    "use it as a starting point, or change the sliders on the left to run scenarios."
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        label="Scenario A — ROI",
        value=f"{fin_a['roi']:.1f}%",
        delta=None
    )

with k2:
    st.metric(
        label="Scenario A — Payback",
        value=safe_payback_display(fin_a["payback_months"])
    )

with k3:
    st.metric(
        label="Scenario A — Total Benefit",
        value=format_eur(fin_a["total_benefit"])
    )

with k4:
    st.metric(
        label="Scenario A — Total Cost",
        value=format_eur(fin_a["total_cost"])
    )

if enable_b:
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.metric("Scenario B — ROI", f"{fin_b['roi']:.1f}%")
    with b2:
        st.metric("Scenario B — Payback", safe_payback_display(fin_b["payback_months"]))
    with b3:
        st.metric("Scenario B — Total Benefit", format_eur(fin_b["total_benefit"]))
    with b4:
        st.metric("Scenario B — Total Cost", format_eur(fin_b["total_cost"]))

st.divider()

# -------------------------
# ROI vs Accuracy Curve (for selected warehouse scale)
# -------------------------
st.subheader("ROI Sensitivity — Accuracy vs ROI")

# Build ROI curve for the currently selected warehouse multiplier(s)
accuracies = np.arange(80.0, 98.01, 0.5).round(2)

rows = []
for a in accuracies:
    f = calculate_financials(float(a), warehouses=wh_a)
    rows.append({"accuracy": a, "roi": f["roi"], "warehouses": wh_a, "scenario": "A (scale)"})
df_curve_a = pd.DataFrame(rows)

fig = px.line(
    df_curve_a,
    x="accuracy",
    y="roi",
    labels={"accuracy": "Accuracy (%)", "roi": "ROI (%)"},
    title=f"ROI vs Accuracy (Scale = {wh_a} warehouse{'s' if wh_a>1 else ''})",
    markers=True
)

# mark the current chosen accuracy for A
fig.add_vline(x=acc_a, line_dash="dash", line_color="green", annotation_text="A", annotation_position="top left")

# If comparison scenario enabled, overlay B curve
if enable_b:
    rows_b = []
    for a in accuracies:
        f = calculate_financials(float(a), warehouses=wh_b)
        rows_b.append({"accuracy": a, "roi": f["roi"], "warehouses": wh_b, "scenario": "B (scale)"})
    df_curve_b = pd.DataFrame(rows_b)
    fig.add_trace(go.Scatter(
        x=df_curve_b["accuracy"],
        y=df_curve_b["roi"],
        mode="lines+markers",
        name=f"Scenario B (scale={wh_b})",
        line=dict(dash="dot", color="orange")
    ))
    # mark B current
    fig.add_vline(x=acc_b, line_dash="dash", line_color="orange", annotation_text="B", annotation_position="top right")

fig.update_layout(template="plotly_dark", height=420)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------
# Scenario Comparison Table & Bar breakdown
# -------------------------
st.subheader("Scenario Comparison")

rows = []
rows.append(scenario_summary_to_df("A", fin_a, acc_a, wh_a))
if enable_b:
    rows.append(scenario_summary_to_df("B", fin_b, acc_b, wh_b))

df_summary = pd.DataFrame(rows).set_index("scenario")

# Format display-friendly table
df_display = df_summary.copy()
df_display["total_benefit"] = df_display["total_benefit"].apply(lambda v: format_eur(v))
df_display["total_cost"] = df_display["total_cost"].apply(lambda v: format_eur(v))
df_display["recovered_shrink"] = df_display["recovered_shrink"].apply(lambda v: format_eur(v))
df_display["audit_savings"] = df_display["audit_savings"].apply(lambda v: format_eur(v))
df_display["error_savings"] = df_display["error_savings"].apply(lambda v: format_eur(v))
df_display["payback_months"] = df_display["payback_months"].apply(safe_payback_display)
df_display["roi_pct"] = df_display["roi_pct"].apply(lambda v: f"{v:.1f}%")

st.dataframe(df_display, use_container_width=True)

# Download CSV button
csv_bytes = df_summary.reset_index().to_csv(index=False).encode("utf-8")
st.download_button("Download scenario CSV", csv_bytes, "pilot_simulator_scenarios.csv", "text/csv")

st.divider()

# -------------------------
# Visual breakdown (stacked bar) per scenario
# -------------------------
st.subheader("Savings Breakdown by Category")

# Prepare bar chart dataset
bars = []
bars.append({
    "scenario": "A",
    "category": "Recovered Shrink",
    "value": fin_a["recovered_shrink"]
})
bars.append({
    "scenario": "A",
    "category": "Audit Savings",
    "value": fin_a["audit_savings"]
})
bars.append({
    "scenario": "A",
    "category": "Error Savings",
    "value": fin_a["error_savings"]
})

if enable_b:
    bars.append({
        "scenario": "B",
        "category": "Recovered Shrink",
        "value": fin_b["recovered_shrink"]
    })
    bars.append({
        "scenario": "B",
        "category": "Audit Savings",
        "value": fin_b["audit_savings"]
    })
    bars.append({
        "scenario": "B",
        "category": "Error Savings",
        "value": fin_b["error_savings"]
    })

df_bars = pd.DataFrame(bars)

fig = px.bar(
    df_bars,
    x="scenario",
    y="value",
    color="category",
    title="Savings Composition (EUR)",
    labels={"value": "EUR", "scenario": "Scenario"},
    text_auto=".2s"
)
fig.update_layout(template="plotly_dark", height=420)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------
# Quick operational note & guidance for business users
# -------------------------
st.subheader("Operational Guidance")

st.markdown(
    """
- **If ROI is high and Payback is short**: prioritize a pilot rollout to the warehouses with the highest shrink.
- **If Payback is long or N/A**: improve model accuracy (retrain / better data) or reduce CapEx.
- **Use the comparison scenario** to show CFO the financial upside of model improvements or scale.
"""
)

# End of file
