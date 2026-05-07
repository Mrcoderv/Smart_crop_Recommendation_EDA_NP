"""
Smart Crop Recommendation System for Nepal
BCA Project-III: Climate and Season Based Crop Recommendation and GIS Visualization

Main Application Entry Point
"""

import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Smart Crop Recommendation System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Smart Crop Recommendation System for Nepal\nBCA Project-III"
    }
)

# Load custom CSS
try:
    with open("assets/styles/custom.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Main Page Content
st.markdown("""
    <div style='background: linear-gradient(135deg, #27ae60 0%, #1e5631 100%); 
                padding: 40px; border-radius: 15px; margin-bottom: 30px; text-align: center;'>
        <h1 style='color: white; font-size: 2.5em; margin-bottom: 10px;'>
            🌾 Smart Crop Recommendation System
        </h1>
        <h3 style='color: #ecf0f1; margin-top: 0;'>
            Climate & Season Based Crop Recommendation for Nepal
        </h3>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("# 🌾 Smart Agriculture Platform")
st.sidebar.markdown("---")

# Display Navigation Info
st.sidebar.markdown("""
### 📱 Navigation Menu

Use the navigation menu at the top of the sidebar to access different features:

1. **Home** - Overview and quick statistics
2. **EDA Dashboard** - Explore agricultural data
3. **GIS Map** - View geographical distribution
4. **Live Weather** - Real-time weather data
5. **Crop Recommendation** - Get smart suggestions
6. **Dataset Viewer** - Browse datasets
7. **About** - Project information
""")

st.sidebar.markdown("---")

# Application Statistics
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.info("""
**System Features:**
- 📈 Interactive EDA dashboards
- 🗺️ GIS-based crop mapping
- 🌡️ Real-time weather integration
- 🤖 Intelligent recommendations
- 📋 Data exploration tools
""")

# Main Content Area
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #27ae60;
                    text-align: center;'>
            <h3 style='font-size: 1.5em;'>👋 Welcome!</h3>
            <p>This application helps you make data-driven agricultural decisions using 
            climate data, geographical information, and intelligent recommendations.</p>
            <p style='color: #7f8c8d; font-size: 0.9em;'>
                Use the navigation menu to explore features →
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='background: white; border-radius: 12px; padding: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 4px solid #3498db;
                    text-align: center;'>
            <h3 style='font-size: 1.5em;'>🚀 Quick Start</h3>
            <p>Navigate through the pages using the menu to:</p>
            <ul style='text-align: left; display: inline-block;'>
                <li>Analyze agricultural trends</li>
                <li>View crop distributions</li>
                <li>Check live weather</li>
                <li>Get recommendations</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Features Overview
st.markdown("## ✨ Key Features")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
        <div style='background: #f0f9f7; border-radius: 12px; padding: 20px; 
                    border-left: 5px solid #27ae60;'>
            <h4>📈 EDA Dashboard</h4>
            <p>Comprehensive data analysis with interactive charts showing production trends, 
            seasonal patterns, and district-wise comparisons.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
        <div style='background: #f0f9f7; border-radius: 12px; padding: 20px; 
                    border-left: 5px solid #e67e22;'>
            <h4>🗺️ GIS Visualization</h4>
            <p>Interactive maps showing crop distribution, production intensity heatmaps, 
            and seasonal crop patterns across Nepal.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
        <div style='background: #f0f9f7; border-radius: 12px; padding: 20px; 
                    border-left: 5px solid #3498db;'>
            <h4>🌡️ Live Weather</h4>
            <p>Real-time weather data and 7-day forecasts for all districts with 
            crop suitability analysis.</p>
        </div>
    """, unsafe_allow_html=True)

feature_col4, feature_col5, feature_col6 = st.columns(3)

with feature_col4:
    st.markdown("""
        <div style='background: #f0f9f7; border-radius: 12px; padding: 20px; 
                    border-left: 5px solid #9b59b6;'>
            <h4>🌾 Recommendations</h4>
            <p>Intelligent crop recommendations based on temperature, rainfall, season, 
            and altitude with detailed suitability scores.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col5:
    st.markdown("""
        <div style='background: #f0f9f7; border-radius: 12px; padding: 20px; 
                    border-left: 5px solid #e74c3c;'>
            <h4>📊 Dataset Viewer</h4>
            <p>Browse, search, filter, and export agricultural datasets with 
            advanced analysis and data quality reports.</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col6:
    st.markdown("""
        <div style='background: #f0f9f7; border-radius: 12px; padding: 20px; 
                    border-left: 5px solid #16a085;'>
            <h4>📚 Documentation</h4>
            <p>Comprehensive project information, methodology, technologies used, 
            and detailed documentation.</p>
        </div>
    """, unsafe_allow_html=True)

# Technology Stack
st.markdown("## 🛠️ Technology Stack")

tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

with tech_col1:
    st.markdown("""
        **Data Processing**
        - Python 3.9+
        - Pandas
        - NumPy
        - SciPy
    """)

with tech_col2:
    st.markdown("""
        **Visualization**
        - Streamlit
        - Plotly
        - Matplotlib
        - Seaborn
    """)

with tech_col3:
    st.markdown("""
        **GIS & Mapping**
        - GeoPandas
        - Folium
        - GeoJSON
        - Shapely
    """)

with tech_col4:
    st.markdown("""
        **APIs & Services**
        - Open-Meteo API
        - Requests
        - Python-dotenv
    """)

# Getting Started
st.markdown("## 🚀 How to Get Started")

st.markdown("""
1. **Explore Home Page** - Get an overview of the system and key statistics
2. **View EDA Dashboard** - Analyze historical agricultural data
3. **Check GIS Maps** - See crop distribution across districts
4. **Monitor Live Weather** - Get real-time weather data
5. **Get Recommendations** - Input your parameters and get crop suggestions
6. **Browse Datasets** - Explore and download agricultural data
7. **Learn More** - Read about the project in the About section
""")

# System Information
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
        **Project Type**
        
        BCA Project-III (Final Year)
        Bachelor of Computer Application
    """)

with col2:
    st.info("""
        **Data Coverage**
        
        Nepal - All Districts
        Historical + Real-time Data
    """)

with col3:
    st.success("""
        **Status**
        
        ✅ Fully Functional
        Last Updated: 2026
    """)

# Footer
st.markdown("""
    <hr>
    <div style='text-align: center; padding: 20px; color: #7f8c8d;'>
        <p>
            <strong>Smart Crop Recommendation System for Nepal</strong><br>
            BCA Project-III | Climate & Season Based Agricultural Analytics<br>
            © 2026 | Built with Python, Streamlit, and GIS Technologies<br>
            <br>
            "Empowering Agriculture Through Data and Technology"
        </p>
    </div>
""", unsafe_allow_html=True)
        st.warning("Data not available. Please ensure the dataset is generated.")
        
    # Add footer
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            color: gray;
            text-align: center;
        }
        </style>
        <div class="footer">
            <p>Developed for the Nepal Agriculture Community 🌿</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
