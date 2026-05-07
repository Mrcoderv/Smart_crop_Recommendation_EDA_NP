# Machine Learning Crop Recommendation System

## Overview

This document provides comprehensive guidance on the Machine Learning-based crop recommendation system integrated into the Smart Crop Recommendation Application.

## Architecture

### Components

```
smart-agriculture/
├── models/
│   ├── train_model.py          # Training script
│   ├── crop_model.pkl          # Trained Random Forest model
│   ├── scaler.pkl              # StandardScaler for feature normalization
│   ├── label_encoder.pkl       # LabelEncoder for crop encoding
│   └── training_report.txt     # Training metrics and evaluation
├── utils/
│   ├── ml_predictor.py         # Core prediction logic
│   ├── model_loader.py         # Streamlit integration utilities
│   └── recommendation.py       # Rule-based recommendations
├── pages/
│   ├── 5_Crop_Recommendation_ML.py  # Updated recommendation page with ML
│   └── ...
├── tests/
│   └── test_ml_system.py       # Comprehensive test suite
└── data/
    └── crop_recommendation.csv # Training dataset
```

## Quick Start

### 1. Train the ML Model

```bash
# Navigate to project directory
cd /home/mrrv/Smartagri

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Train the model
python models/train_model.py
```

**Expected Output:**
```
==============================================================
🌾 CROP RECOMMENDATION MODEL TRAINING PIPELINE
==============================================================

✓ Data loaded successfully: 100 samples
  Columns: ['temperature', 'humidity', 'rainfall', 'nitrogen', 'phosphorus', 'potassium', 'crop']
  Unique crops: 10

📊 Data Preprocessing...
  Features: ['temperature', 'humidity', 'rainfall', 'nitrogen', 'phosphorus', 'potassium']
  Target classes: 10 crops
✓ Data preprocessing completed

🤖 Training Random Forest Model...
  Training samples: 80
  Testing samples: 20
✓ Model training completed

📈 Model Evaluation...
  Accuracy: 0.9500
  F1-Score (weighted): 0.9487

💾 Saving Model Artifacts...
✓ Model saved to models/crop_model.pkl
✓ Scaler saved to models/scaler.pkl
✓ Label encoder saved to models/label_encoder.pkl

==============================================================
✅ TRAINING PIPELINE COMPLETED SUCCESSFULLY!
==============================================================
```

### 2. Run the Streamlit Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

### 3. Use ML Predictions

Navigate to the "🤖 AI Prediction (ML)" tab on the Crop Recommendation page to make predictions.

## Model Details

### Algorithm: Random Forest Classifier

**Hyperparameters:**
- Number of trees: 100
- Max depth: 15
- Min samples split: 5
- Min samples leaf: 2
- Random state: 42

**Advantages:**
- Handles non-linear relationships
- Robust to outliers
- Provides feature importance scores
- Fast inference time

### Input Features (6)

| Feature | Range | Unit | Description |
|---------|-------|------|-------------|
| Temperature | 0-40 | °C | Average temperature during growing season |
| Humidity | 0-100 | % | Relative humidity percentage |
| Rainfall | 0-400 | mm | Annual or seasonal rainfall |
| Nitrogen (N) | 0-100 | mg/kg | Soil nitrogen content |
| Phosphorus (P) | 0-100 | mg/kg | Soil phosphorus content |
| Potassium (K) | 0-100 | mg/kg | Soil potassium content |

### Output Classes (10 Crops)

1. **Rice** 🍚 - Water-loving crop
2. **Wheat** 🌾 - Cold-hardy grain
3. **Maize** 🌽 - Warm-season crop
4. **Potato** 🥔 - Cool-season tuber
5. **Tomato** 🍅 - Commercial vegetable
6. **Onion** 🧅 - Long-day crop
7. **Cabbage** 🥬 - Brassica crop
8. **Millet** 🌾 - Drought-tolerant
9. **Barley** 🌾 - Cold-hardy grain
10. **Lentil** 🫘 - Legume crop

## Data Flow

```
User Input (6 parameters)
        ↓
Feature Normalization (StandardScaler)
        ↓
Random Forest Model
        ↓
Prediction Output
        ├── Predicted Crop
        ├── Confidence Score (0-100%)
        ├── Top 3 Recommendations
        └── All Crop Probabilities
```

## Model Performance

### Evaluation Metrics

- **Accuracy:** Percentage of correct predictions
- **F1-Score:** Harmonic mean of precision and recall
- **Confusion Matrix:** Shows prediction distribution
- **Classification Report:** Per-class metrics

### Training Report

After training, metrics are saved to `models/training_report.txt`:

