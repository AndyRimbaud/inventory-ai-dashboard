import pandas as pd
import numpy as np

def format_eur(value: float) -> str:
    return f"€{value:,.0f}"

def calculate_accuracy(df: pd.DataFrame) -> float:
    valid_df = df[df['erp_inventory_count'] > 0]
    if valid_df.empty:
        return 0.0
    
    abs_diff = np.abs(valid_df['erp_inventory_count'] - valid_df['sensor_inventory_count'])
    accuracy = (1 - np.mean(abs_diff / valid_df['erp_inventory_count'])) * 100
    return round(float(accuracy), 2)

def calculate_mape(df: pd.DataFrame) -> float:
    valid_df = df[df['erp_inventory_count'] > 0]
    if valid_df.empty:
        return 0.0
        
    actual = valid_df['erp_inventory_count']
    predicted = valid_df['sensor_inventory_count']
    
    mape = np.mean(np.abs(actual - predicted) / actual) * 100
    return round(float(mape), 2)

def calculate_rmse(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
        
    actual = df['erp_inventory_count']
    predicted = df['sensor_inventory_count']
    
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    return round(float(rmse), 2)

def get_top_error_skus(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
        
    df_copy = df.copy()
    df_copy['abs_discrepancy'] = df_copy['discrepancy_value'].abs()
    
    grouped = df_copy.groupby(['sku_id', 'product_name'])['abs_discrepancy'].sum().reset_index()
    return grouped.sort_values(by='abs_discrepancy', ascending=False).head(top_n)