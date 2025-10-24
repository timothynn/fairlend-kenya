import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def clean_credit_data(self, df):
        """Clean and preprocess credit data for Kenyan context"""
        logger.info("Starting data cleaning process...")
        
        # Create a copy to avoid modifying original
        cleaned_df = df.copy()
        
        # Handle missing values
        cleaned_df = self._handle_missing_values(cleaned_df)
        
        # Convert data types
        cleaned_df = self._convert_data_types(cleaned_df)
        
        # Encode categorical variables
        cleaned_df = self._encode_categorical_variables(cleaned_df)
        
        # Create Kenyan-specific features
        cleaned_df = self._create_kenyan_features(cleaned_df)
        
        logger.info(f"Data cleaning completed. Final shape: {cleaned_df.shape}")
        return cleaned_df
    
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        # For numerical columns, fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
        
        return df
    
    def _convert_data_types(self, df):
        """Convert data types appropriately"""
        # Convert potential numeric columns stored as strings
        numeric_columns = ['age', 'loan_amount', 'mpesa_transaction_count', 'income']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _encode_categorical_variables(self, df):
        """Encode categorical variables for Kenyan context"""
        categorical_columns = ['location', 'gender', 'business_type', 'education_level']
        
        for col in categorical_columns:
            if col in df.columns:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
        
        return df
    
    def _create_kenyan_features(self, df):
        """Create features specific to Kenyan financial context"""
        # Create financial behavior score based on M-Pesa activity
        if 'mpesa_transaction_count' in df.columns:
            df['financial_activity_score'] = np.log1p(df['mpesa_transaction_count'])
        
        # Create age groups relevant to credit scoring
        if 'age' in df.columns:
            df['age_group'] = pd.cut(df['age'], 
                                   bins=[18, 25, 35, 45, 55, 65, 100],
                                   labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        
        # Create loan-to-income ratio if both exist
        if 'loan_amount' in df.columns and 'income' in df.columns:
            df['loan_to_income_ratio'] = df['loan_amount'] / (df['income'] + 1)  # +1 to avoid division by zero
        
        return df
    
    def get_data_summary(self, df):
        """Generate comprehensive data summary"""
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'basic_stats': df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
        }
        return summary
