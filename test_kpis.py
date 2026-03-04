import pandas as pd
from data.mock_data_generator import generate_mock_data
from services.kpi_engine import calculate_accuracy, calculate_mape, calculate_rmse, get_top_error_skus, format_eur

print("Running KPI Engine Tests on Mock Dataset...\n")

df_inv, _, _ = generate_mock_data()

accuracy = calculate_accuracy(df_inv)
mape = calculate_mape(df_inv)
rmse = calculate_rmse(df_inv)
top_skus = get_top_error_skus(df_inv)
formatted_currency = format_eur(123456)

print(f"Accuracy: {accuracy}%")
print(f"MAPE: {mape}%")
print(f"RMSE: {rmse}")
print(f"Formatted EUR Example (123456): {formatted_currency}")
print("\nTop Error SKUs:")
print(top_skus.to_string(index=False))
