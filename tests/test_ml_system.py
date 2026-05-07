"""
Test Suite for ML Crop Recommendation System
Tests training, prediction, and integration functionality
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path
import tempfile
import shutil
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.train_model import CropRecommendationModel
from utils.ml_predictor import MLCropPredictor, get_crop_info, get_suitability_message, CROP_CHARACTERISTICS


class TestDataPreprocessing(unittest.TestCase):
    """Test data loading and preprocessing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.trainer = CropRecommendationModel(model_dir='models_test')
    
    def tearDown(self):
        """Clean up test artifacts"""
        if os.path.exists('models_test'):
            shutil.rmtree('models_test')
    
    def test_data_loading(self):
        """Test if data loads successfully"""
        df = self.trainer.load_data('data/crop_recommendation.csv')
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)
        self.assertIn('crop', df.columns)
    
    def test_required_columns(self):
        """Test if all required columns exist"""
        df = self.trainer.load_data('data/crop_recommendation.csv')
        required_columns = ['temperature', 'humidity', 'rainfall', 'nitrogen', 'phosphorus', 'potassium', 'crop']
        for col in required_columns:
            self.assertIn(col, df.columns)
    
    def test_preprocessing(self):
        """Test data preprocessing"""
        df = self.trainer.load_data('data/crop_recommendation.csv')
        X_scaled, y_encoded, feature_names = self.trainer.preprocess_data(df)
        
        self.assertEqual(X_scaled.shape[0], len(df))
        self.assertEqual(X_scaled.shape[1], 6)  # 6 features
        self.assertEqual(len(feature_names), 6)


class TestModelTraining(unittest.TestCase):
    """Test model training functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.trainer = CropRecommendationModel(model_dir='models_test')
        df = self.trainer.load_data('data/crop_recommendation.csv')
        self.X_scaled, self.y_encoded, self.feature_names = self.trainer.preprocess_data(df)
    
    def tearDown(self):
        """Clean up test artifacts"""
        if os.path.exists('models_test'):
            shutil.rmtree('models_test')
    
    def test_model_training(self):
        """Test if model trains without errors"""
        X_test, y_test = self.trainer.train(self.X_scaled, self.y_encoded)
        
        self.assertIsNotNone(self.trainer.model)
        self.assertGreater(len(X_test), 0)
    
    def test_model_prediction_shape(self):
        """Test if model predictions have correct shape"""
        X_test, y_test = self.trainer.train(self.X_scaled, self.y_encoded)
        predictions = self.trainer.model.predict(X_test)
        
        self.assertEqual(len(predictions), len(X_test))
    
    def test_model_evaluation(self):
        """Test model evaluation metrics"""
        X_test, y_test = self.trainer.train(self.X_scaled, self.y_encoded)
        metrics = self.trainer.evaluate(X_test, y_test, self.feature_names)
        
        self.assertIn('accuracy', metrics)
        self.assertIn('f1_score', metrics)
        self.assertGreater(metrics['accuracy'], 0)
        self.assertLessEqual(metrics['accuracy'], 1)


class TestModelPersistence(unittest.TestCase):
    """Test model saving and loading"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.trainer = CropRecommendationModel(model_dir='models_test')
        df = self.trainer.load_data('data/crop_recommendation.csv')
        self.X_scaled, self.y_encoded, _ = self.trainer.preprocess_data(df)
        self.trainer.train(self.X_scaled, self.y_encoded)
    
    def tearDown(self):
        """Clean up test artifacts"""
        if os.path.exists('models_test'):
            shutil.rmtree('models_test')
    
    def test_model_saving(self):
        """Test if model saves successfully"""
        self.trainer.save_model()
        
        self.assertTrue(self.trainer.model_path.exists())
        self.assertTrue(self.trainer.scaler_path.exists())
        self.assertTrue(self.trainer.label_encoder_path.exists())


