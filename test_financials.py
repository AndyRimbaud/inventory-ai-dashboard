from services.financial_engine import calculate_financials

print("Running Financial Engine Tests...")
print("\nAccuracy: 92.0")
financials = calculate_financials(92.0)

for key, value in financials.items():
    print(f"{key}: {value:.2f}")
