"""
GIS Map Page - Interactive mapping and geographical visualization
"""

import streamlit as st
import sys
from pathlib import Path
import folium
from streamlit_folium import st_folium

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_crop_data, load_nepal_districts, load_geojson
from utils.map_utils import (
    create_base_map, add_geojson_layer, add_crop_intensity_markers,
    NEPAL_DISTRICT_COORDS
)

st.set_page_config(page_title="GIS Map", page_icon="🗺️", layout="wide")

# Load custom CSS
with open("assets/styles/custom.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #27ae60 0%, #1e5631 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🗺️ GIS Map Visualization</h1>
        <p style='color: #d5f4e6; margin: 10px 0 0 0;'>Interactive Geographical Analysis of Nepal</p>
    </div>
""", unsafe_allow_html=True)

# Load data
crop_data = load_crop_data()
nepal_gdf = load_nepal_districts()
geojson_data = load_geojson()

if crop_data.empty:
    st.error("❌ No crop data available")
    st.stop()

# Sidebar options
st.sidebar.markdown("### 🎨 Map Options")
map_type = st.sidebar.radio(
    "Select Map Type",
    ["Crop Distribution", "District Intensity", "Production Heatmap"]
)

col1, col2 = st.columns([3, 1])

with col1:
    if map_type == "Crop Distribution":
        st.markdown("### 🌾 Crop Distribution Map")
        
        # Get unique crops
        crops = crop_data['Crop'].unique().tolist()
        selected_crop = st.selectbox("Select Crop", crops)
        
        # Filter data for selected crop
        crop_filtered = crop_data[crop_data['Crop'] == selected_crop]
        
        # Create map
        m = create_base_map()
        
        # Add markers for districts where crop is grown
        for district, group in crop_filtered.groupby('District'):
            if district in NEPAL_DISTRICT_COORDS:
                lat, lon = NEPAL_DISTRICT_COORDS[district]
                production = group['Production'].sum()
                area = group['Area'].sum()
                
                # Determine color based on production
                max_prod = crop_filtered['Production'].max()
                intensity = (production / max_prod) if max_prod > 0 else 0
                
                if intensity > 0.7:
                    color = 'darkgreen'
                elif intensity > 0.4:
                    color = 'green'
                else:
                    color = 'orange'
                
                popup_html = f"""
                <b>{district}</b><br>
                Crop: {selected_crop}<br>
                Production: {production:,.0f}<br>
                Area: {area:,.0f}<br>
                Intensity: {intensity*100:.1f}%
                """
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=5 + intensity * 15,
                    popup=folium.Popup(popup_html, max_width=250),
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
        
        # Add geojson overlay
        if geojson_data:
            folium.GeoJson(
                geojson_data,
                style_function=lambda x: {'color': 'black', 'weight': 1, 'fillOpacity': 0.1}
            ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_folium(m, width=1200, height=600)
    
    elif map_type == "District Intensity":
        st.markdown("### 📍 District Crop Intensity Map")
        
        # Get district production summary
        district_data = crop_data.groupby('District').agg({
            'Production': 'sum',
            'Area': 'sum',
            'Yield': 'mean'
        }).reset_index()
        
        # Create map
        m = create_base_map()
        
        # Add intensity markers
        max_production = district_data['Production'].max()
        
        for idx, row in district_data.iterrows():
            district = row['District']
            if district in NEPAL_DISTRICT_COORDS:
                lat, lon = NEPAL_DISTRICT_COORDS[district]
                production = row['Production']
                intensity = (production / max_production) if max_production > 0 else 0
                
                # Color scale
                if intensity > 0.7:
                    color = 'darkgreen'
                    radius = 15
                elif intensity > 0.4:
                    color = 'green'
                    radius = 12
                else:
                    color = 'orange'
                    radius = 8
                
                popup_html = f"""
                <b>{district}</b><br>
                Total Production: {production:,.0f}<br>
                Total Area: {row['Area']:,.0f}<br>
                Avg Yield: {row['Yield']:.2f}<br>
                Intensity: {intensity*100:.1f}%
                """
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=radius,
                    popup=folium.Popup(popup_html, max_width=250),
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
        
        # Add geojson overlay
        if geojson_data:
            folium.GeoJson(
                geojson_data,
                style_function=lambda x: {'color': 'black', 'weight': 1, 'fillOpacity': 0.05}
            ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_folium(m, width=1200, height=600)
    
    else:  # Production Heatmap
        st.markdown("### 🔥 Production Heatmap by District")
        
        # Create data for heatmap
        district_production = crop_data.groupby('District')['Production'].sum().reset_index()
        
        # Create map
        m = create_base_map()
        
        # Add heatmap data
        heat_data = []
        for idx, row in district_production.iterrows():
            if row['District'] in NEPAL_DISTRICT_COORDS:
                lat, lon = NEPAL_DISTRICT_COORDS[row['District']]
                # Normalize production for heatmap
                normalized = (row['Production'] - district_production['Production'].min()) / (district_production['Production'].max() - district_production['Production'].min())
                heat_data.append([lat, lon, normalized])
        
        # Add heatmap layer
        plugins = st.sidebar.checkbox("Show heatmap layer", value=True)
        
        if heat_data:
            from folium import plugins as folium_plugins
            folium_plugins.HeatMap(heat_data, radius=30, blur=15, max_zoom=13).add_to(m)
        
        # Add geojson overlay
        if geojson_data:
            folium.GeoJson(
                geojson_data,
                style_function=lambda x: {'color': 'black', 'weight': 1, 'fillOpacity': 0.05}
            ).add_to(m)
        
        folium.LayerControl().add_to(m)
        st_folium(m, width=1200, height=600)

with col2:
    st.markdown("### 📊 Legend")
    st.markdown("""
        <div style='background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h4 style='margin-top: 0;'>Color Scale:</h4>
            <div style='margin: 10px 0;'>
                <span style='display: inline-block; width: 20px; height: 20px; background: darkgreen; border-radius: 50%; margin-right: 10px;'></span>
                <span>High Intensity (>70%)</span>
            </div>
            <div style='margin: 10px 0;'>
                <span style='display: inline-block; width: 20px; height: 20px; background: green; border-radius: 50%; margin-right: 10px;'></span>
                <span>Medium Intensity (40-70%)</span>
            </div>
            <div style='margin: 10px 0;'>
                <span style='display: inline-block; width: 20px; height: 20px; background: orange; border-radius: 50%; margin-right: 10px;'></span>
                <span>Low Intensity (<40%)</span>
            </div>
            <hr>
            <p style='font-size: 0.9em; margin: 10px 0;'>
                <strong>Marker size</strong> indicates production volume
            </p>
        </div>
    """, unsafe_allow_html=True)

# District Statistics Table
st.markdown("### 📋 District Statistics")

district_stats = crop_data.groupby('District').agg({
    'Production': 'sum',
    'Area': 'sum',
    'Yield': 'mean',
    'Crop': 'count'
}).reset_index()

district_stats.columns = ['District', 'Total Production', 'Total Area', 'Avg Yield', 'Crop Count']
district_stats = district_stats.sort_values('Total Production', ascending=False)

st.dataframe(district_stats, use_container_width=True)
