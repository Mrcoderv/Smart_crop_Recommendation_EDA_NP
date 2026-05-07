"""
About Page - Project information and details
"""

import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

# Load custom CSS
with open("assets/styles/custom.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>ℹ️ About This Project</h1>
        <p style='color: #ecf0f1; margin: 10px 0 0 0;'>Climate & Season Based Crop Recommendation System for Nepal</p>
    </div>
""", unsafe_allow_html=True)

# Project Overview
st.markdown("## 🎯 Project Objective")

st.markdown("""
This comprehensive Smart Agriculture application helps farmers, agricultural planners, and policymakers in Nepal 
make data-driven decisions for crop cultivation. The system integrates climate data, geographical information, 
and historical agricultural data to provide intelligent crop recommendations.

### Key Goals:
- 📍 **Location Intelligence**: Identify the best crops for specific districts and regions
- 🌡️ **Climate Analysis**: Understand how climate conditions affect crop suitability
- 🌍 **Geographical Insights**: Visualize crop distributions and patterns using GIS mapping
- 🌾 **Smart Recommendations**: Provide science-backed crop suggestions based on real-time and historical data
- 📊 **Data Exploration**: Enable exploratory analysis of agricultural datasets
- 🌐 **Real-time Integration**: Fetch live weather data for up-to-date recommendations
""")

# Features
st.markdown("## ✨ Features Overview")

features = {
    "📈 EDA Dashboard": {
        "description": "Comprehensive exploratory data analysis with interactive visualizations",
        "details": [
            "Crop production analysis across districts and seasons",
            "Yield comparisons and trend analysis",
            "Correlation studies and statistical insights",
            "Interactive charts with filters"
        ]
    },
    "🗺️ GIS Visualization": {
        "description": "Interactive geographical mapping of Nepal's agricultural landscape",
        "details": [
            "District-wise crop intensity mapping",
            "Production heatmaps",
            "Seasonal crop distribution",
            "Zoomable and interactive maps"
        ]
    },
    "🌡️ Live Weather": {
        "description": "Real-time weather data and 7-day forecasts",
        "details": [
            "Current weather conditions for all districts",
            "Temperature and humidity tracking",
            "Precipitation and wind speed monitoring",
            "Multi-district weather comparison"
        ]
    },
    "🌾 Crop Recommendation": {
        "description": "Intelligent crop recommendations based on climate and season",
        "details": [
            "Temperature and rainfall analysis",
            "Seasonal suitability assessment",
            "Altitude-based recommendations",
            "Suitability scoring system"
        ]
    },
    "📊 Dataset Viewer": {
        "description": "Browse and explore agricultural datasets",
        "details": [
            "Data preview and statistics",
            "Advanced filtering and search",
            "Export to CSV, Excel, and JSON",
            "Data quality reports"
        ]
    }
}

for feature_name, feature_data in features.items():
    with st.expander(f"### {feature_name}"):
        st.write(f"**{feature_data['description']}**")
        st.write("\nCapabilities:")
        for detail in feature_data['details']:
            st.write(f"- {detail}")

# Technology Stack
st.markdown("## 🛠️ Technology Stack")

tech_stack = {
    "Backend & Data Processing": ["Python", "Pandas", "NumPy", "SciPy"],
    "Frontend & Visualization": ["Streamlit", "Plotly", "Matplotlib", "Seaborn"],
    "GIS & Mapping": ["GeoPandas", "Folium", "GeoJSON"],
    "APIs & External Services": ["Open-Meteo API", "Requests Library"],
    "Environment": ["Python 3.8+", "Virtual Environment", "pip"]
}

col1, col2 = st.columns(2)

with col1:
    for idx, (category, technologies) in enumerate(list(tech_stack.items())[:3]):
        st.markdown(f"**{category}**")
        for tech in technologies:
            st.write(f"• {tech}")
        st.markdown("")

with col2:
    for idx, (category, technologies) in enumerate(list(tech_stack.items())[3:]):
        st.markdown(f"**{category}**")
        for tech in technologies:
            st.write(f"• {tech}")
        st.markdown("")

# Data Sources
st.markdown("## 📚 Data Sources")

st.markdown("""
### Primary Data:
- **Crop Production Dataset**: Historical agricultural production data across Nepal districts
- **District GeoJSON**: Nepal administrative boundaries in GeoJSON format
- **Climate Dataset**: Historical climate and weather patterns

### Real-time Data:
- **Open-Meteo API**: Free weather API providing real-time and forecast data
  - Current weather conditions
  - 7-day forecasts
  - Historical weather archives
""")

# Methodology
st.markdown("## 🔬 Methodology")

st.markdown("""
### Crop Suitability Scoring:
The system evaluates crop suitability based on multiple factors:

1. **Temperature Compatibility** (30 points)
   - Each crop has an optimal temperature range
   - Score decreases as conditions deviate from optimal range

2. **Rainfall Requirements** (30 points)
   - Minimum and maximum rainfall thresholds
   - Matching between available and required rainfall

3. **Seasonal Alignment** (25 points)
   - Crops have preferred seasons
   - Perfect match if season aligns

4. **Altitude Suitability** (15 points)
   - Altitude constraints for crop cultivation
   - Regional altitude variations

**Total Score**: 0-100, where higher scores indicate better suitability

### Climate Classification:
The system classifies climate into categories:
- Tropical: Hot and Wet (>25°C, >150mm rainfall)
- Subtropical: Hot and Dry
- Temperate: Moderate conditions
- Alpine: Cold conditions
""")

# Project Workflow
st.markdown("## 🔄 Project Workflow")

workflow_steps = [
    ("Data Collection", "Gathering historical agricultural data and GIS information"),
    ("Data Preprocessing", "Cleaning, normalizing, and preparing data for analysis"),
    ("Exploratory Analysis", "Understanding patterns and trends in agricultural data"),
    ("Recommendation Engine", "Developing intelligent crop recommendation algorithms"),
    ("Visualization", "Creating interactive dashboards and maps for exploration"),
    ("API Integration", "Connecting real-time weather data sources"),
    ("Testing & Validation", "Ensuring accuracy and reliability of recommendations"),
    ("Deployment", "Launching as a Streamlit web application")
]

for idx, (step, description) in enumerate(workflow_steps, 1):
    st.markdown(f"**Step {idx}: {step}**")
    st.markdown(f"_{description}_")
    if idx < len(workflow_steps):
        st.markdown("↓")

# Future Enhancements
st.markdown("## 🚀 Future Scope & Enhancements")

future_enhancements = [
    "🤖 Machine Learning Models for better prediction accuracy",
    "📱 Mobile application for farmer accessibility",
    "🌐 Multi-language support (Nepali, English, regional languages)",
    "💾 Cloud deployment on Azure or AWS",
    "📊 Advanced analytics with big data processing",
    "🔔 Push notifications for weather alerts",
    "🌾 Crop disease prediction and management",
    "💱 Market price predictions and trends",
    "👥 Community forum for farmers to share experiences",
    "🌱 Soil health assessment and recommendations"
]

col1, col2 = st.columns(2)

with col1:
    for enhancement in future_enhancements[:5]:
        st.write(enhancement)

with col2:
    for enhancement in future_enhancements[5:]:
        st.write(enhancement)

# Team & Credits
st.markdown("## 👥 Project Information")

st.markdown("""
### Project Details:
- **Title**: Climate and Season Based Crop Recommendation and GIS Visualization System for Nepal
- **Category**: BCA Project-III (Final Year Bachelor Project)
- **Institution**: Bachelor of Computer Application Program
- **Duration**: Academic Year 2025-2026
- **Status**: ✅ In Development

### Technologies Used:
- Python 3.9+
- Streamlit Framework
- Geospatial Analysis Libraries
- Data Visualization Tools
- Cloud APIs

### Development Approach:
- Modular and scalable architecture
- RESTful API principles
- Object-oriented programming
- Clean code practices
- Comprehensive documentation
""")

# Getting Started
st.markdown("## 🚀 Getting Started")

st.markdown("""
### Installation:
```bash
# Clone the repository
git clone <repository-url>

# Navigate to project directory
cd Smart_crop_Recommendation_EDA_NP

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application:
```bash
streamlit run app.py
```

### Project Structure:
```
project/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── data/                     # Data files (CSV, GeoJSON)
├── utils/                    # Utility modules
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── weather_api.py
│   ├── recommendation.py
│   ├── visualization.py
│   └── map_utils.py
├── pages/                    # Streamlit pages
│   ├── 1_Home.py
│   ├── 2_EDA_Dashboard.py
│   ├── 3_GIS_Map.py
│   ├── 4_Live_Weather.py
│   ├── 5_Crop_Recommendation.py
│   ├── 6_Dataset_Viewer.py
│   └── 7_About.py
└── assets/                   # Static files and styles
    └── styles/custom.css
```
""")

# Support & Documentation
st.markdown("## 📖 Support & Resources")

st.markdown("""
### Documentation:
- README.md: Project overview and setup guide
- Code comments: Inline documentation in all modules
- Type hints: Function signatures with type hints
- Docstrings: Comprehensive function documentation

### Resources:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python)
- [GeoPandas Documentation](https://geopandas.org)
- [Open-Meteo API](https://open-meteo.com)
- [Nepal GIS Data](https://www.arcgis.com)

### Contact & Feedback:
- Report issues or suggest features
- Questions about the system
- Feature requests and improvements
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
