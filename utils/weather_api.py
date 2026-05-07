"""
Weather API Module
Fetches live weather data from Open-Meteo API.
"""

import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Open-Meteo API endpoint
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Nepal district coordinates (latitude, longitude)
NEPAL_COORDINATES = {
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
    'Dhulikhel': (27.6167, 85.4167),
    'Gorkha': (28.0333, 84.6333),
    'Syangja': (28.1333, 83.8500),
    'Tanahun': (27.9000, 84.3667),
    'Kaski': (28.2500, 83.9833),
    'Lamjung': (28.4333, 84.9167),
    'Manang': (28.6333, 84.3333),
    'Mustang': (29.2000, 83.8667),
    'Myagdi': (28.7500, 83.6667),
    'Parbat': (28.2667, 83.6667),
    'Baglung': (28.3667, 83.6000),
    'Gulmi': (27.9500, 83.5000),
    'Arghakhanchi': (27.8333, 83.4333),
}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_weather_data(latitude, longitude):
    """Fetch weather data from Open-Meteo API."""
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
            "timezone": "Asia/Kathmandu"
        }
        
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch weather data: {str(e)}")
        return None

def get_district_weather(district):
    """Get weather for a specific district."""
    if district in NEPAL_COORDINATES:
        lat, lon = NEPAL_COORDINATES[district]
        return get_weather_data(lat, lon)
    return None

def parse_current_weather(weather_data):
    """Parse current weather information."""
    if not weather_data or 'current' not in weather_data:
        return None
    
    current = weather_data['current']
    return {
        'temperature': current.get('temperature_2m', 'N/A'),
        'humidity': current.get('relative_humidity_2m', 'N/A'),
        'wind_speed': current.get('wind_speed_10m', 'N/A'),
        'precipitation': current.get('precipitation', 'N/A'),
        'time': current.get('time', '')
    }

def parse_daily_forecast(weather_data, days=7):
    """Parse daily weather forecast."""
    if not weather_data or 'daily' not in weather_data:
        return pd.DataFrame()
    
    daily = weather_data['daily']
    dates = pd.date_range(datetime.now().date(), periods=len(daily['time']), freq='D')
    
    df = pd.DataFrame({
        'Date': dates,
        'Max_Temp': daily.get('temperature_2m_max', []),
        'Min_Temp': daily.get('temperature_2m_min', []),
        'Precipitation': daily.get('precipitation_sum', []),
        'Wind_Speed': daily.get('wind_speed_10m_max', [])
    })
    
    return df.head(days)

def get_weather_description(code):
    """Convert WMO weather code to description."""
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing rime fog',
        51: 'Drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with hail',
        99: 'Thunderstorm with large hail'
    }
    return weather_codes.get(code, 'Unknown')

def get_all_districts_weather():
    """Fetch weather for all major districts."""
    weather_dict = {}
    for district in list(NEPAL_COORDINATES.keys())[:10]:  # Limit to 10 to avoid rate limiting
        weather_dict[district] = get_district_weather(district)
    return weather_dict

def is_suitable_for_crop(temperature, rainfall, crop):
    """Check if weather conditions are suitable for a crop."""
    crop_requirements = {
        'Rice': {'temp_min': 20, 'temp_max': 30, 'rainfall_min': 150},
        'Wheat': {'temp_min': 15, 'temp_max': 25, 'rainfall_min': 40},
        'Maize': {'temp_min': 18, 'temp_max': 27, 'rainfall_min': 60},
        'Potato': {'temp_min': 15, 'temp_max': 22, 'rainfall_min': 50},
        'Tomato': {'temp_min': 20, 'temp_max': 28, 'rainfall_min': 60},
        'Millet': {'temp_min': 22, 'temp_max': 30, 'rainfall_min': 40},
        'Barley': {'temp_min': 10, 'temp_max': 20, 'rainfall_min': 30}
    }
    
    if crop not in crop_requirements:
        return False
    
    requirements = crop_requirements[crop]
    
    temp_suitable = requirements['temp_min'] <= temperature <= requirements['temp_max']
    rainfall_suitable = rainfall >= requirements['rainfall_min']
    
    return temp_suitable and rainfall_suitable
