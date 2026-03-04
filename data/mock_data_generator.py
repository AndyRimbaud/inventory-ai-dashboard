import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data():
    """Generates mock data for the inventory SaaS application."""
    # 1. Generate Warehouses
    warehouses_data = {
        'warehouse_id': ['WH-001', 'WH-002'],
        'company_id': ['COMP-A', 'COMP-A'],
        'location': ['Berlin', 'Munich']
    }
    df_warehouses = pd.DataFrame(warehouses_data)

    # 2. Generate SKU Master
    skus_data = {
        'sku_id': ['SKU-101', 'SKU-102', 'SKU-103'],
        'product_name': ['Laptop Pro', 'Wireless Mouse', 'Mechanical Keyboard'],
        'product_category': ['Electronics', 'Accessories', 'Accessories'],
        'unit_cost': [1200.0, 25.0, 80.0],
    }
    df_skus = pd.DataFrame(skus_data)
    # Required: annual_holding_cost
    df_skus['annual_holding_cost'] = df_skus['unit_cost'] * 0.20

    # 3. Generate Inventory Logs
    base_date = datetime(2026, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(10)]
    
    logs = []
    snapshot_counter = 1
    for d in dates:
        for w_id in df_warehouses['warehouse_id']:
            for _, sku in df_skus.iterrows():
                erp_count = np.random.randint(50, 200)
                sensor_count = erp_count - np.random.randint(0, 5) # some discrepancy
                unit_discrepancy = erp_count - sensor_count
                
                logs.append({
                    'snapshot_id': f"SNAP-{snapshot_counter:04d}",
                    'date': d,
                    'warehouse_id': w_id,
                    'sku_id': sku['sku_id'],
                    'erp_inventory_count': erp_count,
                    'sensor_inventory_count': sensor_count,
                    'unit_discrepancy': unit_discrepancy
                })
                snapshot_counter += 1
                
    df_inventory = pd.DataFrame(logs)
    
    # Merge SKUs to get product_name, product_category and unit_cost
    df_inventory = df_inventory.merge(
        df_skus[['sku_id', 'product_name', 'product_category', 'unit_cost']], 
        on='sku_id', 
        how='left'
    )
    
    # Calculate discrepancy_value and total_capital_tied
    df_inventory['discrepancy_value'] = df_inventory['unit_discrepancy'] * df_inventory['unit_cost']
    df_inventory['total_capital_tied'] = df_inventory['erp_inventory_count'] * df_inventory['unit_cost']
    
    # Drop unit_cost as it's not in the required schema for inventory_logs
    df_inventory = df_inventory.drop(columns=['unit_cost'])

    return df_inventory, df_skus, df_warehouses


def validate_schema(df_inventory, df_skus, df_warehouses):
    """Validates the dataframes against the SCHEMA.md contract."""
    # Required columns based on SCHEMA.md
    inventory_required = [
        'snapshot_id', 'date', 'warehouse_id', 'sku_id', 'product_name', 
        'product_category', 'erp_inventory_count', 'sensor_inventory_count', 
        'unit_discrepancy', 'discrepancy_value', 'total_capital_tied'
    ]
    
    sku_required = [
        'sku_id', 'product_name', 'product_category', 'unit_cost', 
        'annual_holding_cost'
    ]
    
    warehouse_required = [
        'warehouse_id', 'company_id', 'location'
    ]
    
    # Check inventory
    missing_inv = [col for col in inventory_required if col not in df_inventory.columns]
    if missing_inv:
        raise ValueError(f"Schema Validation Error: inventory_logs missing columns {missing_inv}")
        
    # Check skus
    missing_skus = [col for col in sku_required if col not in df_skus.columns]
    if missing_skus:
        raise ValueError(f"Schema Validation Error: sku_master missing columns {missing_skus}")
        
    # Check warehouses
    missing_wh = [col for col in warehouse_required if col not in df_warehouses.columns]
    if missing_wh:
        raise ValueError(f"Schema Validation Error: warehouse missing columns {missing_wh}")
        
    print("SUCCESS: Schema validation passed for all dataframes.")
    return True

if __name__ == "__main__":
    df_inv, df_sku, df_wh = generate_mock_data()
    validate_schema(df_inv, df_sku, df_wh)
    print("\n--- Final Dataframe Columns ---")
    print("inventory_logs:", list(df_inv.columns))
    print("sku_master:", list(df_sku.columns))
    print("warehouse:", list(df_wh.columns))
