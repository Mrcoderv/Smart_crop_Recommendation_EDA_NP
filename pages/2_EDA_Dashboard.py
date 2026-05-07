"""
EDA Dashboard Page - Exploratory Data Analysis with interactive visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_crop_data, load_climate_data
from utils.preprocessing import (
    clean_data, get_district_summary, get_crop_summary, get_seasonal_data,
    filter_by_district, filter_by_province, filter_by_season, filter_by_crop
)
from utils.visualization import (
    create_bar_chart, create_line_chart, create_pie_chart, create_scatter_plot,
    create_correlation_heatmap, create_histogram, create_box_plot, create_area_chart
)

st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")

# Load custom CSS
with open("assets/styles/custom.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #27ae60 0%, #1e5631 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>📊 EDA Dashboard</h1>
        <p style='color: #d5f4e6; margin: 10px 0 0 0;'>Comprehensive Data Analysis & Insights</p>
    </div>
""", unsafe_allow_html=True)

# Load data
crop_data = load_crop_data()

if crop_data.empty:
    st.error("❌ No data available. Please run generate_dummy_data.py")
    st.stop()

# Data cleaning
crop_data = clean_data(crop_data)

# Sidebar Filters
st.sidebar.markdown("### 🔍 Filters")
selected_district = st.sidebar.selectbox("Select District", ["All"] + crop_data['District'].unique().tolist())
selected_crop = st.sidebar.selectbox("Select Crop", ["All"] + crop_data['Crop'].unique().tolist())
selected_season = st.sidebar.selectbox("Select Season", ["All"] + crop_data['Season'].unique().tolist() if 'Season' in crop_data.columns else ["All"])

# Apply filters
filtered_data = crop_data.copy()
if selected_district != "All":
    filtered_data = filter_by_district(filtered_data, selected_district)
if selected_crop != "All":
    filtered_data = filter_by_crop(filtered_data, selected_crop)
if selected_season != "All" and 'Season' in crop_data.columns:
    filtered_data = filter_by_season(filtered_data, selected_season)

# KPI Cards
st.markdown("### 📈 Key Performance Indicators")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    total_records = len(filtered_data)
    st.metric("📋 Records", f"{total_records:,}")

with kpi_col2:
    avg_production = filtered_data['Production'].mean() if 'Production' in filtered_data.columns else 0
    st.metric("🌾 Avg Production", f"{avg_production:,.0f}")

with kpi_col3:
    avg_yield = filtered_data['Yield'].mean() if 'Yield' in filtered_data.columns else 0
    st.metric("📊 Avg Yield", f"{avg_yield:,.2f}")

with kpi_col4:
    total_area = filtered_data['Area'].sum() if 'Area' in filtered_data.columns else 0
    st.metric("🗺️ Total Area", f"{total_area:,.0f}")

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Crop Analysis", "District Analysis", "Seasonal Analysis", "Production Trends", "Yield Analysis", "Correlations"]
)