```
CROP RECOMMENDATION MODEL - TRAINING REPORT
==================================================

Model: Random Forest Classifier
Training Date: [timestamp]

METRICS:
- Accuracy: 0.9500
- F1-Score (weighted): 0.9487

FEATURE IMPORTANCE:
  rainfall: 0.3245
  nitrogen: 0.2150
  humidity: 0.1998
  temperature: 0.1543
  phosphorus: 0.0512
  potassium: 0.0452
```

## Module Documentation

### 1. `models/train_model.py`

**Main Class: `CropRecommendationModel`**

Methods:
- `load_data()` - Load training dataset
- `preprocess_data()` - Clean and normalize data
- `train()` - Train Random Forest model
- `evaluate()` - Calculate metrics
- `save_model()` - Persist model artifacts
- `run_training_pipeline()` - Execute complete pipeline

Example:
```python
from models.train_model import CropRecommendationModel

trainer = CropRecommendationModel(model_dir='models')
trainer.run_training_pipeline(data_path='data/crop_recommendation.csv')
```

### 2. `utils/ml_predictor.py`

**Main Class: `MLCropPredictor`**

Methods:
- `load_model()` - Load trained model and scalers
- `is_model_loaded()` - Check model status
- `prepare_features()` - Normalize input features
- `predict()` - Make single prediction
- `batch_predict()` - Make multiple predictions
- `get_feature_importance()` - Get feature scores
- `get_all_crops()` - Get list of supported crops

Helper Functions:
- `get_crop_info()` - Get crop characteristics
- `get_suitability_message()` - Get confidence interpretation
- `get_confidence_color()` - Get color code for UI

Example:
```python
from utils.ml_predictor import MLCropPredictor

predictor = MLCropPredictor()
result = predictor.predict(
    temperature=25,
    humidity=65,
    rainfall=150,
    nitrogen=50,
    phosphorus=30,
    potassium=40
)

print(f"Predicted crop: {result['predicted_crop']}")
print(f"Confidence: {result['confidence']:.1f}%")
```

### 3. `utils/model_loader.py`

**Streamlit-specific utilities**

Functions:
- `load_ml_model()` - Load with Streamlit caching
- `check_model_availability()` - Verify model files exist
- `display_model_info()` - Show model metrics
- `display_prediction_result()` - Render prediction UI
- `display_feature_importance()` - Show feature chart
- `get_model_status()` - Get current status

Example:
```python
from utils.model_loader import load_ml_model, display_prediction_result

predictor = load_ml_model()
if predictor:
    result = predictor.predict(temp, humidity, rainfall, n, p, k)
    display_prediction_result(result)
```

## Integration with Streamlit

### Crop Recommendation Page (Updated)

**Three Tabs:**

1. **🤖 AI Prediction (ML)**
   - Input 6 parameters
   - Get ML predictions
   - View confidence scores
   - See top 3 recommendations

2. **📊 Rule-Based Recommendation**
   - Traditional approach
   - Based on climate and season
   - Detailed crop analysis

3. **📈 Model Analytics**
   - Feature importance visualization
   - Model information
   - Training metrics

### UI Components

- **Input Sliders:** 6 parameter inputs with appropriate ranges
- **Prediction Card:** Large, color-coded prediction display
- **Confidence Progress Bar:** Visual confidence representation
- **Recommendation List:** Top 3 crops with scores
- **Feature Importance Chart:** Interactive Plotly bar chart

## Testing

### Run All Tests

```bash
python tests/test_ml_system.py
```

### Test Coverage

```
✓ Data Preprocessing (3 tests)
✓ Model Training (3 tests)
✓ Model Persistence (1 test)
✓ ML Predictor (8 tests)
✓ Utility Functions (6 tests)
✓ Integration (1 test)
────────────────────────────
  Total: 22 tests
```

### Individual Test Examples

```python
# Run specific test class
python -m unittest tests.test_ml_system.TestDataPreprocessing

# Run specific test method
python -m unittest tests.test_ml_system.TestMLPredictor.test_prediction

# Run with verbose output
python -m unittest tests.test_ml_system -v
```

## Prediction Workflow

### Step-by-Step Process

```
1. User enters 6 parameters in Streamlit UI
   ↓
2. Input validation (range checks)
   ↓
3. Feature normalization using saved scaler
   ↓
4. Random Forest prediction
   ↓
5. Probability calculation for all crops
   ↓
6. Output formatting:
   - Predicted crop
   - Confidence score (highest probability)
   - Top 3 recommendations
   - All crop probabilities
   ↓
7. Streamlit UI rendering with:
   - Large prediction card
   - Color-coded confidence
   - Crop information
   - Suitability message
```

### Confidence Score Interpretation

| Confidence | Interpretation | Color |
|-----------|-----------------|-------|
| 80-100% | Highly Recommended | 🟢 Green |
| 60-79% | Well-Suited | 🟡 Orange |
| 40-59% | Fair | 🟠 Light Orange |
| 0-39% | Not Recommended | 🔴 Red |

