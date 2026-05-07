import pandas as pd
import geopandas as gpd
import streamlit as st
import os

@st.cache_data
def load_crop_data():
    """Loads the crop production dataset."""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crop_production.csv')
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error(f"Dataset not found at {data_path}. Please run generate_dummy_data.py first.")
        return pd.DataFrame()

@st.cache_data
def load_geojson_data():
    """Loads the Nepal district GeoJSON data."""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'nepal_districts.geojson')
    try:
        gdf = gpd.read_file(data_path)
        return gdf
    except FileNotFoundError:
        st.error(f"GeoJSON not found at {data_path}. Please run generate_dummy_data.py first.")
        return gpd.GeoDataFrame()

def get_unique_districts(df):
    if not df.empty:
        return sorted(df['District'].unique())
    return []

def get_unique_provinces(df):
    if not df.empty:
        return sorted(df['Province'].unique())
    return []

def get_unique_crops(df):
    if not df.empty:
        return sorted(df['Crop'].unique())
    return []

def get_unique_months(df):
    if not df.empty and 'Planting_Month' in df.columns:
        return sorted(df['Planting_Month'].dropna().unique())
    return []
