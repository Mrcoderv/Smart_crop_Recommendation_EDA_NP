# 🌾 Smart Crop Recommendation System for Nepal

## BCA Project-III: Climate and Season Based Crop Recommendation and GIS Visualization System

---

## 📋 Project Overview

This comprehensive Streamlit-based application helps farmers, agricultural planners, and decision-makers in Nepal make data-driven decisions for crop cultivation. The system integrates climate data, geographical information, live weather APIs, and historical agricultural data to provide intelligent crop recommendations.

### Key Features

- **📈 EDA Dashboard** - Exploratory Data Analysis with interactive visualizations
- **🗺️ GIS Visualization** - Interactive maps showing crop distribution and production intensity
- **🌡️ Live Weather** - Real-time weather data and 7-day forecasts using Open-Meteo API
- **🌾 Crop Recommendation** - Intelligent recommendations based on climate, season, and geography
- **📊 Dataset Viewer** - Browse, filter, and export agricultural datasets
- **📚 About** - Comprehensive project documentation

---

## 🎯 Project Objectives

1. **Location Intelligence**: Identify the best crops for specific districts and regions
2. **Climate Analysis**: Understand how climate conditions affect crop suitability
3. **Geographical Insights**: Visualize crop distributions using GIS mapping
4. **Smart Recommendations**: Provide science-backed crop suggestions
5. **Data Exploration**: Enable comprehensive exploratory analysis
6. **Real-time Integration**: Fetch and display live weather data

---

## 🛠️ Technology Stack

### Backend & Data Processing
- **Python 3.9+** - Programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing

### Frontend & Visualization
- **Streamlit** - Web framework
- **Plotly** - Interactive visualizations
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical visualizations

### GIS & Mapping
- **GeoPandas** - Geospatial data analysis
- **Folium** - Interactive mapping
- **GeoJSON** - Geographical data format
- **Shapely** - Geometric operations

### APIs & External Services
- **Open-Meteo API** - Real-time weather data
- **Requests** - HTTP library
- **Python-dotenv** - Environment variables

---

## 📁 Project Structure

```
Smart_crop_Recommendation_EDA_NP/
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/
│   ├── crop_production.csv         # Crop production dataset
│   ├── climate_data.csv            # Climate dataset
│   └── nepal_districts.geojson     # GIS boundaries
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── data_loader.py              # Data loading functions
│   ├── preprocessing.py            # Data cleaning and processing
│   ├── weather_api.py              # Weather API integration
│   ├── recommendation.py           # Recommendation engine
│   ├── visualization.py            # Plotting functions
│   └── map_utils.py                # GIS mapping utilities
│
├── pages/                          # Streamlit multi-page app
│   ├── 1_Home.py                   # Landing page
│   ├── 2_EDA_Dashboard.py          # Data exploration
│   ├── 3_GIS_Map.py                # Geographical visualization
│   ├── 4_Live_Weather.py           # Real-time weather
│   ├── 5_Crop_Recommendation.py    # Recommendations
│   ├── 6_Dataset_Viewer.py         # Data browser
│   └── 7_About.py                  # Project info
│
├── assets/
│   └── styles/
│       └── custom.css              # Custom styling
│
├── notebooks/
│   └── eda_analysis.ipynb          # Jupyter notebook for EDA
│
└── screenshots/                    # Project screenshots
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/Mrcoderv/Smart_crop_Recommendation_EDA_NP.git
cd Smart_crop_Recommendation_EDA_NP
```

2. **Create Virtual Environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

---

## 📖 Application Guide

### 1. Home Page
- Overview of the system
- Key statistics
- Feature highlights
- Quick navigation

### 2. EDA Dashboard
- Crop production analysis
- District-wise statistics
- Seasonal trends
- Yield comparisons
- Correlation analysis

### 3. GIS Map
- Crop distribution visualization
- District intensity mapping
- Production heatmaps
- Interactive features

### 4. Live Weather
- Current weather conditions
- 7-day forecast
- Crop suitability analysis
- Multi-district comparison

### 5. Crop Recommendation
- Input climate parameters
- Get intelligent recommendations
- View suitability scores
- Learn crop requirements

### 6. Dataset Viewer
- Browse full datasets
- Advanced filtering
- Export options
- Data quality reports

### 7. About
- Project documentation
- Technology details
- Methodology explanation
- Future enhancements

---

## 🤖 Crop Recommendation Algorithm

### Scoring System (0-100 points)

1. **Temperature Compatibility** (30 points)
2. **Rainfall Suitability** (30 points)
3. **Season Alignment** (25 points)
4. **Altitude Compatibility** (15 points)

### Supported Crops
Rice, Wheat, Maize, Potato, Tomato, Onion, Cabbage, Millet, Barley, Lentil

---

## 🌦️ Weather API Integration

### Open-Meteo API
- Free to use, no API key required
- Real-time and forecast data
- Generous rate limiting

---

## 🔧 Customization

### Adding New Crops
Edit `utils/recommendation.py` and add to `CROP_DATABASE`

### Adding New Districts
Update coordinates in `utils/weather_api.py` and `utils/map_utils.py`

### Modifying Styling
Edit `assets/styles/custom.css`

---

## 🐛 Troubleshooting

**Data file not found**: Run `python generate_dummy_data.py`

**API timeout**: Check internet connection

**Pages not appearing**: Ensure correct file naming in `pages/` directory

---

## 📝 License

This is an academic project for BCA Project-III.

---

## 🎓 Academic Information

- **Project Title**: Climate and Season Based Crop Recommendation and GIS Visualization System for Nepal
- **Program**: Bachelor of Computer Application (BCA)
- **Semester**: VI (Final Year)
- **Project Category**: Project-III
- **Year**: 2025-2026
- **Status**: ✅ Complete and Functional

---

## 🎉 Built With

- Streamlit - Web framework
- Python - Programming language
- Plotly - Visualizations
- GeoPandas - GIS analysis
- Folium - Interactive mapping
- Open-Meteo API - Weather data

---

**"Empowering Agriculture Through Data and Technology"** 🌾

**Last Updated**: May 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
