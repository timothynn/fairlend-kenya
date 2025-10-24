import pandas as pd
import numpy as np
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing
import matplotlib.pyplot as plt
import seaborn as sns

class BiasDetector:
    def __init__(self):
        self.protected_attributes = ['location', 'gender', 'business_type']
        
    def analyze_dataset(self, data_path):
        """Comprehensive bias analysis of credit dataset"""
        df = pd.read_csv(data_path)
        
        # Basic statistics
        report = {
            'dataset_shape': df.shape,
            'approval_rate': df['loan_approved'].mean() if 'loan_approved' in df.columns else None,
            'bias_metrics': {}
        }
        
        # Check for disparate impact across protected attributes
        for attr in self.protected_attributes:
            if attr in df.columns:
                bias_metric = self._calculate_disparate_impact(df, attr)
                report['bias_metrics'][attr] = bias_metric
                
        return report
    
    def _calculate_disparate_impact(self, df, protected_attribute):
        """Calculate disparate impact ratio"""
        if 'loan_approved' not in df.columns:
            return "Target column 'loan_approved' not found"
            
        unique_values = df[protected_attribute].unique()
        if len(unique_values) < 2:
            return f"Not enough unique values in {protected_attribute}"
            
        # Calculate approval rates for each group
        approval_rates = {}
        for value in unique_values:
            group_data = df[df[protected_attribute] == value]
            approval_rates[value] = group_data['loan_approved'].mean()
            
        # Calculate disparate impact ratio
        min_rate = min(approval_rates.values())
        max_rate = max(approval_rates.values())
        disparate_impact = min_rate / max_rate if max_rate > 0 else 0
        
        return {
            'approval_rates': approval_rates,
            'disparate_impact': disparate_impact,
            'is_biased': disparate_impact < 0.8  # Common threshold
        }
    
    def generate_bias_report(self, report, save_path=None):
        """Generate visual bias report"""
        fig, axes = plt.subplots(1, len(report['bias_metrics']), figsize=(15, 5))
        
        for i, (attr, metrics) in enumerate(report['bias_metrics'].items()):
            if isinstance(metrics, dict) and 'approval_rates' in metrics:
                groups = list(metrics['approval_rates'].keys())
                rates = list(metrics['approval_rates'].values())
                
                ax = axes[i] if len(report['bias_metrics']) > 1 else axes
                bars = ax.bar(groups, rates, color=['skyblue', 'lightcoral'])
                
                # Color the biased groups
                if metrics['is_biased']:
                    min_rate = min(rates)
                    max_rate = max(rates)
                    for j, rate in enumerate(rates):
                        if rate == min_rate:
                            bars[j].set_color('red')
                        elif rate == max_rate:
                            bars[j].set_color('green')
                
                ax.set_title(f'Approval Rates by {attr.title()}')
                ax.set_ylabel('Approval Rate')
                ax.set_xlabel(attr.title())
                
                # Add disparate impact ratio
                ax.text(0.5, -0.2, f'DI Ratio: {metrics["disparate_impact"]:.3f}', 
                       transform=ax.transAxes, ha='center', fontweight='bold',
                       color='red' if metrics['is_biased'] else 'green')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
