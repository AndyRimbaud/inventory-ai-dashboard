# Constants in EUR
BASE_REVENUE = 5_000_000
SHRINK_RATE = 0.015
AUDIT_COST = 60_000
ERROR_COST = 40_000

HARDWARE_COST = 15_000
SAAS_COST = 5_000
IMPLEMENTATION_COST = 10_000
TRAINING_COST = 5_000

REFERENCE_ACCURACY = 95.0
MAX_RECOVERY_RATE = 0.50

# services/financial_engine.py
# (mantén las constantes arriba exactamente como ya las tienes)

def calculate_financials(accuracy: float, warehouses: int = 1):
    """
    Central financial calculation.
    Validates inputs and returns a dict with keys:
    recovered_shrink, audit_savings, error_savings, total_benefit, total_cost, roi, payback_months
    """

    # input validation
    try:
        accuracy = float(accuracy)
    except Exception:
        raise ValueError(f"accuracy must be numeric (got {accuracy!r})")

    try:
        warehouses = int(warehouses)
    except Exception:
        raise ValueError(f"warehouses must be integer (got {warehouses!r})")

    if accuracy < 0 or accuracy > 100:
        raise ValueError(f"accuracy out of bounds: {accuracy}. Expected between 0 and 100 (percentage).")

    if warehouses <= 0:
        raise ValueError(f"warehouses must be >= 1 (got {warehouses})")

    # --- calculation (existing logic) ---
    shrink_baseline = BASE_REVENUE * SHRINK_RATE

    recovered_shrink = (
        shrink_baseline
        * MAX_RECOVERY_RATE
        * (accuracy / REFERENCE_ACCURACY)
    )

    audit_savings = AUDIT_COST * (accuracy / REFERENCE_ACCURACY) * 0.25
    error_savings = ERROR_COST * (accuracy / REFERENCE_ACCURACY) * 0.20

    total_benefit = recovered_shrink + audit_savings + error_savings
    total_cost = HARDWARE_COST + SAAS_COST + IMPLEMENTATION_COST + TRAINING_COST

    # scale by warehouses
    total_benefit *= warehouses
    total_cost *= warehouses

    # guard against division by zero
    if total_cost == 0:
        roi = float("inf")
    else:
        roi = ((total_benefit - total_cost) / total_cost) * 100

    monthly_savings = total_benefit / 12.0
    payback_months = total_cost / monthly_savings if monthly_savings > 0 else float("inf")

    return {
        "recovered_shrink": recovered_shrink * warehouses,
        "audit_savings": audit_savings * warehouses,
        "error_savings": error_savings * warehouses,
        "total_benefit": total_benefit,
        "total_cost": total_cost,
        "roi": roi,
        "payback_months": payback_months,
    }