class TestMLPredictor(unittest.TestCase):
    """Test ML predictor class"""
    
    @classmethod
    def setUpClass(cls):
        """Train model once for all tests"""
        trainer = CropRecommendationModel(model_dir='models_test')
        df = trainer.load_data('data/crop_recommendation.csv')
        X_scaled, y_encoded, feature_names = trainer.preprocess_data(df)
        trainer.train(X_scaled, y_encoded)
        trainer.save_model()
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = MLCropPredictor(model_dir='models_test')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test artifacts"""
        if os.path.exists('models_test'):
            shutil.rmtree('models_test')
    
    def test_model_loading(self):
        """Test if model loads successfully"""
        self.assertTrue(self.predictor.is_model_loaded())
    
    def test_feature_preparation(self):
        """Test feature preparation"""
        features = self.predictor.prepare_features(25, 65, 150, 50, 30, 40)
        
        self.assertEqual(features.shape[0], 1)
        self.assertEqual(features.shape[1], 6)
    
    def test_prediction(self):
        """Test prediction functionality"""
        result = self.predictor.predict(25, 65, 150, 50, 30, 40)
        
        self.assertTrue(result['success'])
        self.assertIn('predicted_crop', result)
        self.assertIn('confidence', result)
        self.assertGreater(result['confidence'], 0)
        self.assertLessEqual(result['confidence'], 100)
    
    def test_crop_list(self):
        """Test getting list of all crops"""
        crops = self.predictor.get_all_crops()
        
        self.assertEqual(len(crops), 10)
        self.assertIn('Rice', crops)
        self.assertIn('Wheat', crops)
    
    def test_feature_importance(self):
        """Test getting feature importance"""
        importances = self.predictor.get_feature_importance()
        
        self.assertEqual(len(importances), 6)
        total_importance = sum(importances.values())
        self.assertAlmostEqual(total_importance, 1.0, places=1)
    
    def test_top_features(self):
        """Test getting top features"""
        top_features = self.predictor.get_top_features(3)
        
        self.assertEqual(len(top_features), 3)
        for feature, importance in top_features:
            self.assertIsInstance(feature, str)
            self.assertGreater(importance, 0)
    
    def test_batch_prediction(self):
        """Test batch prediction"""
        data = pd.DataFrame({
            'temperature': [25, 20, 22],
            'humidity': [65, 55, 60],
            'rainfall': [150, 80, 100],
            'nitrogen': [50, 45, 48],
            'phosphorus': [30, 25, 28],
            'potassium': [40, 35, 38]
        })
        
        results = self.predictor.batch_predict(data)
        
        self.assertEqual(len(results), 3)
        self.assertIn('predicted_crop', results.columns)
        self.assertIn('confidence', results.columns)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_crop_info(self):
        """Test getting crop information"""
        info = get_crop_info('Rice')
        
        self.assertIsNotNone(info)
        self.assertIn('optimal_temp', info)
        self.assertIn('optimal_rainfall', info)
        self.assertIn('seasons', info)
        self.assertIn('emoji', info)
    
    def test_invalid_crop_info(self):
        """Test getting info for non-existent crop"""
        info = get_crop_info('InvalidCrop')
        
        self.assertEqual(info, {})
    
    def test_suitability_message_excellent(self):
        """Test suitability message for high confidence"""
        msg = get_suitability_message(85)
        
        self.assertIn('Excellent', msg)
    
    def test_suitability_message_good(self):
        """Test suitability message for medium confidence"""
        msg = get_suitability_message(70)
        
        self.assertIn('Good', msg)
    
    def test_suitability_message_fair(self):
        """Test suitability message for low-medium confidence"""
        msg = get_suitability_message(50)
        
        self.assertIn('Fair', msg)
    
    def test_suitability_message_poor(self):
        """Test suitability message for very low confidence"""
        msg = get_suitability_message(30)
        
        self.assertIn('Poor', msg)
    
    def test_crop_characteristics(self):
        """Test crop characteristics database"""
        self.assertEqual(len(CROP_CHARACTERISTICS), 10)
        
        for crop_name, info in CROP_CHARACTERISTICS.items():
            self.assertIn('optimal_temp', info)
            self.assertIn('optimal_rainfall', info)
            self.assertIn('seasons', info)
            self.assertIn('emoji', info)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    @classmethod
    def setUpClass(cls):
        """Train model once for all tests"""
        trainer = CropRecommendationModel(model_dir='models_test')
        df = trainer.load_data('data/crop_recommendation.csv')
        X_scaled, y_encoded, _ = trainer.preprocess_data(df)
        trainer.train(X_scaled, y_encoded)
        trainer.save_model()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test artifacts"""
        if os.path.exists('models_test'):
            shutil.rmtree('models_test')
    
    def test_end_to_end_prediction(self):
        """Test complete prediction pipeline"""
        predictor = MLCropPredictor(model_dir='models_test')
        
        # Test various scenarios
        test_cases = [
            (25, 65, 150, 50, 30, 40),  # Rice conditions
            (15, 50, 80, 45, 25, 35),   # Wheat conditions
            (28, 70, 120, 40, 35, 45),  # Tomato conditions
        ]
        
        for temp, humidity, rainfall, n, p, k in test_cases:
            result = predictor.predict(temp, humidity, rainfall, n, p, k)
            self.assertTrue(result['success'])
            self.assertIn('predicted_crop', result)
            self.assertGreater(result['confidence'], 0)


def run_tests(verbose=2):
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataPreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestModelTraining))
    suite.addTests(loader.loadTestsFromTestCase(TestModelPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestMLPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbose)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🧪 RUNNING CROP RECOMMENDATION ML SYSTEM TESTS")
    print("="*70 + "\n")
    
    result = run_tests(verbose=2)
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    exit(0 if result.wasSuccessful() else 1)
