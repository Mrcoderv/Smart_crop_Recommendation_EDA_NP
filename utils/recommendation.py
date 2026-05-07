"""
Crop Recommendation Module
Provides intelligent crop recommendations based on climate and season.
"""

import pandas as pd
import numpy as np

# Crop suitability database
CROP_DATABASE = {
    'Rice': {
        'temp_range': (20, 30),
        'rainfall_range': (150, 250),
        'seasons': ['Monsoon', 'Summer'],
        'altitude_range': (0, 2000),
        'ph_range': (5.5, 8.0),
        'description': 'Rice thrives in warm, wet conditions with abundant water',
        'icon': '🌾'
    },
    'Wheat': {
        'temp_range': (10, 25),
        'rainfall_range': (40, 100),
        'seasons': ['Winter', 'Spring'],
        'altitude_range': (0, 3000),
        'ph_range': (6.0, 8.5),
        'description': 'Wheat prefers cool weather and moderate moisture',
        'icon': '🌾'
    },
    'Maize': {
        'temp_range': (15, 27),
        'rainfall_range': (60, 120),
        'seasons': ['Summer', 'Monsoon'],
        'altitude_range': (0, 2500),
        'ph_range': (5.5, 7.5),
        'description': 'Maize needs warm weather with moderate rainfall',
        'icon': '🌽'
    },
    'Potato': {
        'temp_range': (10, 22),
        'rainfall_range': (40, 100),
        'seasons': ['Winter', 'Spring'],
        'altitude_range': (1000, 3000),
        'ph_range': (5.0, 6.8),
        'description': 'Potatoes prefer cool weather and moderate moisture',
        'icon': '🥔'
    },
    'Tomato': {
        'temp_range': (18, 28),
        'rainfall_range': (50, 120),
        'seasons': ['Summer', 'Spring'],
        'altitude_range': (0, 2000),
        'ph_range': (6.0, 6.8),
        'description': 'Tomatoes thrive in warm weather with good drainage',
        'icon': '🍅'
    },
    'Onion': {
        'temp_range': (15, 25),
        'rainfall_range': (40, 80),
        'seasons': ['Winter', 'Spring'],
        'altitude_range': (0, 2500),
        'ph_range': (6.0, 7.5),
        'description': 'Onions prefer cool to moderate weather',
        'icon': '🧅'
    },
    'Cabbage': {
        'temp_range': (10, 20),
        'rainfall_range': (50, 100),
        'seasons': ['Winter', 'Spring'],
        'altitude_range': (0, 2500),
        'ph_range': (6.0, 7.5),
        'description': 'Cabbage thrives in cool weather',
        'icon': '🥬'
    },
    'Millet': {
        'temp_range': (22, 32),
        'rainfall_range': (40, 80),
        'seasons': ['Summer', 'Monsoon'],
        'altitude_range': (0, 1500),
        'ph_range': (5.0, 7.5),
        'description': 'Millet is drought-resistant and prefers warm climate',
        'icon': '🌾'
    },
    'Barley': {
        'temp_range': (8, 18),
        'rainfall_range': (30, 60),
        'seasons': ['Winter', 'Spring'],
        'altitude_range': (1500, 3500),
        'ph_range': (6.0, 8.5),
        'description': 'Barley prefers cool climate and low rainfall',
        'icon': '🌾'
    },
    'Lentil': {
        'temp_range': (10, 22),
        'rainfall_range': (30, 70),
        'seasons': ['Winter', 'Spring'],
        'altitude_range': (0, 2500),
        'ph_range': (5.5, 7.5),
        'description': 'Lentils are drought-tolerant legumes',
        'icon': '🫘'
    }
}

def recommend_crops(temperature, rainfall, season, altitude=1000):
    """
    Recommend crops based on climate parameters.
    
    Args:
        temperature: Average temperature in Celsius
        rainfall: Annual rainfall in mm
        season: Current season (Spring, Summer, Monsoon, Winter)
        altitude: Altitude in meters
    
    Returns:
        List of recommended crops sorted by suitability score
    """
    recommendations = []
    
    for crop, requirements in CROP_DATABASE.items():
        score = 0
        
        # Temperature suitability (0-30 points)
        temp_min, temp_max = requirements['temp_range']
        if temp_min <= temperature <= temp_max:
            # Peak at middle of range
            mid_temp = (temp_min + temp_max) / 2
            temp_score = 30 - abs(temperature - mid_temp) * (30 / ((temp_max - temp_min) / 2))
            score += max(0, temp_score)
        
        # Rainfall suitability (0-30 points)
        rain_min, rain_max = requirements['rainfall_range']
        if rain_min <= rainfall <= rain_max:
            mid_rain = (rain_min + rain_max) / 2
            rain_score = 30 - abs(rainfall - mid_rain) * (30 / ((rain_max - rain_min) / 2))
            score += max(0, rain_score)
        
        # Season suitability (0-25 points)
        if season in requirements['seasons']:
            score += 25
        
        # Altitude suitability (0-15 points)
        alt_min, alt_max = requirements['altitude_range']
        if alt_min <= altitude <= alt_max:
            score += 15
        
        if score > 0:
            recommendations.append({
                'crop': crop,
                'score': score,
                'icon': requirements['icon'],
                'description': requirements['description'],
                'temperature_range': f"{temp_min}°C - {temp_max}°C",
                'rainfall_range': f"{rain_min}mm - {rain_max}mm",
                'seasons': ', '.join(requirements['seasons'])
            })
    
    # Sort by score descending
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations

def get_suitability_score(temperature, rainfall, season, crop):
    """Get suitability score for a specific crop."""
    if crop not in CROP_DATABASE:
        return 0
    
    requirements = CROP_DATABASE[crop]
    score = 0
    
    # Temperature suitability
    temp_min, temp_max = requirements['temp_range']
    if temp_min <= temperature <= temp_max:
        score += 30
    
    # Rainfall suitability
    rain_min, rain_max = requirements['rainfall_range']
    if rain_min <= rainfall <= rain_max:
        score += 30
    
    # Season suitability
    if season in requirements['seasons']:
        score += 25
    
    return score

def get_crop_details(crop):
    """Get detailed information about a crop."""
    if crop in CROP_DATABASE:
        return CROP_DATABASE[crop]
    return None

def get_all_crops():
    """Get list of all recommended crops."""
    return list(CROP_DATABASE.keys())

def get_seasonal_crops(season):
    """Get crops suitable for a specific season."""
    suitable_crops = []
    for crop, requirements in CROP_DATABASE.items():
        if season in requirements['seasons']:
            suitable_crops.append(crop)
    return suitable_crops

def climate_classification(temperature, rainfall):
    """Classify climate based on temperature and rainfall."""
    if temperature > 25 and rainfall > 150:
        return "Tropical - Hot and Wet"
    elif temperature > 25 and rainfall <= 150:
        return "Subtropical - Hot and Dry"
    elif 15 <= temperature <= 25 and rainfall > 100:
        return "Temperate - Moderate and Wet"
    elif 15 <= temperature <= 25 and rainfall <= 100:
        return "Temperate - Moderate and Dry"
    elif temperature < 15 and rainfall > 50:
        return "Alpine - Cold and Wet"
    else:
        return "Alpine - Cold and Dry"
