import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class BiasDashboard:
    def __init__(self):
        self.set_style()
    
    def set_style(self):
        """Set consistent plotting style"""
        plt.style.use('default')
        sns.set_palette("husl")
        
    def create_bias_comparison_plot(self, original_report, synthetic_report, save_path=None):
        """Create comparison plot between original and synthetic data bias"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Original data bias
        self._plot_bias_metrics(original_report, axes[0], "Original Data Bias Analysis")
        
        # Synthetic data bias
        self._plot_bias_metrics(synthetic_report, axes[1], "Synthetic Data Bias Analysis")
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        return fig
    
    def _plot_bias_metrics(self, report, ax, title):
        """Plot bias metrics for a single dataset"""
        if 'bias_metrics' not in report:
            ax.text(0.5, 0.5, 'No bias metrics available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return
        
        attributes = []
        di_ratios = []
        is_biased = []
        
        for attr, metrics in report['bias_metrics'].items():
            if isinstance(metrics, dict) and 'disparate_impact' in metrics:
                attributes.append(attr)
                di_ratios.append(metrics['disparate_impact'])
                is_biased.append(metrics['is_biased'])
        
        colors = ['red' if biased else 'green' for biased in is_biased]
        
        bars = ax.bar(attributes, di_ratios, color=colors, alpha=0.7)
        ax.set_title(title)
        ax.set_ylabel('Disparate Impact Ratio')
        ax.set_ylim(0, 1.1)
        ax.axhline(y=0.8, color='black', linestyle='--', alpha=0.7, label='Fairness Threshold')
        
        # Add value labels on bars
        for bar, ratio in zip(bars, di_ratios):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{ratio:.3f}', ha='center', va='bottom')
        
        ax.legend()
    
    def create_interactive_fairness_dashboard(self, original_data, synthetic_data, protected_attributes):
        """Create an interactive Plotly dashboard for fairness analysis"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Approval Rates by Group', 'Disparate Impact Comparison',
                          'Feature Distribution', 'Model Performance'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Add your Plotly visualization code here
        # This would include interactive charts comparing original vs synthetic data
        
        fig.update_layout(height=800, title_text="FairLend Kenya - Fairness Analysis Dashboard")
        return fig
    
    def generate_comprehensive_report(self, original_data, synthetic_data, validation_report, save_path='fairness_report.html'):
        """Generate a comprehensive HTML report"""
        from datetime import datetime
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>FairLend Kenya - Bias Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #2E86AB; color: white; padding: 20px; border-radius: 10px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #2E86AB; background-color: #f9f9f9; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #e8e8e8; border-radius: 5px; }}
                .improvement {{ color: green; font-weight: bold; }}
                .warning {{ color: orange; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🇰🇪 FairLend Kenya - Bias Analysis Report</h1>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <p>Analysis of bias mitigation through synthetic data generation for credit risk assessment in Kenya.</p>
            </div>
            
            <div class="section">
                <h2>📈 Key Metrics</h2>
                <div class="metric">
                    <h3>Original Data Size</h3>
                    <p>{len(original_data)} records</p>
                </div>
                <div class="metric">
                    <h3>Synthetic Data Size</h3>
                    <p>{len(synthetic_data)} records</p>
                </div>
                <div class="metric">
                    <h3>ML Utility Score</h3>
                    <p>{validation_report.get('machine_learning_utility', {}).get('accuracy', 'N/A')}</p>
                </div>
            </div>
            
            <div class="section">
                <h2>✅ Fairness Improvements</h2>
                <p>Analysis of disparate impact across protected attributes:</p>
                <!-- Add dynamic fairness metrics here -->
            </div>
            
            <div class="section">
                <h2>🎯 Recommendations</h2>
                <ul>
                    <li>Use synthetic data for training fair credit models</li>
                    <li>Monitor model performance across demographic groups</li>
                    <li>Regularly update synthetic data generation process</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        with open(save_path, 'w') as f:
            f.write(html_content)
        
        return save_path
