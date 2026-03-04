import pandas as pd
import numpy as np

def format_eur(value: float) -> str:
    return f"€{value:,.0f}"

def calculate_accuracy(df: pd.DataFrame) -> float:
    pass

def calculate_mape(df: pd.DataFrame) -> float:
    pass

def calculate_rmse(df: pd.DataFrame) -> float:
    pass

def get_top_error_skus(df: pd.DataFrame, top_n: int = 5):
    pass