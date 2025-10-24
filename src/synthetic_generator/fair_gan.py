import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sdv.tabular import CTGAN
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class FairDataGenerator:
    def __init__(self, epochs=100, batch_size=500):
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.scaler = StandardScaler()
        
    def generate_fair_data(self, original_data, num_samples=None, fair_columns=None):
        """Generate synthetic data with fairness constraints"""
        if num_samples is None:
            num_samples = len(original_data)
            
        if fair_columns is None:
            fair_columns = ['location', 'gender']
            
        # Train CTGAN model
        self.model = CTGAN(epochs=self.epochs, batch_size=self.batch_size)
        self.model.fit(original_data)
        
        # Generate synthetic data
        synthetic_data = self.model.sample(num_samples)
        
        # Apply fairness constraints by balancing protected attributes
        synthetic_data = self._balance_protected_attributes(synthetic_data, fair_columns)
        
        return synthetic_data
    
    def _balance_protected_attributes(self, data, protected_columns):
        """Balance protected attributes in the synthetic data"""
        balanced_data = data.copy()
        
        for column in protected_columns:
            if column in balanced_data.columns:
                # Get value counts and find target distribution
                value_counts = balanced_data[column].value_counts()
                target_count = value_counts.max()  # Aim for equal representation
                
                # Resample to balance
                balanced_samples = []
                for value in value_counts.index:
                    value_data = balanced_data[balanced_data[column] == value]
                    # Oversample underrepresented groups
                    if len(value_data) < target_count:
                        additional_needed = target_count - len(value_data)
                        additional_samples = value_data.sample(
                            n=additional_needed, 
                            replace=True,  # Allow sampling with replacement
                            random_state=42
                        )
                        balanced_samples.append(pd.concat([value_data, additional_samples]))
                    else:
                        balanced_samples.append(value_data)
                
                # Combine and shuffle
                balanced_data = pd.concat(balanced_samples, ignore_index=True)
                balanced_data = balanced_data.sample(frac=1, random_state=42).reset_index(drop=True)
        
        return balanced_data
    
    def validate_synthetic_data(self, original_data, synthetic_data, target_column='loan_approved'):
        """Validate the quality and fairness of synthetic data"""
        validation_report = {
            'size_comparison': {
                'original': len(original_data),
                'synthetic': len(synthetic_data)
            },
            'fairness_improvement': {}
        }
        
        # Compare distributions of key columns
        if target_column in original_data.columns and target_column in synthetic_data.columns:
            orig_approval = original_data[target_column].mean()
            synth_approval = synthetic_data[target_column].mean()
            validation_report['approval_rate'] = {
                'original': orig_approval,
                'synthetic': synth_approval,
                'difference': abs(orig_approval - synth_approval)
            }
        
        return validation_report
