import pandas as pd
import numpy as np
import json
import os
import random

# Load Real Kaggle Data
kaggle_file = "/home/mrrv/.cache/kagglehub/datasets/ramkrishnapudasaini/nepal-major-crop-yield-dataset-1990-2022/versions/1/Nepal_Crop_main.csv"
real_df = pd.read_csv(kaggle_file)

# Kaggle Columns: Area, Item, Year, hg/ha_yield, avg_temp, average_rain_fall_mm_per_year, pesticides_tonnes
# Convert hg/ha to kg/ha (divide by 10)
real_df['Yield_Kg_Ha'] = real_df['hg/ha_yield'] / 10.0
real_df.rename(columns={
    'Item': 'Crop',
    'avg_temp': 'Avg_Temperature_C',
    'average_rain_fall_mm_per_year': 'Avg_Rainfall_mm',
    'pesticides_tonnes': 'Pesticide_Tonnes'
}, inplace=True)

# Define District Constraints to project the country data onto specific Districts realistically
district_profiles = {
    # Tarai (Hot, High Rain)
    "Jhapa": {"region": "Tarai", "temp_mod": 1.1, "rain_mod": 1.2, "province": "Koshi", "area_base": 12000},
    "Morang": {"region": "Tarai", "temp_mod": 1.1, "rain_mod": 1.1, "province": "Koshi", "area_base": 11000},
    "Sunsari": {"region": "Tarai", "temp_mod": 1.15, "rain_mod": 1.1, "province": "Koshi", "area_base": 10000},
    "Parsa": {"region": "Tarai", "temp_mod": 1.2, "rain_mod": 1.0, "province": "Madhesh", "area_base": 9000},
    "Chitwan": {"region": "Tarai", "temp_mod": 1.15, "rain_mod": 1.1, "province": "Bagmati", "area_base": 11000},
    "Rupandehi": {"region": "Tarai", "temp_mod": 1.2, "rain_mod": 1.0, "province": "Lumbini", "area_base": 9500},
    "Dang": {"region": "Tarai", "temp_mod": 1.1, "rain_mod": 0.9, "province": "Lumbini", "area_base": 8000},
    "Banke": {"region": "Tarai", "temp_mod": 1.25, "rain_mod": 0.8, "province": "Lumbini", "area_base": 7000},
    "Bardia": {"region": "Tarai", "temp_mod": 1.2, "rain_mod": 0.85, "province": "Lumbini", "area_base": 7500},
    "Kailali": {"region": "Tarai", "temp_mod": 1.2, "rain_mod": 0.9, "province": "Sudurpashchim", "area_base": 8500},
    "Kanchanpur": {"region": "Tarai", "temp_mod": 1.15, "rain_mod": 1.0, "province": "Sudurpashchim", "area_base": 9000},
    # Hilly (Moderate Temp)
    "Kathmandu": {"region": "Hilly", "temp_mod": 0.8, "rain_mod": 0.9, "province": "Bagmati", "area_base": 4000},
    "Bhaktapur": {"region": "Hilly", "temp_mod": 0.8, "rain_mod": 0.9, "province": "Bagmati", "area_base": 3000},
    "Lalitpur": {"region": "Hilly", "temp_mod": 0.8, "rain_mod": 0.9, "province": "Bagmati", "area_base": 3500},
    "Kavrepalanchok": {"region": "Hilly", "temp_mod": 0.85, "rain_mod": 0.85, "province": "Bagmati", "area_base": 4500},
    "Nuwakot": {"region": "Hilly", "temp_mod": 0.9, "rain_mod": 0.95, "province": "Bagmati", "area_base": 5000},
    "Makwanpur": {"region": "Hilly", "temp_mod": 0.95, "rain_mod": 1.0, "province": "Bagmati", "area_base": 5500},
    "Dhading": {"region": "Hilly", "temp_mod": 0.9, "rain_mod": 0.95, "province": "Bagmati", "area_base": 5000},
    "Sindhuli": {"region": "Hilly", "temp_mod": 0.95, "rain_mod": 1.05, "province": "Bagmati", "area_base": 6000},
    "Kaski": {"region": "Hilly", "temp_mod": 0.85, "rain_mod": 1.5, "province": "Gandaki", "area_base": 4500},
    "Syangja": {"region": "Hilly", "temp_mod": 0.9, "rain_mod": 1.2, "province": "Gandaki", "area_base": 5000},
    "Gorkha": {"region": "Hilly", "temp_mod": 0.8, "rain_mod": 1.1, "province": "Gandaki", "area_base": 4000},
    "Tanahu": {"region": "Hilly", "temp_mod": 0.9, "rain_mod": 1.15, "province": "Gandaki", "area_base": 4800},
    "Surkhet": {"region": "Hilly", "temp_mod": 1.0, "rain_mod": 0.85, "province": "Karnali", "area_base": 4000},
    "Ilam": {"region": "Hilly", "temp_mod": 0.75, "rain_mod": 1.3, "province": "Koshi", "area_base": 3500}
}

