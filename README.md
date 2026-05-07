# Climate and Season Based Crop Recommendation and GIS Visualization System for Nepal

**BCA Project-III**

This is a comprehensive, beginner-friendly web application tailored for the agricultural landscape of Nepal using explicit, understandable logic constraints without relying on overly complex machine-learning AI. It is built natively using Python and Streamlit, leveraging active and historical data logic to draw insights for students, farmers, and agriculture planners.

## Core Features
- **Data Analysis Dashboard**: Perform Exploratory Data Analysis (EDA) on Nepal's historical crop production trends combining area, production, and yields.
- **GIS Visualization Page**: View geographical choropleth maps displaying crop distributions actively colored via Folium and GeoPandas logic across Nepal's districts.
- **Live Weather API**: Fetches real-time temperature, humidity, and rainfall conditions locally across varied Nepalese Hubs dynamically hooking into **Open-Meteo API**.
- **Crop Recommendation System**: A straightforward constraint and rule-based system that parses specific climate factors directly filtering and computing against simple thresholds to safely output exactly which crops survive under given temperature profiles.

## Tech Stack
- **Python**: Core programming language.
- **Streamlit**: Web structural framer and front-end host.
- **Pandas & NumPy**: Data processing logic.
- **Plotly & Matplotlib**: Exploratory Data Chartings.
- **GeoPandas & Folium**: Geospatial map building via GeoJSONs.
- **Requests**: Handing external REST pulls (Open-Meteo).

## Project Structure
```text
Smartagri/
│
├── app.py                # Main project root mapping and navigation
├── data/                 # Directory holding datasets & GeoJSON formats
├── pages/                
│   ├── 1_Dashboard.py    # EDA dashboards and charts
│   ├── 2_GIS_Map.py      # Spatial data and Map visualization
│   ├── 3_Crop_Recommendation.py  # Rule-based crop suggestion module
│   └── 4_Live_Weather.py # Live Open-Meteo API fetching module
├── api/
│   └── weather.py        # Logic interface connecting to Open-Meteo
├── utils/                
│   ├── data_loader.py    # Handlers for IO/Caching
│   └── processor.py      # Mathematical computations
├── requirements.txt      # Python dependencies
└── README.md             # Project information
```

## How to Run
Ensure your virtual environment is activated.

```bash
pip install -r requirements.txt
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

## Documentation
Designed tightly as a semester-targeted BCA academic submission.
