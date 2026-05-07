"""
Machine Learning Predictor Module
Provides prediction utilities for crop recommendation
Handles model loading, feature preparation, and prediction
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')


class MLCropPredictor:
    """Machine Learning based crop predictor"""
    
    def __init__(self, model_dir='models'):
        """Initialize predictor with model paths"""
        self.model_dir = Path(model_dir)
        self.model_path = self.model_dir / 'crop_model.pkl'
        self.scaler_path = self.model_dir / 'scaler.pkl'
        self.label_encoder_path = self.model_dir / 'label_encoder.pkl'
        
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = ['temperature', 'humidity', 'rainfall', 'nitrogen', 'phosphorus', 'potassium']
        
        self.load_model()
    
    def load_model(self) -> bool:
        """Load trained model and scalers"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            self.label_encoder = joblib.load(self.label_encoder_path)
            return True
        except FileNotFoundError as e:
            print(f"⚠️ Model files not found: {e}")
            print("Please train the model first using: python models/train_model.py")
            return False
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.scaler is not None and self.label_encoder is not None
    
    def prepare_features(self, temperature: float, humidity: float, rainfall: float,
                        nitrogen: float, phosphorus: float, potassium: float) -> np.ndarray:
        """
        Prepare features for prediction
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage (0-100)
            rainfall: Rainfall in mm
            nitrogen: Nitrogen content
            phosphorus: Phosphorus content
            potassium: Potassium content
        
        Returns:
            Scaled feature array
        """
        features = np.array([[temperature, humidity, rainfall, nitrogen, phosphorus, potassium]])
        scaled_features = self.scaler.transform(features)
        return scaled_features
    
    def predict(self, temperature: float, humidity: float, rainfall: float,
               nitrogen: float, phosphorus: float, potassium: float) -> Dict:
        """
        Predict suitable crop and get confidence scores
        
        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage (0-100)
            rainfall: Rainfall in mm
            nitrogen: Nitrogen content
            phosphorus: Phosphorus content
            potassium: Potassium content
        
        Returns:
            Dictionary with prediction details
        """
        if not self.is_model_loaded():
            return {
                'success': False,
                'message': 'Model not loaded. Please train the model first.'
            }
        
        try:
            # Prepare features
            scaled_features = self.prepare_features(temperature, humidity, rainfall,
                                                    nitrogen, phosphorus, potassium)
            
            # Make prediction
            prediction = self.model.predict(scaled_features)[0]
            probabilities = self.model.predict_proba(scaled_features)[0]
            
            # Get crop name
            predicted_crop = self.label_encoder.inverse_transform([prediction])[0]
            
            # Get confidence
            confidence = probabilities[prediction] * 100
            
            # Get top 3 recommendations with scores
            top_3_indices = np.argsort(probabilities)[::-1][:3]
            top_recommendations = []
            for idx in top_3_indices:
                crop_name = self.label_encoder.inverse_transform([idx])[0]
                confidence_score = probabilities[idx] * 100
                top_recommendations.append({
                    'crop': crop_name,
                    'confidence': confidence_score
                })
            
            return {
                'success': True,
                'predicted_crop': predicted_crop,
                'confidence': confidence,
                'all_probabilities': dict(zip(self.label_encoder.classes_, probabilities * 100)),
                'top_3_recommendations': top_recommendations
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Prediction error: {str(e)}'
            }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from trained model
        
        Returns:
            Dictionary with feature names and importance scores
        """
        if not self.is_model_loaded():
            return {}
        
        importances = self.model.feature_importances_
        return dict(zip(self.feature_names, importances))
    
    def get_top_features(self, top_n: int = 3) -> List[Tuple[str, float]]:
        """
        Get top N most important features
        
        Args:
            top_n: Number of top features to return
        
        Returns:
            List of tuples (feature_name, importance_score)
        """
        importances = self.get_feature_importance()
        sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)
        return sorted_features[:top_n]
    
    def get_all_crops(self) -> List[str]:
        """Get list of all supported crops"""
        if not self.is_model_loaded():
            return []
        return list(self.label_encoder.classes_)
    
    def batch_predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions for multiple samples
        
        Args:
            data: DataFrame with columns [temperature, humidity, rainfall, nitrogen, phosphorus, potassium]
        
        Returns:
            DataFrame with predictions and confidence scores
        """
        if not self.is_model_loaded():
            return pd.DataFrame()
        
        predictions = []
        for _, row in data.iterrows():
            result = self.predict(
                row['temperature'],
                row['humidity'],
                row['rainfall'],
                row['nitrogen'],
                row['phosphorus'],
                row['potassium']
            )
            if result['success']:
                predictions.append({
                    'predicted_crop': result['predicted_crop'],
                    'confidence': result['confidence']
                })
        
        return pd.DataFrame(predictions)


