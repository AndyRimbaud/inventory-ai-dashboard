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

def calculate_financials(accuracy: float) -> dict:
    shrink_baseline = BASE_REVENUE * SHRINK_RATE
    recovered_shrink = shrink_baseline * MAX_RECOVERY_RATE * (accuracy / REFERENCE_ACCURACY)
    
    audit_savings = AUDIT_COST * (accuracy / REFERENCE_ACCURACY) * 0.25
    error_savings = ERROR_COST * (accuracy / REFERENCE_ACCURACY) * 0.20
    
    total_benefit = recovered_shrink + audit_savings + error_savings
    total_cost = HARDWARE_COST + SAAS_COST + IMPLEMENTATION_COST + TRAINING_COST
    
    roi = ((total_benefit - total_cost) / total_cost) * 100
    
    monthly_savings = total_benefit / 12
    payback_months = total_cost / monthly_savings if monthly_savings > 0 else float('inf')
    
    return {
        "recovered_shrink": recovered_shrink,
        "audit_savings": audit_savings,
        "error_savings": error_savings,
        "total_benefit": total_benefit,
        "total_cost": total_cost,
        "roi": roi,
        "payback_months": payback_months
    }