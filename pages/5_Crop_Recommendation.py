"""
Crop Recommendation Page - Hybrid Intelligence (Rule-based + ML)
Combines traditional recommendation engine with ML predictions
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.recommendation import (
    recommend_crops, get_crop_details, get_suitability_score,
    climate_classification, get_all_crops
)
from utils.model_loader import (
    load_ml_model, check_model_availability, display_prediction_result,
    display_feature_importance, display_confidence_distribution, get_model_status
)
from utils.ml_predictor import get_crop_info, get_suitability_message

st.set_page_config(page_title="Crop Recommendation", page_icon="🌾", layout="wide")

# Load custom CSS
try:
    with open("assets/styles/custom.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Header
st.markdown("""
    <div style='background: linear-gradient(135deg, #27ae60 0%, #1e5631 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🌾 Smart Crop Recommendation System</h1>
        <p style='color: #d5f4e6; margin: 10px 0 0 0;'>Hybrid Intelligence: Traditional + Machine Learning Recommendations</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs for different recommendation methods
tab1, tab2, tab3 = st.tabs(["🤖 AI Prediction (ML)", "📊 Rule-Based Recommendation", "📈 Model Analytics"])

# ============================================================================
# TAB 1: ML-BASED PREDICTION
# ============================================================================
with tab1:
    st.markdown("### 🤖 Machine Learning Crop Prediction")
    
    # Check model availability
    model_status = get_model_status()
    
    if not model_status['available']:
        st.warning("⚠️ ML Model Not Trained")
        st.info("""
        The ML model needs to be trained first. Run the following command:
        ```bash
        python models/train_model.py
        ```
        Then refresh this page.
        """)
    else:
        # Load ML model
        ml_predictor = load_ml_model()
        
        if ml_predictor:
            st.success("✅ ML Model Loaded Successfully")
            
            # ML Input Section
            st.markdown("#### 📊 Enter Agricultural Parameters for ML Prediction")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ml_temperature = st.slider(
                    "🌡️ Temperature (°C)",
                    min_value=0.0,
                    max_value=40.0,
                    value=25.0,
                    step=0.1,
                    key="ml_temp"
                )
                
                ml_humidity = st.slider(
                    "💧 Humidity (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=65.0,
                    step=1.0,
                    key="ml_humidity"
                )
            
            with col2:
                ml_rainfall = st.slider(
                    "🌧️ Rainfall (mm)",
                    min_value=0.0,
                    max_value=400.0,
                    value=150.0,
                    step=5.0,
                    key="ml_rainfall"
                )
                
                ml_nitrogen = st.slider(
                    "🧪 Nitrogen (N)",
                    min_value=0.0,
                    max_value=100.0,
                    value=50.0,
                    step=1.0,
                    key="ml_nitrogen"
                )
            
            with col3:
                ml_phosphorus = st.slider(
                    "🧪 Phosphorus (P)",
                    min_value=0.0,
                    max_value=100.0,
                    value=30.0,
                    step=1.0,
                    key="ml_phosphorus"
                )
                
                ml_potassium = st.slider(
                    "🧪 Potassium (K)",
                    min_value=0.0,
                    max_value=100.0,
                    value=40.0,
                    step=1.0,
                    key="ml_potassium"
                )
            
            # Make prediction
            if st.button("🚀 Get ML Prediction", key="ml_predict"):
                with st.spinner("🔄 Analyzing data with ML model..."):
                    prediction = ml_predictor.predict(
                        ml_temperature,
                        ml_humidity,
                        ml_rainfall,
                        ml_nitrogen,
                        ml_phosphorus,
                        ml_potassium
                    )
                    
                    if prediction['success']:
                        # Display prediction result
                        display_prediction_result(prediction, show_details=True)
                        
                        # Store prediction in session state for later use
                        st.session_state.last_ml_prediction = prediction
                    else:
                        st.error(f"❌ Prediction Error: {prediction.get('message')}")

# ============================================================================
# TAB 2: RULE-BASED RECOMMENDATION
# ============================================================================
with tab2:
    st.markdown("### 📊 Traditional Rule-Based Recommendation")

    # Input Section
    st.markdown("#### 📊 Enter Your Agricultural Parameters")

    col1, col2 = st.columns(2)

col1, col2 = st.columns(2)

with col1:
    temperature = st.slider(
        "🌡️ Average Temperature (°C)",
        min_value=0,
        max_value=40,
        value=25,
        step=1
    )
    
    rainfall = st.slider(
        "💧 Annual Rainfall (mm)",
        min_value=0,
        max_value=400,
        value=150,
        step=10
    )

with col2:
    season = st.selectbox(
        "🌤️ Select Season",
        ["Spring", "Summer", "Monsoon", "Winter"]
    )
    
    altitude = st.slider(
        "⛰️ Altitude (meters)",
        min_value=0,
        max_value=3500,
        value=1000,
        step=100
    )

# Get recommendations
st.markdown("---")
recommendations = recommend_crops(temperature, rainfall, season, altitude)

# Climate Classification
climate = climate_classification(temperature, rainfall)
st.markdown(f"""
    <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                color: white; padding: 20px; border-radius: 12px; margin-bottom: 30px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <h3 style='margin-top: 0;'>🌍 Climate Classification</h3>
        <p style='font-size: 1.2em; margin: 0;'>{climate}</p>
    </div>
""", unsafe_allow_html=True)

# Display Recommendations
st.markdown("### 🎯 Recommended Crops")

