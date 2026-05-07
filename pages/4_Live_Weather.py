"""
Live Weather Page - Real-time weather data and forecasts
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.weather_api import (
    get_district_weather, parse_current_weather, parse_daily_forecast,
    NEPAL_COORDINATES, is_suitable_for_crop
)
from utils.visualization import create_line_chart, create_bar_chart
from utils.recommendation import get_all_crops

st.set_page_config(page_title="Live Weather", page_icon="🌡️", layout="wide")

# Load custom CSS
with open("assets/styles/custom.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🌡️ Live Weather & Climate Data</h1>
        <p style='color: #d5f4e6; margin: 10px 0 0 0;'>Real-time Weather Information for Nepal Districts</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar - District Selection
st.sidebar.markdown("### 🎯 Select District")
selected_district = st.sidebar.selectbox(
    "Choose a district",
    sorted(NEPAL_COORDINATES.keys())
)

# Fetch weather data
weather_data = get_district_weather(selected_district)

if weather_data is None:
    st.error("❌ Unable to fetch weather data. Please try again later.")
    st.stop()

# Parse weather data
current_weather = parse_current_weather(weather_data)
forecast = parse_daily_forecast(weather_data, days=7)

# Display Current Weather
st.markdown(f"### 🌍 Current Weather in {selected_district}")

if current_weather:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <div style='font-size: 0.9em; opacity: 0.9;'>Temperature</div>
                <div style='font-size: 2.5em; font-weight: bold; margin: 10px 0;'>{current_weather['temperature']}°C</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <div style='font-size: 0.9em; opacity: 0.9;'>Humidity</div>
                <div style='font-size: 2.5em; font-weight: bold; margin: 10px 0;'>{current_weather['humidity']}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #27ae60 0%, #1e5631 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <div style='font-size: 0.9em; opacity: 0.9;'>Wind Speed</div>
                <div style='font-size: 2.5em; font-weight: bold; margin: 10px 0;'>{current_weather['wind_speed']} km/h</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <div style='font-size: 0.9em; opacity: 0.9;'>Precipitation</div>
                <div style='font-size: 2.5em; font-weight: bold; margin: 10px 0;'>{current_weather['precipitation']} mm</div>
            </div>
        """, unsafe_allow_html=True)

# Weather Forecast
if not forecast.empty:
    st.markdown("### 📅 7-Day Weather Forecast")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_line_chart(
            forecast, 'Date', 'Max_Temp',
            'Maximum Temperature Forecast'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_line_chart(
            forecast, 'Date', 'Min_Temp',
            'Minimum Temperature Forecast'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_bar_chart(
            forecast, 'Date', 'Precipitation',
            'Precipitation Forecast'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_line_chart(
            forecast, 'Date', 'Wind_Speed',
            'Wind Speed Forecast'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Forecast table
    st.markdown("### 📋 Detailed Forecast")
    st.dataframe(forecast, use_container_width=True)

# Crop Suitability Analysis
st.markdown("### 🌾 Crop Suitability for Current Weather")

if current_weather:
    temp = current_weather['temperature']
    humidity = current_weather['humidity']
    
    # Estimate rainfall (basic estimation from humidity)
    estimated_rainfall = humidity * 0.5
    
    st.markdown(f"""
        <div style='background: #f0f9f7; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60;'>
            <p><strong>Current Conditions:</strong></p>
            <ul>
                <li>Temperature: {temp}°C</li>
                <li>Humidity: {humidity}%</li>
                <li>Estimated Rainfall: {estimated_rainfall:.1f}mm</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Check crop suitability
    suitable_crops = []
    unsuitable_crops = []
    
    for crop in get_all_crops():
        if is_suitable_for_crop(temp, estimated_rainfall, crop):
            suitable_crops.append(crop)
        else:
            unsuitable_crops.append(crop)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Suitable Crops")
        if suitable_crops:
            for crop in suitable_crops:
                st.markdown(f"• {crop}")
        else:
            st.info("No crops are currently suitable")
    
    with col2:
        st.markdown("### ❌ Unsuitable Crops")
        if unsuitable_crops:
            for crop in unsuitable_crops[:5]:
                st.markdown(f"• {crop}")
            if len(unsuitable_crops) > 5:
                st.markdown(f"... and {len(unsuitable_crops) - 5} more")
        else:
            st.info("All crops are suitable")

# Multi-District Comparison
st.markdown("### 🌍 Multi-District Weather Comparison")

comparison_districts = st.multiselect(
    "Select districts to compare",
    sorted(NEPAL_COORDINATES.keys()),
    default=[selected_district]
)

if comparison_districts:
    comparison_data = []
    
    for district in comparison_districts:
        weather = get_district_weather(district)
        if weather:
            current = parse_current_weather(weather)
            if current:
                comparison_data.append({
                    'District': district,
                    'Temperature': current['temperature'],
                    'Humidity': current['humidity'],
                    'Wind Speed': current['wind_speed'],
                    'Precipitation': current['precipitation']
                })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_bar_chart(
                comparison_df, 'District', 'Temperature',
                'Temperature Comparison'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_bar_chart(
                comparison_df, 'District', 'Humidity',
                'Humidity Comparison'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📊 Detailed Comparison")
        st.dataframe(comparison_df, use_container_width=True)

# About this page
st.markdown("""
    <hr>
    <div style='background: #f0f9f7; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db;'>
        <h4>ℹ️ About This Page</h4>
        <p>This page displays real-time weather data fetched from the <strong>Open-Meteo API</strong>, a free weather API service.
        The data includes current conditions and 7-day forecasts for all major districts in Nepal.</p>
        <p><strong>Note:</strong> Data is cached for 1 hour to minimize API calls. Some values may be slightly delayed.</p>
    </div>
""", unsafe_allow_html=True)
            if temp > 30:
                st.warning("⚠️ High temperatures detected. Ensure crops have sufficient irrigation.")
            elif temp < 10:
                st.info("❄️ Cold conditions detected. Watch out for frost damage on sensitive crops.")
            else:
                st.success("✅ Favorable moderate temperatures for general growth.")
                
            if rain > 10:
                st.info("🌧️ Heavy precipitation occurring. Refrain from applying fertilizers or pesticides directly today.")
            elif rain > 0:
                st.info("🌦️ Light rain. Good natural irrigation.")
            else:
                st.warning("☀️ No precipitation. Monitor soil moisture levels.")
                
            st.markdown("---")
            st.subheader("7-Day Forecast")
            daily = data.get("daily", {})
            if daily:
                df_forecast = pd.DataFrame({
                    "Date": daily.get("time", []),
                    "Max Temp (°C)": daily.get("temperature_2m_max", []),
                    "Min Temp (°C)": daily.get("temperature_2m_min", []),
                    "Precipitation (mm)": daily.get("precipitation_sum", [])
                })
                st.dataframe(df_forecast, use_container_width=True)
                st.line_chart(df_forecast.set_index("Date")[["Max Temp (°C)", "Min Temp (°C)"]])
                
        else:
            st.error("Failed to fetch weather data. Please ensure you have internet connectivity.")
