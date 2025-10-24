#!/usr/bin/env python3
"""
Generate sample Kenyan credit data for FairLend Kenya demo
Run this script to create data/sample_data.csv
"""

import pandas as pd
import numpy as np
import os

def generate_sample_kenyan_credit_data(num_samples=1000, seed=42):
    """Generate realistic sample Kenyan credit data with intentional biases"""
    np.random.seed(seed)
    
    # Define Kenyan-specific parameters
    counties = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Malindi', 'Rural']
    business_types = ['Retail', 'Agriculture', 'Services', 'Manufacturing', 'Informal', 'Tech']
    
    data = {
        'applicant_id': [f'APP_{i:05d}' for i in range(1, num_samples + 1)],
        'age': np.random.randint(21, 65, num_samples),
        'location': np.random.choice(
            counties, 
            num_samples, 
            p=[0.35, 0.15, 0.08, 0.08, 0.05, 0.05, 0.04, 0.20]
        ),
        'gender': np.random.choice(['Male', 'Female'], num_samples, p=[0.65, 0.35]),
        'business_type': np.random.choice(
            business_types, 
            num_samples, 
            p=[0.25, 0.20, 0.20, 0.10, 0.20, 0.05]
        ),
        'monthly_income': np.random.lognormal(10.5, 0.8, num_samples).clip(10000, 500000),
        'mpesa_transaction_count': np.random.poisson(35, num_samples).clip(0, 200),
        'mpesa_avg_transaction': np.random.lognormal(8, 1, num_samples).clip(100, 50000),
        'sacco_member': np.random.choice([0, 1], num_samples, p=[0.55, 0.45]),
        'existing_loans': np.random.poisson(0.8, num_samples).clip(0, 5),
        'credit_history_months': np.random.randint(0, 120, num_samples),
        'loan_amount': np.random.lognormal(10.5, 1, num_samples).clip(5000, 1000000),
        'education_level': np.random.choice(
            ['Primary', 'Secondary', 'Certificate', 'Diploma', 'Degree', 'Postgraduate'],
            num_samples,
            p=[0.10, 0.25, 0.15, 0.25, 0.20, 0.05]
        ),
    }
    
    df = pd.DataFrame(data)
    
    # Round financial columns
    df['monthly_income'] = df['monthly_income'].round(0)
    df['mpesa_avg_transaction'] = df['mpesa_avg_transaction'].round(0)
    df['loan_amount'] = df['loan_amount'].round(0)
    
    # Simulate biased approval process (reflecting real-world biases)
    approval_probability = 0.25  # Base probability
    
    # Urban bias
    approval_probability += 0.15 * df['location'].isin(['Nairobi', 'Mombasa', 'Thika']).astype(float)
    
    # Gender bias (favoring males)
    approval_probability += 0.12 * (df['gender'] == 'Male').astype(float)
    
    # Income bias
    approval_probability += 0.20 * (df['monthly_income'] > 50000).astype(float)
    
    # Formal sector bias
    approval_probability += 0.15 * (df['business_type'] != 'Informal').astype(float)
    
    # M-Pesa activity bias
    approval_probability += 0.10 * (df['mpesa_transaction_count'] > 30).astype(float)
    
    # SACCO membership bias
    approval_probability += 0.08 * df['sacco_member'].astype(float)
    
    # Education bias
    education_scores = {
        'Primary': 0.0, 'Secondary': 0.05, 'Certificate': 0.08,
        'Diploma': 0.10, 'Degree': 0.12, 'Postgraduate': 0.15
    }
    approval_probability += df['education_level'].map(education_scores).astype(float)
    
    # Normalize to [0, 1]
    approval_probability = (approval_probability / approval_probability.max()).clip(0, 1)
    
    # Generate approval decisions
    df['loan_approved'] = np.random.binomial(1, approval_probability)
    
    # Add approval amount (0 if not approved, random percentage of requested if approved)
    df['approved_amount'] = df.apply(
        lambda row: row['loan_amount'] * np.random.uniform(0.7, 1.0) if row['loan_approved'] == 1 else 0,
        axis=1
    ).round(0)
    
    return df


def main():
    """Generate and save sample data"""
    # Create data directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/synthetic', exist_ok=True)
    
    # Generate sample data
    print("🔄 Generating sample Kenyan credit data...")
    sample_data = generate_sample_kenyan_credit_data(1000)
    
    # Save to CSV
    output_path = 'data/sample_data.csv'
    sample_data.to_csv(output_path, index=False)
    print(f"✅ Sample data saved to {output_path}")
    
    # Print statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total records: {len(sample_data)}")
    print(f"   Approval rate: {sample_data['loan_approved'].mean():.2%}")
    print(f"\n   Approval by Gender:")
    print(sample_data.groupby('gender')['loan_approved'].agg(['count', 'mean']))
    print(f"\n   Approval by Location:")
    print(sample_data.groupby('location')['loan_approved'].agg(['count', 'mean']).sort_values('mean', ascending=False))
    print(f"\n   Approval by Business Type:")
    print(sample_data.groupby('business_type')['loan_approved'].agg(['count', 'mean']).sort_values('mean', ascending=False))
    
    print(f"\n✨ Data generation complete! Use this data to test FairLend Kenya.")


if __name__ == "__main__":
    main()
