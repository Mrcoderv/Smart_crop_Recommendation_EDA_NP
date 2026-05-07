import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from utils.data_loader import load_crop_data, get_unique_districts, get_unique_months
from api.weather import get_live_weather

st.set_page_config(page_title="Crop Recommendation ML Model", page_icon="🌱", layout="wide")

st.title("🤖 Intelligent Crop Recommendation System")
st.markdown("Combines **Live Weather API Data** and **Historical Machine Learning** to dynamically predict the ideal crop for your region.")

df = load_crop_data()

if df.empty:
    st.warning("Data not available. Please run data generator.")
    st.stop()

# Prepare Data & Train Model (Cached for performance)
@st.cache_resource
def train_model(dataset):
    # Features: District, Planting_Month, Avg_Rainfall_mm, Avg_Temperature_C, Avg_Humidity_Pct
    le_district = LabelEncoder()
    le_month = LabelEncoder()
    le_crop = LabelEncoder()
    
    encoded_df = dataset.copy()
    
    # Fill potential NaNs in extended features safely
    if 'Avg_Humidity_Pct' not in encoded_df.columns:
        encoded_df['Avg_Humidity_Pct'] = 60.0
        
    encoded_df['Avg_Humidity_Pct'] = encoded_df['Avg_Humidity_Pct'].fillna(encoded_df['Avg_Humidity_Pct'].mean())
    
    encoded_df['District_Enc'] = le_district.fit_transform(encoded_df['District'])
    encoded_df['Month_Enc'] = le_month.fit_transform(encoded_df['Planting_Month'])
    encoded_df['Crop_Enc'] = le_crop.fit_transform(encoded_df['Crop'])
    
    # We define "good" as Yield being at least the median for that specific crop class
    crop_medians = encoded_df.groupby('Crop_Enc')['Yield_Kg_Ha'].transform('median')
    success_df = encoded_df[encoded_df['Yield_Kg_Ha'] >= crop_medians]
    
    if success_df.empty:
        success_df = encoded_df # Fallback
        
    X = success_df[['District_Enc', 'Month_Enc', 'Avg_Rainfall_mm', 'Avg_Temperature_C', 'Avg_Humidity_Pct']]
    y = success_df['Crop_Enc']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, le_district, le_month, le_crop

with st.spinner("Training Random Forest ML Model on District Historical Data..."):
    model, le_district, le_month, le_crop = train_model(df)

# District Lat/Lon matching for API auto-fill
locations = {
    "Kathmandu": {"lat": 27.7172, "lon": 85.3240},
    "Pokhara": {"lat": 28.2096, "lon": 83.9856},
    "Chitwan": {"lat": 27.5255, "lon": 84.4365},
    "Mustang": {"lat": 28.9985, "lon": 83.8473},
    "Jhapa": {"lat": 26.6384, "lon": 87.9715},
    "Surkhet": {"lat": 28.6139, "lon": 81.8258}
}

# State management for auto-fill logic
if 'input_temp' not in st.session_state: st.session_state.input_temp = 25.0
if 'input_rain' not in st.session_state: st.session_state.input_rain = 1500.0
if 'input_humidity' not in st.session_state: st.session_state.input_humidity = 60.0

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Geographic Selection")
    district = st.selectbox("Select District", get_unique_districts(df))
    month = st.selectbox("Select Planting Month", get_unique_months(df))
    
    if district in locations:
        if st.button("🌦️ Auto-Fill with Live Open-Meteo Weather"):
            lat = locations[district]["lat"]
            lon = locations[district]["lon"]
            data = get_live_weather(lat, lon)
            if data:
                current = data.get("current", {})
                st.session_state.input_temp = float(current.get('temperature_2m', 25.0))
                # Open-Meteo gives daily precipitation, we try to estimate yearly run rate or just use weekly scaling
                st.session_state.input_rain = float(current.get('precipitation', 1.0)) * 100 # Rough estimate mapping
                st.session_state.input_humidity = float(current.get('relative_humidity_2m', 60.0))
                st.success(f"Loaded Live Weather: {st.session_state.input_temp}°C, {st.session_state.input_humidity}% Hum")
            else:
                st.error("Could not reach weather API.")

with col2:
    st.markdown("#### Climate Constraints")
    temperature = st.slider("Temperature (°C)", min_value=-5.0, max_value=45.0, value=st.session_state.input_temp)
    rainfall = st.slider("Rainfall Expectancy (mm/yr)", min_value=0.0, max_value=5000.0, value=st.session_state.input_rain)
    humidity = st.slider("Relative Humidity (%)", min_value=0.0, max_value=100.0, value=st.session_state.input_humidity)

st.markdown("---")

if st.button("Predict Best Crop (ML)", type="primary"):
    with st.spinner("Analyzing cross-district humidity, temperature, and historical yield constraints..."):
        try:
            # Safely handle unseen inputs using the classes available
            if district in le_district.classes_:
                dist_idx = le_district.transform([district])[0]
            else:
                dist_idx = 0  # Mode fallback
                
            if month in le_month.classes_:
                month_idx = le_month.transform([month])[0]
            else:
                month_idx = 0
            
            # Predict
            features = np.array([[dist_idx, month_idx, rainfall, temperature, humidity]])
            prediction = model.predict(features)
            probabilities = model.predict_proba(features)[0]
            
            top_crop = le_crop.inverse_transform(prediction)[0]
            
            # Get top predictions
            top_3_indices = np.argsort(probabilities)[::-1][:3]
            top_3_crops = le_crop.inverse_transform(top_3_indices)
            top_3_probs = probabilities[top_3_indices]

            st.success(f"## 🏆 Primary Machine Learning Recommendation: {top_crop}")
            st.info(f"The model analyzed over thousands of past yields and correlates **{top_crop}** with the highest chance of success under {temperature}°C and {humidity}% humidity. (Confidence: {top_3_probs[0]*100:.1f}%)")
            
            st.markdown("### 📊 Top Alternatives")
            for crop, prob in zip(top_3_crops, top_3_probs):
                if prob > 0:
                    st.write(f"- **{crop}**: Likelihood proxy {prob*100:.1f}%")
                    
            st.markdown("---")
            # Insight hook
            hist = df[(df['Crop'] == top_crop) & (df['District'] == district)]
            if not hist.empty:
                st.metric(f"Proven Historical Base Yield for {top_crop} in {district}", f"{hist['Yield_Kg_Ha'].mean():,.2f} Kg/Ha")
            else:
                st.write(f"This is a mathematically inferred recommendation finding patterns extending outside of traditional {district} historical reliance.")
                
        except ValueError as e:
            st.error(f"Error processing model execution. Error details: {str(e)}")
