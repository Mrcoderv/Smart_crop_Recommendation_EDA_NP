import pandas as pd

def filter_data(df, province=None, district=None, crop=None, season=None, year=None):
    """Filters the dataframe based on provided criteria."""
    filtered_df = df.copy()
    
    if province:
        filtered_df = filtered_df[filtered_df['Province'] == province]
    if district:
        filtered_df = filtered_df[filtered_df['District'] == district]
    if crop:
        filtered_df = filtered_df[filtered_df['Crop'] == crop]
    if season:
        filtered_df = filtered_df[filtered_df['Season'] == season]
    if year:
        filtered_df = filtered_df[filtered_df['Year'] == year]
        
    return filtered_df

def get_summary_stats(df):
    """Calculates summary statistics for the dataset."""
    if df.empty:
        return {}
        
    stats = {
        'total_area': df['Area_Hectares'].sum(),
        'total_production': df['Production_MT'].sum(),
        'avg_yield': df['Yield_Kg_Ha'].mean(),
        'total_districts': df['District'].nunique(),
        'total_crops': df['Crop'].nunique(),
        'top_crop': df.groupby('Crop')['Production_MT'].sum().idxmax(),
        'top_district': df.groupby('District')['Production_MT'].sum().idxmax()
    }
    return stats
