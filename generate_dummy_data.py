import pandas as pd
import numpy as np
import json
import os
import random

# Create dummy directories if they don't exist
os.makedirs('data', exist_ok=True)

# 1. District Profiles (Based on Nepal's geography: Tarai, Hilly)
district_profiles = {
    # Tarai (Hot, High Rain)
    "Jhapa": {"region": "Tarai", "base_temp": 25, "base_rain": 2000, "province": "Koshi"},
    "Morang": {"region": "Tarai", "base_temp": 25, "base_rain": 1900, "province": "Koshi"},
    "Sunsari": {"region": "Tarai", "base_temp": 26, "base_rain": 1800, "province": "Koshi"},
    "Parsa": {"region": "Tarai", "base_temp": 27, "base_rain": 1500, "province": "Madhesh"},
    "Chitwan": {"region": "Tarai", "base_temp": 26, "base_rain": 1800, "province": "Bagmati"},
    "Rupandehi": {"region": "Tarai", "base_temp": 27, "base_rain": 1600, "province": "Lumbini"},
    "Dang": {"region": "Tarai", "base_temp": 25, "base_rain": 1400, "province": "Lumbini"},
    "Banke": {"region": "Tarai", "base_temp": 28, "base_rain": 1300, "province": "Lumbini"},
    "Bardia": {"region": "Tarai", "base_temp": 27, "base_rain": 1400, "province": "Lumbini"},
    "Kailali": {"region": "Tarai", "base_temp": 27, "base_rain": 1500, "province": "Sudurpashchim"},
    "Kanchanpur": {"region": "Tarai", "base_temp": 26, "base_rain": 1600, "province": "Sudurpashchim"},
    # Hilly (Moderate Temp)
    "Kathmandu": {"region": "Hilly", "base_temp": 18, "base_rain": 1400, "province": "Bagmati"},
    "Bhaktapur": {"region": "Hilly", "base_temp": 18, "base_rain": 1400, "province": "Bagmati"},
    "Lalitpur": {"region": "Hilly", "base_temp": 18, "base_rain": 1400, "province": "Bagmati"},
    "Kavrepalanchok": {"region": "Hilly", "base_temp": 19, "base_rain": 1300, "province": "Bagmati"},
    "Nuwakot": {"region": "Hilly", "base_temp": 20, "base_rain": 1500, "province": "Bagmati"},
    "Makwanpur": {"region": "Hilly", "base_temp": 21, "base_rain": 1600, "province": "Bagmati"},
    "Dhading": {"region": "Hilly", "base_temp": 20, "base_rain": 1500, "province": "Bagmati"},
    "Sindhuli": {"region": "Hilly", "base_temp": 22, "base_rain": 1700, "province": "Bagmati"},
    "Kaski": {"region": "Hilly", "base_temp": 19, "base_rain": 3000, "province": "Gandaki"},
    "Syangja": {"region": "Hilly", "base_temp": 20, "base_rain": 2000, "province": "Gandaki"},
    "Gorkha": {"region": "Hilly", "base_temp": 18, "base_rain": 1800, "province": "Gandaki"},
    "Tanahu": {"region": "Hilly", "base_temp": 21, "base_rain": 1900, "province": "Gandaki"},
    "Surkhet": {"region": "Hilly", "base_temp": 23, "base_rain": 1400, "province": "Karnali"},
    # Hilly East (Tea region)
    "Ilam": {"region": "Hilly_East", "base_temp": 17, "base_rain": 2500, "province": "Koshi"}
}

