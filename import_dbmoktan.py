import pandas as pd
import numpy as np
import json
import os

new_kaggle_file = "/home/mrrv/.cache/kagglehub/datasets/dbmoktan/crop-yield-prediction-in-nepal/versions/1/Crop Yield Prediction in Nepal.csv"
df = pd.read_csv(new_kaggle_file)

# Standardize column mappings and bring in more features
df.rename(columns={
    'Districts': 'District',
    'yield_kg/ha': 'Yield_Kg_Ha',
    'crop_type': 'Crop',
    'avg_temp_C': 'Avg_Temperature_C',
    'avg_rainfall_mm_per_year': 'Avg_Rainfall_mm',
    'avg_relative_humidity': 'Avg_Humidity_Pct',
    'avg_wind_speed_m/s': 'Avg_Wind_Speed_ms',
    'Area': 'Area_Hectares'
}, inplace=True)

# Translate crops
crop_translation = {
    'Paddy': 'Rice',
    'Maize': 'Maize',
    'Millet': 'Millet',
    'Wheat': 'Wheat',
    'Barley': 'Barley',
    'Buckwheat': 'Buckwheat',
}
df['Crop'] = df['Crop'].map(lambda x: crop_translation.get(x, x))
df['Production_MT'] = (df['Yield_Kg_Ha'] * df['Area_Hectares']) / 1000.0
df['Year'] = df['Year'] - 57

def assign_month(crop):
    if crop == 'Rice': return 'July'
    if crop == 'Wheat' or crop == 'Barley': return 'November'
    if crop == 'Maize': return 'April'
    if crop == 'Millet': return 'August'
    return 'September'
df['Planting_Month'] = df['Crop'].apply(assign_month)

provinces = {
    "Taplejung": "Koshi", "Panchthar": "Koshi", "Ilam": "Koshi", "Jhapa": "Koshi", "Morang": "Koshi", 
    "Sunsari": "Koshi", "Dhankuta": "Koshi", "Tehrathum": "Koshi", "Bhojpur": "Koshi", "Sankhuwasabha": "Koshi", 
    "Solukhumbu": "Koshi", "Okhaldhunga": "Koshi", "Khotang": "Koshi", "Udayapur": "Koshi",
    "Saptari": "Madhesh", "Siraha": "Madhesh", "Dhanusha": "Madhesh", "Mahottari": "Madhesh", 
    "Sarlahi": "Madhesh", "Rautahat": "Madhesh", "Bara": "Madhesh", "Parsa": "Madhesh",
    "Dolakha": "Bagmati", "Sindhupalchok": "Bagmati", "Rasuwa": "Bagmati", "Dhading": "Bagmati", 
    "Nuwakot": "Bagmati", "Kathmandu": "Bagmati", "Bhaktapur": "Bagmati", "Lalitpur": "Bagmati", 
    "Kavrepalanchok": "Bagmati", "Ramechhap": "Bagmati", "Sindhuli": "Bagmati", "Makwanpur": "Bagmati", "Chitwan": "Bagmati",
    "Gorkha": "Gandaki", "Manang": "Gandaki", "Mustang": "Gandaki", "Myagdi": "Gandaki", 
    "Kaski": "Gandaki", "Lamjung": "Gandaki", "Tanahu": "Gandaki", "Nawalparasi East": "Gandaki", 
    "Syangja": "Gandaki", "Parbat": "Gandaki", "Baglung": "Gandaki",
    "Rukum East": "Lumbini", "Rolpa": "Lumbini", "Pyuthan": "Lumbini", "Gulmi": "Lumbini", 
    "Arghakhanchi": "Lumbini", "Palpa": "Lumbini", "Nawalparasi West": "Lumbini", "Rupandehi": "Lumbini", 
    "Kapilbastu": "Lumbini", "Arghakhanchi": "Lumbini", "Dang": "Lumbini", "Banke": "Lumbini", "Bardia": "Lumbini",
    "Dolpa": "Karnali", "Mugu": "Karnali", "Humla": "Karnali", "Jumla": "Karnali", 
    "Kalikot": "Karnali", "Dailekh": "Karnali", "Jajarkot": "Karnali", "Rukum West": "Karnali", 
    "Salyan": "Karnali", "Surkhet": "Karnali",
    "Bajura": "Sudurpashchim", "Bajhang": "Sudurpashchim", "Darchula": "Sudurpashchim", "Baitadi": "Sudurpashchim", 
    "Dadeldhura": "Sudurpashchim", "Doti": "Sudurpashchim", "Achham": "Sudurpashchim", "Kailali": "Sudurpashchim", 
    "Kanchanpur": "Sudurpashchim"
}

df['District'] = df['District'].str.strip().str.title()
df['Province'] = df['District'].apply(lambda x: provinces.get(x, "Unknown"))
df = df.dropna(subset=['District', 'Crop', 'Yield_Kg_Ha'])

os.makedirs('data', exist_ok=True)
df.to_csv('data/crop_production.csv', index=False)

print("Successfully injected all features from dbmoktan CSV onto the real GeoJSON architecture! ")
