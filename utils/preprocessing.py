"""
Data Preprocessing Module
Handles data cleaning, transformation, and feature engineering.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def clean_data(df):
    """Clean and preprocess dataframe."""
    df = df.copy()
    
    # Drop rows with all NaN values
    df = df.dropna(how='all')
    
    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)
    
    # Fill categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
    
    return df

def normalize_numeric(df, columns):
    """Normalize numeric columns to 0-1 range."""
    df = df.copy()
    scaler = MinMaxScaler()
    
    for col in columns:
        if col in df.columns:
            df[col] = scaler.fit_transform(df[[col]])
    
    return df

def calculate_statistics(df):
    """Calculate descriptive statistics."""
    stats = {
        'Mean': df.mean(),
        'Median': df.median(),
        'Std': df.std(),
        'Min': df.min(),
        'Max': df.max(),
        'Quartile_25': df.quantile(0.25),
        'Quartile_75': df.quantile(0.75)
    }
    return pd.DataFrame(stats)

def filter_by_district(df, district):
    """Filter data by district."""
    if 'District' in df.columns:
        return df[df['District'] == district]
    return df

def filter_by_province(df, province):
    """Filter data by province."""
    if 'Province' in df.columns:
        return df[df['Province'] == province]
    return df

def filter_by_season(df, season):
    """Filter data by season."""
    if 'Season' in df.columns:
        return df[df['Season'] == season]
    return df

def filter_by_crop(df, crop):
    """Filter data by crop."""
    if 'Crop' in df.columns:
        return df[df['Crop'] == crop]
    return df

def get_seasonal_data(df):
    """Group data by season."""
    if 'Season' in df.columns:
        return df.groupby('Season').agg({
            'Production': 'sum',
            'Area': 'sum',
            'Yield': 'mean'
        }).reset_index()
    return pd.DataFrame()

def get_district_summary(df):
    """Get summary statistics by district."""
    if 'District' in df.columns:
        return df.groupby('District').agg({
            'Production': 'sum',
            'Area': 'sum',
            'Yield': 'mean'
        }).reset_index().sort_values('Production', ascending=False)
    return pd.DataFrame()

def get_crop_summary(df):
    """Get summary statistics by crop."""
    if 'Crop' in df.columns:
        return df.groupby('Crop').agg({
            'Production': 'sum',
            'Area': 'sum',
            'Yield': 'mean'
        }).reset_index().sort_values('Production', ascending=False)
    return pd.DataFrame()
