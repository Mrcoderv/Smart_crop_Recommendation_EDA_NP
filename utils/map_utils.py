"""
Map Utilities Module
Handles GIS mapping and visualization of Nepal districts.
"""

import folium
from folium import plugins
import geopandas as gpd
import pandas as pd
import streamlit as st
import json

def create_base_map(center_lat=27.7172, center_lon=85.3240, zoom_start=7):
    """Create a base Folium map centered on Nepal."""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    return m

def add_geojson_layer(m, geojson_data, column_name='DISTRICT'):
    """Add GeoJSON layer to map."""
    folium.GeoJson(
        geojson_data,
        name='Districts',
        popup=folium.GeoJsonPopup(fields=[column_name]),
        style_function=lambda x: {
            'fillColor': '#7fbc41',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5
        }
    ).add_to(m)
    return m

def create_choropleth_map(gdf, column, title, colormap='YlGn'):
    """Create a choropleth map."""
    m = create_base_map()
    
    if gdf.empty:
        return m
    
    # Convert to Web Mercator projection
    gdf = gdf.to_crs(epsg=4326)
    
    # Create choropleth
    folium.Choropleth(
        geo_data=gdf.geometry.__geo_interface__,
        name=title,
        legend_name=title,
        colormap=colormap
    ).add_to(m)
    
    return m

def add_crop_intensity_markers(m, data_df, district_coords):
    """Add crop intensity markers to map."""
    if data_df.empty:
        return m
    
    for idx, row in data_df.iterrows():
        district = row.get('District', '')
        production = row.get('Production', 0)
        area = row.get('Area', 0)
        
        if district in district_coords:
            lat, lon = district_coords[district]
            
            # Scale intensity (0-1)
            intensity = min(production / data_df['Production'].max(), 1) if data_df['Production'].max() > 0 else 0
            
            # Color based on intensity
            if intensity > 0.7:
                color = 'darkgreen'
            elif intensity > 0.4:
                color = 'green'
            else:
                color = 'orange'
            
            popup_text = f"""
            <b>{district}</b><br>
            Production: {production:,.0f}<br>
            Area: {area:,.0f}<br>
            Intensity: {intensity*100:.1f}%
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=5 + intensity * 10,
                popup=folium.Popup(popup_text, max_width=250),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
    
    return m

def add_weather_markers(m, weather_data, district_coords):
    """Add weather condition markers to map."""
    for district, weather in weather_data.items():
        if district in district_coords and weather:
            lat, lon = district_coords[district]
            
            try:
                current = weather.get('current', {})
                temp = current.get('temperature_2m', 'N/A')
                humidity = current.get('relative_humidity_2m', 'N/A')
                
                popup_text = f"""
                <b>{district}</b><br>
                Temperature: {temp}°C<br>
                Humidity: {humidity}%
                """
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_text, max_width=250),
                    icon=folium.Icon(color='blue', icon='cloud')
                ).add_to(m)
            except:
                pass
    
    return m

def create_seasonal_crop_map(gdf, crop_data, season, colormap='viridis'):
    """Create a map showing crop distribution for a specific season."""
    m = create_base_map()
    
    if crop_data.empty:
        return m
    
    # Filter by season
    season_data = crop_data[crop_data['Season'] == season] if 'Season' in crop_data.columns else crop_data
    
    # Group by district and sum production
    district_production = season_data.groupby('District')['Production'].sum().reset_index()
    
    return m

def add_scale_and_controls(m):
    """Add scale and layer controls to map."""
    folium.LayerControl().add_to(m)
    m.add_child(folium.LatLngPopup())
    return m

def create_district_info_popup(district_name, data_dict):
    """Create detailed popup for district."""
    html = f"""
    <div style="font-family: Arial; font-size: 12px; width: 250px;">
        <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{district_name}</h4>
    """
    
    for key, value in data_dict.items():
        html += f"<p style='margin: 5px 0;'><b>{key}:</b> {value}</p>"
    
    html += "</div>"
    return html

# Nepal district coordinates (latitude, longitude)
NEPAL_DISTRICT_COORDS = {
    'Kathmandu': (27.7172, 85.3240),
    'Pokhara': (28.2096, 83.9856),
    'Lalitpur': (27.6760, 85.3212),
    'Bhaktapur': (27.6721, 85.4121),
    'Dhading': (27.8833, 84.8667),
    'Nuwakot': (27.8333, 85.4333),
    'Makwanpur': (27.5667, 85.3333),
    'Chitwan': (27.5500, 84.9000),
    'Biratnagar': (26.4833, 87.2667),
    'Janakpur': (26.7333, 85.9333),
    'Dhanusha': (26.7500, 85.9333),
    'Morang': (26.5000, 87.4000),
    'Sunsari': (26.5500, 87.1667),
    'Khotang': (27.0500, 87.5500),
    'Ilam': (26.9167, 87.9167),
    'Terathum': (27.2667, 87.1667),
    'Panchthar': (27.2500, 87.7500),
    'Taplejung': (27.3500, 87.7000),
    'Sankhuwasabha': (27.3833, 87.2500),
    'Dhankuta': (27.1667, 87.3333),
}
