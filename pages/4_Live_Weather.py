import streamlit as st
from api.weather import get_live_weather
import pandas as pd

st.set_page_config(page_title="Live Weather", page_icon="⛅", layout="wide")

st.title("⛅ Live Agricultural Weather Module")
st.markdown("Check real-time climate statistics directly from the Open-Meteo API to make on-the-spot agricultural decisions.")

# Example major agriculture hubs in Nepal
locations = {
    "Kathmandu": {"lat": 27.7172, "lon": 85.3240},
    "Pokhara": {"lat": 28.2096, "lon": 83.9856},
    "Chitwan": {"lat": 27.5255, "lon": 84.4365},
    "Mustang": {"lat": 28.9985, "lon": 83.8473},
    "Jhapa": {"lat": 26.6384, "lon": 87.9715},
    "Surkhet": {"lat": 28.6139, "lon": 81.8258}
}

selected_hub = st.selectbox("Select Regional Hub to fetch Live Weather", list(locations.keys()))
lat = locations[selected_hub]["lat"]
lon = locations[selected_hub]["lon"]

if st.button("Fetch Live Weather Data", type="primary"):
    with st.spinner(f"Contacting Open-Meteo API for {selected_hub}..."):
        data = get_live_weather(lat, lon)
        
        if data:
            current = data.get("current", {})
            st.success(f"Weather data retrieved for {selected_hub}!")
            
            # Live Metrics
            st.subheader("Current Climate Conditions")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Temperature (°C)", f"{current.get('temperature_2m', 'N/A')} °C")
            with col2:
                st.metric("Relative Humidity", f"{current.get('relative_humidity_2m', 'N/A')} %")
            with col3:
                st.metric("Precipitation", f"{current.get('precipitation', '0')} mm")
            with col4:
                st.metric("Wind Speed", f"{current.get('wind_speed_10m', 'N/A')} km/h")
                
            st.markdown("---")
            
            # Actionable insight
            temp = current.get('temperature_2m', 20)
            rain = current.get('precipitation', 0)
            
            st.markdown("### Agricultural Insights based on Live Data")
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
