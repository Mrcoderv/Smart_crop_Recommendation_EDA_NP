"""
Home Page - Landing page for the Smart Agriculture Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_crop_data, load_nepal_districts

def load_custom_css():
    """Load custom CSS for the application."""
    with open("assets/styles/custom.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Smart Crop Recommendation System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
load_custom_css()

# Hero Section
st.markdown("""
    <div style='background: linear-gradient(135deg, #27ae60 0%, #1e5631 100%); 
                padding: 40px; border-radius: 15px; margin-bottom: 30px; text-align: center;'>
        <h1 style='color: white; font-size: 2.5em; margin-bottom: 10px;'>
            🌾 Smart Crop Recommendation System
        </h1>
        <h3 style='color: #ecf0f1; margin-top: 0;'>
            Climate & Season Based Crop Recommendation for Nepal
        </h3>
        <p style='color: #d5f4e6; font-size: 1.1em;'>
            Empowering farmers with data-driven crop recommendations using GIS and weather analytics
        </p>
    </div>
""", unsafe_allow_html=True)

# Load data
crop_data = load_crop_data()
nepal_gdf = load_nepal_districts()

# Key Statistics
st.markdown("<h2 style='color: #27ae60; text-align: center;'>📊 Quick Statistics</h2>", unsafe_allow_html=True)

if not crop_data.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <h3 style='margin: 0; font-size: 2em;'>{len(crop_data)}</h3>
                <p style='margin: 0; opacity: 0.9;'>Total Records</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_crops = crop_data['Crop'].nunique() if 'Crop' in crop_data.columns else 0
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <h3 style='margin: 0; font-size: 2em;'>{unique_crops}</h3>
                <p style='margin: 0; opacity: 0.9;'>Crops Analyzed</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unique_districts = crop_data['District'].nunique() if 'District' in crop_data.columns else 0
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <h3 style='margin: 0; font-size: 2em;'>{unique_districts}</h3>
                <p style='margin: 0; opacity: 0.9;'>Districts Covered</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_production = crop_data['Production'].sum() if 'Production' in crop_data.columns else 0
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                        color: white; padding: 20px; border-radius: 12px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                <h3 style='margin: 0; font-size: 2em;'>{total_production/1e6:.1f}M</h3>
                <p style='margin: 0; opacity: 0.9;'>Total Production</p>
            </div>
        """, unsafe_allow_html=True)

# Features Section
st.markdown("<h2 style='color: #27ae60; text-align: center; margin-top: 40px;'>✨ Key Features</h2>", unsafe_allow_html=True)

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #27ae60;
                    text-align: center; transition: all 0.3s ease;'>
            <h3 style='font-size: 1.5em;'>📈 EDA Dashboard</h3>
            <p>Explore comprehensive data analysis with interactive charts and insights into crop production trends across Nepal.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #e67e22;
                    text-align: center; transition: all 0.3s ease;'>
            <h3 style='font-size: 1.5em;'>🗺️ GIS Visualization</h3>
            <p>View interactive maps showing crop distribution, district-wise production, and seasonal crop patterns across Nepal.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #3498db;
                    text-align: center; transition: all 0.3s ease;'>
            <h3 style='font-size: 1.5em;'>🌡️ Live Weather</h3>
            <p>Get real-time weather data and forecasts for different districts using Open-Meteo API integration.</p>
        </div>
    """, unsafe_allow_html=True)

feature_col4, feature_col5, feature_col6 = st.columns(3)

with feature_col4:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #27ae60;
                    text-align: center; transition: all 0.3s ease;'>
            <h3 style='font-size: 1.5em;'>🌾 Crop Recommendation</h3>
            <p>Intelligent recommendations based on climate, season, rainfall, and temperature conditions.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col5:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #e67e22;
                    text-align: center; transition: all 0.3s ease;'>
            <h3 style='font-size: 1.5em;'>📊 Dataset Viewer</h3>
            <p>Browse, search, filter and download crop production datasets with comprehensive statistics.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col6:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #3498db;
                    text-align: center; transition: all 0.3s ease;'>
            <h3 style='font-size: 1.5em;'>ℹ️ About Project</h3>
            <p>Learn about the project objectives, technologies, workflow, and future scope.</p>
        </div>
    """, unsafe_allow_html=True)

# About Section
st.markdown("<h2 style='color: #27ae60; text-align: center; margin-top: 40px;'>🎯 Project Objective</h2>", unsafe_allow_html=True)

st.markdown("""
    <div style='background: #f0f9f7; border-left: 5px solid #27ae60; padding: 20px; border-radius: 8px;'>
        <p style='font-size: 1.05em; line-height: 1.8;'>
            This comprehensive application helps farmers and agricultural decision-makers in Nepal by:
        </p>
        <ul style='font-size: 1.05em; line-height: 2;'>
            <li>📍 Identifying the best crops to grow in specific districts and seasons</li>
            <li>🌍 Understanding optimal growing conditions through GIS mapping</li>
            <li>🌡️ Analyzing climate patterns and their impact on crop productivity</li>
            <li>💡 Providing data-driven recommendations based on real-time weather and historical data</li>
            <li>📊 Enabling informed agricultural planning and resource allocation</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Technology Stack
st.markdown("<h2 style='color: #27ae60; text-align: center; margin-top: 40px;'>🛠️ Technology Stack</h2>", unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown("""
        <div style='background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h4>Data Processing</h4>
            <ul style='margin: 0; padding-left: 20px;'>
                <li>Python</li>
                <li>Pandas</li>
                <li>NumPy</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
        <div style='background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h4>Visualization</h4>
            <ul style='margin: 0; padding-left: 20px;'>
                <li>Streamlit</li>
                <li>Plotly</li>
                <li>Matplotlib</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with tech_col3:
    st.markdown("""
        <div style='background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h4>GIS & Mapping</h4>
            <ul style='margin: 0; padding-left: 20px;'>
                <li>GeoPandas</li>
                <li>Folium</li>
                <li>GeoJSON</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with tech_col4:
    st.markdown("""
        <div style='background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h4>APIs & Tools</h4>
            <ul style='margin: 0; padding-left: 20px;'>
                <li>Open-Meteo API</li>
                <li>Requests</li>
                <li>Python-dotenv</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Call to Action
st.markdown("<h2 style='text-align: center; color: #27ae60; margin-top: 50px;'>🚀 Get Started</h2>", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    if st.button("📊 View EDA Dashboard", use_container_width=True):
        st.switch_page("pages/2_EDA_Dashboard.py")

with nav_col2:
    if st.button("🗺️ Explore GIS Maps", use_container_width=True):
        st.switch_page("pages/3_GIS_Map.py")

with nav_col3:
    if st.button("🌾 Get Recommendations", use_container_width=True):
        st.switch_page("pages/5_Crop_Recommendation.py")

# Footer
st.markdown("""
    <hr style='margin-top: 50px;'>
    <div style='text-align: center; padding: 20px; color: #7f8c8d;'>
        <p>
            <strong>Smart Crop Recommendation System for Nepal</strong><br>
            BCA Project-III | Climate & Season Based Agricultural Analytics<br>
            © 2026 | Built with Python, Streamlit, and GIS Technologies
        </p>
    </div>
""", unsafe_allow_html=True)