if recommendations:
    # Display top 3 recommendations prominently
    st.markdown("#### ⭐ Top Recommendations")
    
    for i, rec in enumerate(recommendations[:3], 1):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            score_percent = min(100, int(rec['score']))
            score_color = '#27ae60' if score_percent > 70 else '#e67e22' if score_percent > 40 else '#e74c3c'
            
            st.markdown(f"""
                <div style='background: white; border-left: 5px solid {score_color}; 
                            padding: 20px; border-radius: 8px; margin: 10px 0;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h3 style='margin: 0 0 10px 0; color: #2c3e50;'>{i}. {rec['crop']} {rec['icon']}</h3>
                            <p style='margin: 5px 0; color: #7f8c8d;'>{rec['description']}</p>
                        </div>
                        <div style='text-align: right;'>
                            <div style='font-size: 1.5em; font-weight: bold; color: {score_color};'>{score_percent}%</div>
                            <div style='color: #7f8c8d; font-size: 0.9em;'>Match Score</div>
                        </div>
                    </div>
                    
                    <hr style='margin: 15px 0;'>
                    
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9em;'>
                        <div>
                            <strong>Temperature:</strong><br>{rec['temperature_range']}
                        </div>
                        <div>
                            <strong>Rainfall:</strong><br>{rec['rainfall_range']}
                        </div>
                        <div>
                            <strong>Seasons:</strong><br>{rec['seasons']}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Show all recommendations in expandable section
    with st.expander("📋 View All Recommendations", expanded=False):
        for i, rec in enumerate(recommendations, 1):
            score_percent = min(100, int(rec['score']))
            st.markdown(f"""
                **{i}. {rec['crop']} {rec['icon']}** (Score: {score_percent}%)
                
                - {rec['description']}
                - Temperature: {rec['temperature_range']}
                - Rainfall: {rec['rainfall_range']}
                - Seasons: {rec['seasons']}
                
                ---
            """)
else:
    st.warning("⚠️ No suitable crops found for the given parameters. Try adjusting the inputs.")

# Crop Details Viewer
st.markdown("---")
st.markdown("### 🔍 Crop Details Viewer")

selected_crop = st.selectbox("Select a crop to view details", get_all_crops())

if selected_crop:
    crop_info = get_crop_details(selected_crop)
    
    if crop_info:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style='background: #f0f9f7; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;'>
                    <h3 style='margin-top: 0;'>{selected_crop} {crop_info['icon']}</h3>
                    <p><strong>Description:</strong></p>
                    <p>{crop_info['description']}</p>
                    
                    <p><strong>Ideal Conditions:</strong></p>
                    <ul>
                        <li>Temperature: {crop_info['temperature_range'][0]}°C - {crop_info['temperature_range'][1]}°C</li>
                        <li>Rainfall: {crop_info['rainfall_range'][0]}mm - {crop_info['rainfall_range'][1]}mm</li>
                        <li>Altitude: {crop_info['altitude_range'][0]}m - {crop_info['altitude_range'][1]}m</li>
                        <li>pH Range: {crop_info['ph_range'][0]} - {crop_info['ph_range'][1]}</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: #f0f9f7; padding: 20px; border-radius: 8px; border-left: 4px solid #27ae60;'>
                    <h3 style='margin-top: 0;'>Best Seasons</h3>
                    <div style='display: flex; gap: 10px; flex-wrap: wrap;'>
            """, unsafe_allow_html=True)
            
            for season_name in crop_info['seasons']:
                st.markdown(f"""
                        <div style='background: #27ae60; color: white; padding: 10px 15px; 
                                    border-radius: 20px; font-weight: 600;'>
                            {season_name}
                        </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Suitability Score Tester
        st.markdown("#### Suitability Score Calculator")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            test_temp = st.number_input("Temperature (°C)", value=25, key=f"temp_{selected_crop}")
        
        with col2:
            test_rainfall = st.number_input("Rainfall (mm)", value=150, key=f"rain_{selected_crop}")
        
        with col3:
            test_season = st.selectbox("Season", ["Spring", "Summer", "Monsoon", "Winter"], key=f"season_{selected_crop}")
        
        suitability = get_suitability_score(test_temp, test_rainfall, test_season, selected_crop)
        
        score_percent = min(100, suitability)
        if score_percent >= 70:
            score_color = '#27ae60'
            score_text = "Highly Suitable ✅"
        elif score_percent >= 40:
            score_color = '#e67e22'
            score_text = "Moderately Suitable ⚠️"
        else:
            score_color = '#e74c3c'
            score_text = "Not Suitable ❌"
        
        st.markdown(f"""
            <div style='background: {score_color}20; border-left: 5px solid {score_color}; 
                        padding: 15px; border-radius: 8px; margin-top: 15px;'>
                <div style='font-size: 1.8em; font-weight: bold; color: {score_color}; margin-bottom: 10px;'>
                    {score_percent}% - {score_text}
                </div>
                <p style='margin: 0; color: #2c3e50;'>
                    {selected_crop} is <strong>{score_text.split()[0].lower()}</strong> for these conditions.
                </p>
            </div>
        """, unsafe_allow_html=True)

# Tips and Best Practices
st.markdown("---")
st.markdown("### 💡 Agricultural Tips & Best Practices")

tips = [
    "🌡️ Monitor temperature variations throughout the season",
    "💧 Ensure proper irrigation systems for consistent rainfall simulation",
    "🌤️ Check seasonal weather forecasts before planting",
    "🗺️ Consider local soil composition and pH levels",
    "🌾 Rotate crops yearly to maintain soil fertility",
    "📊 Keep records of yield and production for future planning",
    "🐛 Monitor pest and disease patterns for your selected crops",
    "🚜 Use proper spacing and planting techniques"
]

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 👨‍🌾 Farmer Tips")
    for tip in tips[:4]:
        st.markdown(f"• {tip}")

with col2:
    st.markdown("#### 🌱 Sustainability Practices")
    for tip in tips[4:]:
        st.markdown(f"• {tip}")
