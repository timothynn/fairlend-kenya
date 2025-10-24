import pandas as pd
import numpy as np

def generate_sample_kenyan_credit_data(num_samples=1000):
    """Generate sample Kenyan credit data for demonstration"""
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(20, 65, num_samples),
        'location': np.random.choice(['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Rural'], 
                                   num_samples, p=[0.4, 0.2, 0.1, 0.1, 0.2]),
        'gender': np.random.choice(['Male', 'Female'], num_samples, p=[0.6, 0.4]),
        'business_type': np.random.choice(['Retail', 'Agriculture', 'Services', 'Manufacturing', 'Informal'], 
                                        num_samples, p=[0.3, 0.2, 0.2, 0.1, 0.2]),
        'monthly_income': np.random.normal(50000, 25000, num_samples).clip(10000, 200000),
        'mpesa_transaction_count': np.random.poisson(30, num_samples),
        'sacco_member': np.random.choice([0, 1], num_samples, p=[0.6, 0.4]),
        'existing_loans': np.random.poisson(1, num_samples).clip(0, 5),
        'loan_amount': np.random.uniform(5000, 500000, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Simulate biased approval process (for demonstration)
    approval_probability = (
        0.3 +  # Base probability
        0.1 * (df['location'].isin(['Nairobi', 'Mombasa']).astype(int)) +  # Urban bias
        0.1 * (df['gender'] == 'Male').astype(int) +  # Gender bias
        0.2 * (df['monthly_income'] > 40000).astype(int) +  # Income bias
        0.1 * (df['business_type'] != 'Informal').astype(int)  # Formal sector bias
    ) / 0.8  # Normalize
    
    df['loan_approved'] = np.random.binomial(1, approval_probability.clip(0, 1))
    
    return df

if __name__ == "__main__":
    # Generate and save sample data
    sample_data = generate_sample_kenyan_credit_data(1000)
    sample_data.to_csv('../data/raw/sample_kenyan_credit_data.csv', index=False)
    print("Sample data generated and saved!")
    print(f"Dataset shape: {sample_data.shape}")
    print(f"Approval rate: {sample_data['loan_approved'].mean():.2f}")
