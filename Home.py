import streamlit as st
from data.mock_data_generator import generate_mock_data

st.set_page_config(
    page_title="Inventory AI Validation Dashboard",
    layout="wide"
)

st.title("Inventory AI Validation System")

df_inventory, df_skus, df_warehouses = generate_mock_data()

st.subheader("Dataset Preview")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Inventory Logs")
    st.dataframe(df_inventory.head())

with col2:
    st.write("SKU Master")
    st.dataframe(df_skus.head())

with col3:
    st.write("Warehouses")
    st.dataframe(df_warehouses.head())