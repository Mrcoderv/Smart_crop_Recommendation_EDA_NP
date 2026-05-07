"""
Machine Learning Model Training Script
Trains a Random Forest Classifier for crop recommendation
Saves the model, scaler, and label encoder for later use
"""

import pandas as pd
import numpy as np
import pickle
import joblib
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
import warnings
warnings.filterwarnings('ignore')


class CropRecommendationModel:
    """Machine Learning model for crop recommendation"""
    
    def __init__(self, model_dir='models'):
        """Initialize model paths"""
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.model_path = self.model_dir / 'crop_model.pkl'
        self.scaler_path = self.model_dir / 'scaler.pkl'
        self.label_encoder_path = self.model_dir / 'label_encoder.pkl'
        self.training_report_path = self.model_dir / 'training_report.txt'
        
        self.model = None
        self.scaler = None
        self.label_encoder = None
    
    def load_data(self, data_path='data/crop_recommendation.csv'):
        """Load crop recommendation dataset"""
        try:
            df = pd.read_csv(data_path)
            print(f"✓ Data loaded successfully: {len(df)} samples")
            print(f"  Columns: {list(df.columns)}")
            print(f"  Unique crops: {df['crop'].nunique()}")
            return df
        except FileNotFoundError:
            print(f"✗ Dataset not found at {data_path}")
            return None
    
    def preprocess_data(self, df):
        """
        Preprocess data: handle missing values, encode, scale
        """
        print("\n📊 Data Preprocessing...")
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.any():
            print(f"⚠ Missing values found:\n{missing}")
            df = df.dropna()
            print(f"✓ Removed {len(df)} rows with missing values")
        
        # Separate features and target
        X = df.drop('crop', axis=1)
        y = df['crop']
        
        print(f"  Features: {list(X.columns)}")
        print(f"  Target classes: {len(y.unique())} crops")
        
        # Encode target variable
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"  Crop classes: {dict(zip(self.label_encoder.classes_, self.label_encoder.transform(self.label_encoder.classes_)))}")
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        print(f"✓ Data preprocessing completed")
        print(f"  Dataset size: {X_scaled.shape}")
        
        return X_scaled, y_encoded, X.columns.tolist()
    
    def train(self, X_scaled, y_encoded, test_size=0.2, random_state=42):
        """
        Train Random Forest Classifier
        """
        print("\n🤖 Training Random Forest Model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
        )
        
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
            verbose=0
        )
        
        self.model.fit(X_train, y_train)
        print(f"✓ Model training completed")
        
        return X_test, y_test
    
    def evaluate(self, X_test, y_test, feature_names):
        """
        Evaluate model performance
        """
        print("\n📈 Model Evaluation...")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  F1-Score (weighted): {f1:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(cm)
        
        # Classification Report
        report = classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_,
            digits=4
        )
        print(f"\nClassification Report:")
        print(report)
        
        # Feature Importance
        print(f"\n🔍 Feature Importance:")
        importances = self.model.feature_importances_
        feature_importance = dict(zip(feature_names, importances))
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        for feature, importance in sorted_features:
            print(f"  {feature}: {importance:.4f}")
        
        # Save report
        report_text = f"""CROP RECOMMENDATION MODEL - TRAINING REPORT
{'='*50}

Model: Random Forest Classifier
Training Date: {pd.Timestamp.now()}

METRICS:
- Accuracy: {accuracy:.4f}
- F1-Score (weighted): {f1:.4f}

CONFUSION MATRIX:
{cm}

CLASSIFICATION REPORT:
{report}

FEATURE IMPORTANCE:
"""
        for feature, importance in sorted_features:
            report_text += f"\n  {feature}: {importance:.4f}"
        
        with open(self.training_report_path, 'w') as f:
            f.write(report_text)
        
        print(f"✓ Training report saved to {self.training_report_path}")
        
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'confusion_matrix': cm,
            'report': report,
            'feature_importance': feature_importance
        }
    
    def save_model(self):
        """Save trained model, scaler, and label encoder"""
        print("\n💾 Saving Model Artifacts...")
        
        # Save model
        joblib.dump(self.model, self.model_path)
        print(f"✓ Model saved to {self.model_path}")
        
        # Save scaler
        joblib.dump(self.scaler, self.scaler_path)
        print(f"✓ Scaler saved to {self.scaler_path}")
        
        # Save label encoder
        joblib.dump(self.label_encoder, self.label_encoder_path)
        print(f"✓ Label encoder saved to {self.label_encoder_path}")
    
    def run_training_pipeline(self, data_path='data/crop_recommendation.csv'):
        """Execute complete training pipeline"""
        print("\n" + "="*60)
        print("🌾 CROP RECOMMENDATION MODEL TRAINING PIPELINE")
        print("="*60)
        
        # Load data
        df = self.load_data(data_path)
        if df is None:
            return False
        
        # Preprocess
        X_scaled, y_encoded, feature_names = self.preprocess_data(df)
        
        # Train
        X_test, y_test = self.train(X_scaled, y_encoded)
        
        # Evaluate
        metrics = self.evaluate(X_test, y_test, feature_names)
        
        # Save
        self.save_model()
        
        print("\n" + "="*60)
        print("✅ TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📁 Model files location: {self.model_dir}")
        print(f"   - Model: {self.model_path}")
        print(f"   - Scaler: {self.scaler_path}")
        print(f"   - Label Encoder: {self.label_encoder_path}")
        print("\n🚀 Ready to use in Streamlit app!")
        
        return True


def main():
    """Main training function"""
    # Initialize model trainer
    trainer = CropRecommendationModel(model_dir='models')
    
    # Run training pipeline
    success = trainer.run_training_pipeline(data_path='data/crop_recommendation.csv')
    
    if success:
        print("\n✨ Model is ready for deployment!")
    else:
        print("\n❌ Training failed. Check the errors above.")


if __name__ == '__main__':
    main()
