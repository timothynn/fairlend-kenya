import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class DataValidator:
    def __init__(self):
        self.validation_results = {}
    
    def validate_synthetic_data(self, original_data, synthetic_data, target_column='loan_approved'):
        """Comprehensive validation of synthetic data quality"""
        validation_report = {
            'statistical_similarity': {},
            'machine_learning_utility': {},
            'fairness_metrics': {},
            'privacy_metrics': {}
        }
        
        # Statistical similarity
        validation_report['statistical_similarity'] = self._validate_statistical_similarity(
            original_data, synthetic_data, target_column
        )
        
        # ML utility
        validation_report['machine_learning_utility'] = self._validate_ml_utility(
            original_data, synthetic_data, target_column
        )
        
        # Fairness improvement
        validation_report['fairness_metrics'] = self._validate_fairness_improvement(
            original_data, synthetic_data, target_column
        )
        
        return validation_report
    
    def _validate_statistical_similarity(self, original, synthetic, target_column):
        """Validate statistical properties between original and synthetic data"""
        results = {}
        
        numerical_cols = original.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col != target_column:
                # Kolmogorov-Smirnov test for distribution similarity
                ks_statistic, ks_pvalue = stats.ks_2samp(original[col], synthetic[col])
                results[col] = {
                    'ks_statistic': ks_statistic,
                    'ks_pvalue': ks_pvalue,
                    'distribution_similar': ks_pvalue > 0.05  # Similar if p > 0.05
                }
        
        return results
    
    def _validate_ml_utility(self, original, synthetic, target_column):
        """Validate that synthetic data maintains machine learning utility"""
        if target_column not in original.columns:
            return {"error": f"Target column '{target_column}' not found"}
        
        # Prepare features
        feature_cols = [col for col in original.columns if col != target_column]
        X_original = original[feature_cols]
        y_original = original[target_column]
        X_synthetic = synthetic[feature_cols]
        y_synthetic = synthetic[target_column]
        
        # Split original data
        X_orig_train, X_orig_test, y_orig_train, y_orig_test = train_test_split(
            X_original, y_original, test_size=0.3, random_state=42
        )
        
        # Train model on synthetic data, test on original
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_synthetic, y_synthetic)
        
        # Predict on original test data
        y_pred = model.predict(X_orig_test)
        y_pred_proba = model.predict_proba(X_orig_test)[:, 1]
        
        accuracy = accuracy_score(y_orig_test, y_pred)
        auc_score = roc_auc_score(y_orig_test, y_pred_proba)
        
        return {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'model_performance': 'Good' if accuracy > 0.7 and auc_score > 0.7 else 'Needs Improvement'
        }
    
    def _validate_fairness_improvement(self, original, synthetic, target_column):
        """Validate improvement in fairness metrics"""
        from ..data_processing.bias_detector import BiasDetector
        
        detector = BiasDetector()
        
        # Calculate bias in original data
        original_bias = detector.analyze_dataset(original)
        synthetic_bias = detector.analyze_dataset(synthetic)
        
        fairness_improvement = {}
        
        for attr in original_bias['bias_metrics']:
            if attr in synthetic_bias['bias_metrics']:
                orig_di = original_bias['bias_metrics'][attr]['disparate_impact']
                synth_di = synthetic_bias['bias_metrics'][attr]['disparate_impact']
                
                improvement = synth_di - orig_di
                fairness_improvement[attr] = {
                    'original_di': orig_di,
                    'synthetic_di': synth_di,
                    'improvement': improvement,
                    'improvement_percentage': (improvement / orig_di) * 100 if orig_di > 0 else 0
                }
        
        return fairness_improvement
    
    def generate_validation_report(self, validation_report, save_path=None):
        """Generate a comprehensive validation report"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Statistical similarity
        stats_data = validation_report['statistical_similarity']
        if stats_data:
            ks_pvalues = [v['ks_pvalue'] for v in stats_data.values()]
            axes[0,0].bar(range(len(ks_pvalues)), ks_pvalues)
            axes[0,0].set_title('Statistical Similarity (KS Test P-values)')
            axes[0,0].set_ylabel('P-value')
            axes[0,0].axhline(y=0.05, color='r', linestyle='--', label='Significance Threshold')
        
        # Plot 2: ML Utility
        ml_data = validation_report['machine_learning_utility']
        if 'accuracy' in ml_data and 'auc_score' in ml_data:
            metrics = ['Accuracy', 'AUC Score']
            scores = [ml_data['accuracy'], ml_data['auc_score']]
            axes[0,1].bar(metrics, scores, color=['skyblue', 'lightgreen'])
            axes[0,1].set_title('Machine Learning Utility')
            axes[0,1].set_ylabel('Score')
            axes[0,1].set_ylim(0, 1)
        
        # Plot 3: Fairness Improvement
        fairness_data = validation_report['fairness_metrics']
        if fairness_data:
            attributes = list(fairness_data.keys())
            original_di = [fairness_data[attr]['original_di'] for attr in attributes]
            synthetic_di = [fairness_data[attr]['synthetic_di'] for attr in attributes]
            
            x = np.arange(len(attributes))
            width = 0.35
            
            axes[1,0].bar(x - width/2, original_di, width, label='Original', color='red', alpha=0.7)
            axes[1,0].bar(x + width/2, synthetic_di, width, label='Synthetic', color='green', alpha=0.7)
            axes[1,0].set_title('Fairness Improvement (Disparate Impact)')
            axes[1,0].set_ylabel('Disparate Impact Ratio')
            axes[1,0].set_xticks(x)
            axes[1,0].set_xticklabels(attributes)
            axes[1,0].legend()
            axes[1,0].axhline(y=0.8, color='black', linestyle='--', alpha=0.5, label='Fairness Threshold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        return fig
