import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from synthetic_generator.fair_gan import FairDataGenerator
from synthetic_generator.data_validator import DataValidator

class TestSyntheticData(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        np.random.seed(42)
        self.sample_data = pd.DataFrame({
            'age': np.random.randint(20, 60, 100),
            'location': np.random.choice([0, 1], 100, p=[0.7, 0.3]),  # 0: Urban, 1: Rural
            'gender': np.random.choice([0, 1], 100, p=[0.6, 0.4]),    # 0: Male, 1: Female
            'income': np.random.normal(50000, 20000, 100),
            'loan_approved': np.random.choice([0, 1], 100, p=[0.4, 0.6])
        })
        
        self.generator = FairDataGenerator(epochs=10)  # Few epochs for testing
        self.validator = DataValidator()
    
    def test_generator_initialization(self):
        """Test that generator initializes correctly"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.epochs, 10)
    
    def test_synthetic_data_generation(self):
        """Test synthetic data generation"""
        synthetic_data = self.generator.generate_fair_data(self.sample_data, num_samples=50)
        
        self.assertIsNotNone(synthetic_data)
        self.assertEqual(len(synthetic_data), 50)
        self.assertEqual(synthetic_data.shape[1], self.sample_data.shape[1])
    
    def test_data_validation(self):
        """Test data validation functionality"""
        synthetic_data = self.generator.generate_fair_data(self.sample_data, num_samples=100)
        validation_report = self.validator.validate_synthetic_data(
            self.sample_data, synthetic_data, 'loan_approved'
        )
        
        self.assertIn('statistical_similarity', validation_report)
        self.assertIn('machine_learning_utility', validation_report)
        self.assertIn('fairness_metrics', validation_report)

if __name__ == '__main__':
    unittest.main()
