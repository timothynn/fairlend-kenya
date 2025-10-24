import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processing.bias_detector import BiasDetector

class TestBiasDetection(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = pd.DataFrame({
            'age': np.random.randint(20, 60, 100),
            'location': np.random.choice(['Nairobi', 'Mombasa', 'Rural'], 100, p=[0.6, 0.3, 0.1]),
            'gender': np.random.choice(['Male', 'Female'], 100, p=[0.7, 0.3]),
            'loan_approved': np.random.choice([0, 1], 100, p=[0.4, 0.6])
        })
        
        self.detector = BiasDetector()
    
    def test_bias_detection_initialization(self):
        """Test that bias detector initializes correctly"""
        self.assertIsNotNone(self.detector)
        self.assertIn('location', self.detector.protected_attributes)
    
    def test_analyze_dataset(self):
        """Test dataset analysis functionality"""
        report = self.detector.analyze_dataset(self.sample_data)
        
        self.assertIn('dataset_shape', report)
        self.assertIn('bias_metrics', report)
        self.assertEqual(report['dataset_shape'], self.sample_data.shape)
    
    def test_disparate_impact_calculation(self):
        """Test disparate impact calculation"""
        # Create intentionally biased data
        biased_data = pd.DataFrame({
            'location': ['Urban'] * 50 + ['Rural'] * 50,
            'loan_approved': [1] * 40 + [0] * 10 + [1] * 10 + [0] * 40
        })
        
        metrics = self.detector._calculate_disparate_impact(biased_data, 'location')
        
        self.assertIn('disparate_impact', metrics)
        self.assertIn('is_biased', metrics)
        self.assertTrue(metrics['is_biased'])  # Should detect bias

if __name__ == '__main__':
    unittest.main()