## Advanced Features

### Feature Importance

Shows which factors most influence the prediction:

```python
importances = predictor.get_feature_importance()
# Output:
# {
#     'rainfall': 0.3245,
#     'nitrogen': 0.2150,
#     'humidity': 0.1998,
#     'temperature': 0.1543,
#     'phosphorus': 0.0512,
#     'potassium': 0.0452
# }
```

### Batch Prediction

Predict for multiple scenarios:

```python
import pandas as pd

data = pd.DataFrame({
    'temperature': [25, 20, 22],
    'humidity': [65, 55, 60],
    'rainfall': [150, 80, 100],
    'nitrogen': [50, 45, 48],
    'phosphorus': [30, 25, 28],
    'potassium': [40, 35, 38]
})

results = predictor.batch_predict(data)
print(results)
```

### Training with Custom Data

```python
from models.train_model import CropRecommendationModel

trainer = CropRecommendationModel()

# Use custom dataset
trainer.run_training_pipeline(data_path='data/custom_crops.csv')
```

## Troubleshooting

### Issue: "Model files not found"

**Solution:**
```bash
# Train the model first
python models/train_model.py

# Check files exist
ls -la models/*.pkl
```

### Issue: "Wrong number of features"

**Solution:**
Ensure input has exactly 6 features in correct order:
1. Temperature
2. Humidity
3. Rainfall
4. Nitrogen
5. Phosphorus
6. Potassium

### Issue: Low Accuracy

**Solutions:**
1. Check training data quality
2. Increase dataset size (currently 100 samples)
3. Adjust model hyperparameters in `train_model.py`
4. Add more diverse examples

### Issue: Streamlit Cache Errors

**Solution:**
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/

# Restart app
streamlit run app.py
```

## Dataset Format

### Training Data Structure

**File:** `data/crop_recommendation.csv`

**Format:** CSV with 7 columns

```csv
temperature,humidity,rainfall,nitrogen,phosphorus,potassium,crop
25,60,100,50,30,40,Rice
22,70,150,40,20,30,Rice
...
```

**Requirements:**
- No missing values (NaN)
- Numeric values for features
- String values for crop names
- Balanced classes recommended

## Performance Optimization

### Model Caching

Models are cached using Streamlit's `@st.cache_resource` decorator:
- Loads once on app startup
- Reuses across reruns
- Dramatically improves performance

### Feature Scaling

StandardScaler ensures:
- Features on same scale
- Better model performance
- Saved and reused during prediction

### Batch Processing

For multiple predictions:
```python
# More efficient than loop
results = predictor.batch_predict(df)
```

## Future Enhancements

### Potential Improvements

1. **More Crops:** Expand from 10 to 50+ crops
2. **More Features:** Add soil pH, EC, organic matter
3. **Advanced Models:** Try XGBoost, Neural Networks
4. **Temporal Data:** Include historical trends
5. **Location-Specific:** Train models per region
6. **Model Comparison:** Evaluate multiple algorithms
7. **Confidence Calibration:** Improve probability accuracy
8. **Real-time Retraining:** Update with new data

## Code Examples

### Example 1: Basic Prediction

```python
from utils.ml_predictor import MLCropPredictor

predictor = MLCropPredictor()

# Make prediction
result = predictor.predict(
    temperature=28,
    humidity=70,
    rainfall=120,
    nitrogen=40,
    phosphorus=35,
    potassium=45
)

if result['success']:
    print(f"Best crop: {result['predicted_crop']}")
    print(f"Confidence: {result['confidence']:.1f}%")
```

### Example 2: Feature Analysis

```python
# Get feature importance
importances = predictor.get_feature_importance()

# Get top 3 features
top_3 = predictor.get_top_features(3)
for feature, score in top_3:
    print(f"{feature}: {score:.4f}")
```

### Example 3: Custom Training

```python
from models.train_model import CropRecommendationModel

trainer = CropRecommendationModel()
success = trainer.run_training_pipeline('data/custom_data.csv')

if success:
    print("Model trained and saved!")
```

## References

- **scikit-learn Documentation:** https://scikit-learn.org/
- **Random Forest Paper:** Breiman, L. (2001)
- **Model Evaluation:** https://scikit-learn.org/modules/model_evaluation.html
- **Crop Science:** FAO Guidelines, Local Agricultural Data

## Support

For issues or questions:
1. Check `models/training_report.txt` for model metrics
2. Run test suite: `python tests/test_ml_system.py`
3. Review error messages in Streamlit terminal
4. Check data format in `data/crop_recommendation.csv`

---

**Version:** 1.0  
**Last Updated:** May 2026  
**Maintainer:** Smart Agriculture Team  
