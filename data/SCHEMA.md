# DATA CONTRACT — INVENTORY AI VALIDATION SYSTEM

## inventory_logs dataframe

Required columns:

- snapshot_id: str
- date: datetime
- warehouse_id: str
- sku_id: str
- product_name: str
- product_category: str
- erp_inventory_count: int
- sensor_inventory_count: int
- unit_discrepancy: int
- discrepancy_value: float
- total_capital_tied: float

## sku_master dataframe

Required columns:

- sku_id: str
- product_name: str
- product_category: str
- unit_cost: float
- annual_holding_cost: float

## warehouse dataframe

Required columns:

- warehouse_id: str
- company_id: str
- location: str