# Real Crops from Kaggle: Maize, Millet, Potatoes, Rice, Soya beans, Wheat
crop_season_map = {
    "Maize": ["Spring", "Summer"],
    "Millet": ["Monsoon"],
    "Potatoes": ["Winter", "Spring"],
    "Rice": ["Monsoon"],
    "Soya beans": ["Summer"],
    "Wheat": ["Winter"]
}

region_crop_bias = {
    "Tarai": {"Rice": 1.5, "Wheat": 1.3, "Maize": 1.0, "Millet": 0.5, "Potatoes": 0.8, "Soya beans": 0.8},
    "Hilly": {"Rice": 0.7, "Wheat": 1.0, "Maize": 1.3, "Millet": 1.5, "Potatoes": 1.4, "Soya beans": 1.2}
}

# Convert real country data to district-level distribution
production_data = []
np.random.seed(42)

for index, row in real_df.iterrows():
    real_crop = row['Crop']
    real_year = row['Year']
    real_temp = row['Avg_Temperature_C']
    real_rain = row['Avg_Rainfall_mm']
    real_yield = row['Yield_Kg_Ha']
    
    # Project this row into all districts based on geographic math
    for dist, p_data in district_profiles.items():
        region = p_data["region"]
        bias = region_crop_bias[region][real_crop]
        
        # Add slight random noise to baseline
        dist_temp = real_temp * p_data["temp_mod"] + np.random.normal(0, 0.5)
        dist_rain = real_rain * p_data["rain_mod"] + np.random.normal(0, 50)
        
        dist_yield = real_yield * bias + np.random.normal(0, real_yield * 0.05)
        dist_yield = max(100, dist_yield) # Prevent negative yields
        
        dist_area = p_data["area_base"] * bias * np.random.uniform(0.8, 1.2)
        dist_prod = (dist_yield * dist_area) / 1000.0 # Metric tonnes
        
        season = random.choice(crop_season_map[real_crop])
        
        # Only add crop if area is meaningful (simulating some districts don't grow some crops)
        if bias < 0.6 and np.random.rand() < 0.5:
            continue
            
        production_data.append({
            "Year": real_year,
            "District": dist,
            "Province": p_data["province"],
            "Crop": real_crop,
            "Season": season,
            "Area_Hectares": round(dist_area, 2),
            "Production_MT": round(dist_prod, 2),
            "Yield_Kg_Ha": round(dist_yield, 2),
            "Avg_Rainfall_mm": round(dist_rain, 2),
            "Avg_Temperature_C": round(dist_temp, 2),
            "Pesticide_Tonnes": round((row['Pesticide_Tonnes'] / len(district_profiles)) * bias, 2)
        })

df_output = pd.DataFrame(production_data)
# Overwrite the old dataset to bridge Kaggle -> Web App natively
os.makedirs('data', exist_ok=True)
df_output.to_csv('data/crop_production.csv', index=False)

# Add GEOJSON if missing naturally (already exists mostly but ensure map runs)
geojson_data = {"type": "FeatureCollection", "features": []}
coords = {
    "Kathmandu": [85.3240, 27.7172], "Bhaktapur": [85.4298, 27.6710], "Lalitpur": [85.3206, 27.6588],
    "Kaski": [83.9856, 28.2096], "Chitwan": [84.4365, 27.5255], "Jhapa": [87.9715, 26.6384],
    "Morang": [87.4429, 26.6644], "Rupandehi": [83.4323, 27.5342], "Kailali": [80.7932, 28.7065],
    "Banke": [81.7960, 28.1182], "Sunsari": [87.1265, 26.6111], "Parsa": [84.9080, 27.1706],
    "Kavrepalanchok": [85.5532, 27.5587], "Nuwakot": [85.1633, 27.9175], "Makwanpur": [85.0326, 27.4258],
    "Dhading": [84.9079, 27.9626], "Syangja": [83.7431, 28.0016], "Gorkha": [84.6298, 28.3242],
    "Tanahu": [84.0950, 27.9820], "Dang": [82.2988, 28.1118], "Bardia": [81.2589, 28.4556],
    "Surkhet": [81.8258, 28.6139], "Kanchanpur": [80.3151, 28.8789], "Ilam": [87.9262, 26.9064],
    "Sindhuli": [85.9696, 27.2407]
}

for dist, coord in coords.items():
    if dist not in district_profiles: continue
    lon, lat = coord
    poly = [[lon - 0.1, lat - 0.1], [lon + 0.1, lat - 0.1], [lon + 0.1, lat + 0.1], [lon - 0.1, lat + 0.1], [lon - 0.1, lat - 0.1]]
    feature = {
        "type": "Feature",
        "properties": {"DISTRICT": dist.upper(), "Province": district_profiles[dist]["province"]},
        "geometry": {"type": "Polygon", "coordinates": [poly]}
    }
    geojson_data["features"].append(feature)

with open('data/nepal_districts.geojson', 'w') as f:
    json.dump(geojson_data, f)
    
print("Successfully mapped and integrated Kaggle 'nepal-major-crop-yield-dataset' onto district-level geographic projections!")