# 2. Crop Profiles (Ideal conditions and expected yields)
crop_profiles = {
    "Rice": {"ideal_temp": (22, 35), "ideal_rain": (1500, 3000), "base_yield": 3500, "regions": ["Tarai"], "seasons": ["Monsoon", "Summer"]},
    "Wheat": {"ideal_temp": (10, 22), "ideal_rain": (300, 1000), "base_yield": 2800, "regions": ["Tarai", "Hilly", "Hilly_East"], "seasons": ["Winter"]},
    "Maize": {"ideal_temp": (15, 30), "ideal_rain": (500, 1500), "base_yield": 3000, "regions": ["Hilly", "Tarai"], "seasons": ["Spring", "Summer"]},
    "Millet": {"ideal_temp": (20, 30), "ideal_rain": (400, 800), "base_yield": 1500, "regions": ["Hilly"], "seasons": ["Summer", "Monsoon"]},
    "Barley": {"ideal_temp": (10, 20), "ideal_rain": (300, 800), "base_yield": 1200, "regions": ["Hilly"], "seasons": ["Winter"]},
    "Potato": {"ideal_temp": (15, 20), "ideal_rain": (500, 1500), "base_yield": 15000, "regions": ["Hilly", "Tarai", "Hilly_East"], "seasons": ["Winter", "Spring"]},
    "Sugarcane": {"ideal_temp": (20, 35), "ideal_rain": (1500, 3000), "base_yield": 45000, "regions": ["Tarai"], "seasons": ["Pre-monsoon", "Summer"]},
    "Mustard": {"ideal_temp": (10, 25), "ideal_rain": (300, 800), "base_yield": 1100, "regions": ["Tarai", "Hilly"], "seasons": ["Winter"]},
    "Tea": {"ideal_temp": (15, 25), "ideal_rain": (1500, 3000), "base_yield": 2000, "regions": ["Hilly_East"], "seasons": ["Spring", "Summer"]}
}

season_modifiers = {
    "Spring": {"temp_mod": 1.0, "rain_mod": 0.5},
    "Summer": {"temp_mod": 1.2, "rain_mod": 0.8},
    "Monsoon": {"temp_mod": 1.1, "rain_mod": 1.6},
    "Pre-monsoon": {"temp_mod": 1.1, "rain_mod": 1.0},
    "Winter": {"temp_mod": 0.6, "rain_mod": 0.2}
}

years = [2018, 2019, 2020, 2021, 2022, 2023]
production_data = []
np.random.seed(42)

for dist, p_data in district_profiles.items():
    for year in years:
        # Each district grows multiple suitable crops each year
        for crop, c_data in crop_profiles.items():
            # Assume 80% chance they grow this crop if region matches
            if p_data["region"] not in c_data["regions"] and np.random.rand() > 0.1:
                continue # Skip mostly crops not meant for this region
                
            season = random.choice(c_data["seasons"])
            mod = season_modifiers[season]
            
            # Simulated environment this year
            actual_temp = p_data["base_temp"] * mod["temp_mod"] + np.random.normal(0, 2)
            actual_rain = p_data["base_rain"] * mod["rain_mod"] + np.random.normal(0, 200)
            
            # Limit logic
            actual_temp = max(5, actual_temp)
            actual_rain = max(100, actual_rain)
            
            # Check crop suitability
            temp_penalty = 1.0
            if actual_temp < c_data["ideal_temp"][0] or actual_temp > c_data["ideal_temp"][1]:
                temp_penalty = 0.6 # 40% drop if out of ideal temp
                
            rain_penalty = 1.0
            if actual_rain < c_data["ideal_rain"][0] or actual_rain > c_data["ideal_rain"][1]:
                rain_penalty = 0.7 # 30% drop if out of ideal rain
                
            # Random variation
            random_factor = np.random.uniform(0.8, 1.2)
            
            # Final Yield calculation
            yield_ha = c_data["base_yield"] * temp_penalty * rain_penalty * random_factor
            
            area_ha = np.random.uniform(100, 12000)
            if p_data["region"] == "Tarai" and crop in ["Rice", "Wheat"]:
                area_ha *= 2 # Tarai grows more volume
            
            production_mt = (yield_ha * area_ha) / 1000
            
            production_data.append({
                "Year": year,
                "District": dist,
                "Province": p_data["province"],
                "Crop": crop,
                "Season": season,
                "Area_Hectares": round(area_ha, 2),
                "Production_MT": round(production_mt, 2),
                "Yield_Kg_Ha": round(yield_ha, 2),
                "Avg_Rainfall_mm": round(actual_rain, 2),
                "Avg_Temperature_C": round(actual_temp, 2)
            })

df_production = pd.DataFrame(production_data)
df_production.to_csv('data/crop_production.csv', index=False)

# GEOJSON CREATION (Keep the mock points for visualization)
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

print("Generated realistic correlation crop production data successfully.")