# Crop characteristics database for additional context
CROP_CHARACTERISTICS = {
    'Rice': {
        'optimal_temp': '20-30°C',
        'optimal_rainfall': '150-250mm',
        'seasons': ['Monsoon', 'Winter'],
        'description': 'Water-loving crop, needs consistent moisture',
        'emoji': '🍚'
    },
    'Wheat': {
        'optimal_temp': '10-25°C',
        'optimal_rainfall': '40-100mm',
        'seasons': ['Winter', 'Spring'],
        'description': 'Cold-hardy grain crop',
        'emoji': '🌾'
    },
    'Maize': {
        'optimal_temp': '21-27°C',
        'optimal_rainfall': '50-100mm',
        'seasons': ['Summer', 'Monsoon'],
        'description': 'Warm-season crop with high yield potential',
        'emoji': '🌽'
    },
    'Potato': {
        'optimal_temp': '15-20°C',
        'optimal_rainfall': '50-70mm',
        'seasons': ['Winter', 'Spring'],
        'description': 'Cool-season tuber crop',
        'emoji': '🥔'
    },
    'Tomato': {
        'optimal_temp': '25-30°C',
        'optimal_rainfall': '60-100mm',
        'seasons': ['Summer', 'Spring'],
        'description': 'Warm-season vegetable with commercial value',
        'emoji': '🍅'
    },
    'Onion': {
        'optimal_temp': '13-24°C',
        'optimal_rainfall': '40-60mm',
        'seasons': ['Winter', 'Spring'],
        'description': 'Long-day crop, requires dry season',
        'emoji': '🧅'
    },
    'Cabbage': {
        'optimal_temp': '15-20°C',
        'optimal_rainfall': '50-80mm',
        'seasons': ['Winter', 'Spring'],
        'description': 'Cool-season brassica crop',
        'emoji': '🥬'
    },
    'Millet': {
        'optimal_temp': '25-35°C',
        'optimal_rainfall': '40-70mm',
        'seasons': ['Summer', 'Monsoon'],
        'description': 'Drought-tolerant cereal crop',
        'emoji': '🌾'
    },
    'Barley': {
        'optimal_temp': '10-15°C',
        'optimal_rainfall': '30-50mm',
        'seasons': ['Winter', 'Spring'],
        'description': 'Cold-hardy grain for malting',
        'emoji': '🌾'
    },
    'Lentil': {
        'optimal_temp': '10-20°C',
        'optimal_rainfall': '40-70mm',
        'seasons': ['Winter', 'Spring'],
        'description': 'Nitrogen-fixing legume crop',
        'emoji': '🫘'
    }
}


def get_crop_info(crop_name: str) -> Dict:
    """Get detailed information about a crop"""
    return CROP_CHARACTERISTICS.get(crop_name, {})


def get_suitability_message(confidence: float) -> str:
    """Get suitability message based on confidence score"""
    if confidence >= 80:
        return "🌟 Excellent - Highly recommended for this region"
    elif confidence >= 60:
        return "✅ Good - Well-suited crop for these conditions"
    elif confidence >= 40:
        return "⚠️ Fair - Possible but suboptimal conditions"
    else:
        return "❌ Poor - Not recommended for these conditions"


def get_confidence_color(confidence: float) -> str:
    """Get color code based on confidence score"""
    if confidence >= 80:
        return '#27ae60'  # Green
    elif confidence >= 60:
        return '#f39c12'  # Orange
    else:
        return '#e74c3c'  # Red