# Tab 1: Crop Analysis
with tab1:
    st.markdown("### 🌾 Crop Production Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_summary = get_crop_summary(filtered_data)
        if not crop_summary.empty:
            fig = create_bar_chart(
                crop_summary.head(10), 'Crop', 'Production',
                'Top 10 Crops by Production'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not crop_summary.empty:
            fig = create_pie_chart(
                crop_summary.head(10), 'Production', 'Crop',
                'Crop Production Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Crop yield analysis
    st.markdown("### Crop Yield Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        if not crop_summary.empty:
            fig = create_bar_chart(
                crop_summary.head(10), 'Crop', 'Yield',
                'Average Yield by Crop'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not crop_summary.empty:
            fig = create_scatter_plot(
                crop_summary, 'Area', 'Production',
                'Area vs Production by Crop', color='Crop'
            )
            st.plotly_chart(fig, use_container_width=True)

# Tab 2: District Analysis
with tab2:
    st.markdown("### 📍 District-wise Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        district_summary = get_district_summary(filtered_data)
        if not district_summary.empty:
            fig = create_bar_chart(
                district_summary.head(15), 'District', 'Production',
                'Top 15 Districts by Production'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not district_summary.empty:
            fig = create_bar_chart(
                district_summary.head(15), 'District', 'Yield',
                'Average Yield by District'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Area analysis
    st.markdown("### Area Cultivation by District")
    col1, col2 = st.columns(2)
    
    with col1:
        if not district_summary.empty:
            fig = create_pie_chart(
                district_summary.head(10), 'Area', 'District',
                'Area Distribution (Top 10 Districts)'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not district_summary.empty:
            fig = create_scatter_plot(
                district_summary, 'Area', 'Production',
                'District: Area vs Production', color='Yield'
            )
            st.plotly_chart(fig, use_container_width=True)

# Tab 3: Seasonal Analysis
with tab3:
    st.markdown("### 🌤️ Seasonal Crop Analysis")
    
    if 'Season' in filtered_data.columns:
        seasonal_data = get_seasonal_data(filtered_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not seasonal_data.empty:
                fig = create_bar_chart(
                    seasonal_data, 'Season', 'Production',
                    'Production by Season'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if not seasonal_data.empty:
                fig = create_pie_chart(
                    seasonal_data, 'Production', 'Season',
                    'Seasonal Production Distribution'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Seasonal area analysis
        st.markdown("### Seasonal Cultivation Patterns")
        col1, col2 = st.columns(2)
        
        with col1:
            if not seasonal_data.empty:
                fig = create_bar_chart(
                    seasonal_data, 'Season', 'Area',
                    'Cultivation Area by Season'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if not seasonal_data.empty:
                fig = create_bar_chart(
                    seasonal_data, 'Season', 'Yield',
                    'Average Yield by Season'
                )
                st.plotly_chart(fig, use_container_width=True)

# Tab 4: Production Trends
with tab4:
    st.markdown("### 📈 Production Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_data.empty and 'Production' in filtered_data.columns:
            fig = create_histogram(
                filtered_data, 'Production',
                'Production Distribution', nbins=30
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not filtered_data.empty and 'Yield' in filtered_data.columns:
            fig = create_histogram(
                filtered_data, 'Yield',
                'Yield Distribution', nbins=30
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Box plots
    st.markdown("### Production & Yield Box Plots")
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_data.empty and 'District' in filtered_data.columns:
            top_districts = filtered_data['District'].value_counts().head(10).index
            df_top = filtered_data[filtered_data['District'].isin(top_districts)]
            fig = create_box_plot(df_top, 'Production', 'District', 'Production by District')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not filtered_data.empty and 'Crop' in filtered_data.columns:
            top_crops = filtered_data['Crop'].value_counts().head(10).index
            df_top = filtered_data[filtered_data['Crop'].isin(top_crops)]
            fig = create_box_plot(df_top, 'Yield', 'Crop', 'Yield by Crop')
            st.plotly_chart(fig, use_container_width=True)

# Tab 5: Yield Analysis
with tab5:
    st.markdown("### 🎯 Yield Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Crop' in filtered_data.columns and 'Yield' in filtered_data.columns:
            crop_yield = filtered_data.groupby('Crop')['Yield'].mean().sort_values(ascending=False)
            fig = create_bar_chart(
                crop_yield.reset_index(), 'Crop', 'Yield',
                'Average Yield by Crop'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'District' in filtered_data.columns and 'Yield' in filtered_data.columns:
            district_yield = filtered_data.groupby('District')['Yield'].mean().sort_values(ascending=False).head(10)
            fig = create_bar_chart(
                district_yield.reset_index(), 'District', 'Yield',
                'Top 10 Districts by Average Yield'
            )
            st.plotly_chart(fig, use_container_width=True)

# Tab 6: Correlations
with tab6:
    st.markdown("### 🔗 Correlation Analysis")
    
    if len(filtered_data.select_dtypes(include=[np.number]).columns) > 1:
        fig = create_correlation_heatmap(filtered_data)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div style='background: #f0f9f7; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60;'>
                <h4>📊 Interpretation:</h4>
                <ul>
                    <li>Values close to <strong>+1</strong> indicate strong positive correlation (variables increase together)</li>
                    <li>Values close to <strong>-1</strong> indicate strong negative correlation (one increases as other decreases)</li>
                    <li>Values close to <strong>0</strong> indicate no correlation</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Data Table
st.markdown("### 📋 Data Preview")
st.dataframe(filtered_data.head(20), use_container_width=True)

# Summary Statistics
st.markdown("### 📊 Summary Statistics")
st.dataframe(filtered_data.describe(), use_container_width=True)
