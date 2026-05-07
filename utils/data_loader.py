"""
Data Loader Module
Handles loading and caching data from CSV and GeoJSON files.
"""

import pandas as pd
import geopandas as gpd
import streamlit as st
from pathlib import Path
import json

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

@st.cache_data
def load_crop_data():
    """Load crop production dataset."""
    try:
        df = pd.read_csv(PROJECT_ROOT / "data" / "crop_production.csv")
        return df
    except FileNotFoundError:
        st.error("Crop data file not found!")
        return pd.DataFrame()

@st.cache_data
def load_climate_data():
    """Load climate dataset."""
    try:
        df = pd.read_csv(PROJECT_ROOT / "data" / "climate_data.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

@st.cache_data
def load_nepal_districts():
    """Load Nepal districts GeoJSON."""
    try:
        gdf = gpd.read_file(PROJECT_ROOT / "data" / "nepal_districts.geojson")
        return gdf
    except FileNotFoundError:
        st.error("Nepal GeoJSON file not found!")
        return gpd.GeoDataFrame()

@st.cache_data
def load_geojson():
    """Load GeoJSON as dictionary."""
    try:
        with open(PROJECT_ROOT / "data" / "nepal_districts.geojson", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("GeoJSON file not found!")
        return None

def get_unique_districts(df):
    """Get unique districts from dataframe."""
    if not df.empty and 'District' in df.columns:
        return sorted(df['District'].unique())
    return []

def get_unique_provinces(df):
    """Get unique provinces from dataframe."""
    if not df.empty and 'Province' in df.columns:
        return sorted(df['Province'].unique())
    return []

def get_unique_crops(df):
    """Get unique crops from dataframe."""
    if not df.empty and 'Crop' in df.columns:
        return sorted(df['Crop'].unique())
    return []

def get_unique_seasons(df):
    """Get unique seasons from dataframe."""
    if not df.empty and 'Season' in df.columns:
        return sorted(df['Season'].dropna().unique())
    return []

def get_districts_list():
    """Get all districts in Nepal."""
    gdf = load_nepal_districts()
    if not gdf.empty:
        districts = sorted(gdf['properties'].apply(lambda x: x.get('DISTRICT', '')).unique().tolist())
        return [d for d in districts if d]
    return []
