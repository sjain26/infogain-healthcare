"""
Script to generate sample healthcare datasets based on the specifications
"""
import pandas as pd
import numpy as np
from config import RANDOM_SEED

np.random.seed(RANDOM_SEED)

def generate_dataset_1(n=2000):
    """
    Generate Health Dataset 1 with N=2000 records
    """
    data = {
        'Patient_Number': [f'P{i+1:05d}' for i in range(n)],
        'Blood_Pressure_Abnormality': np.random.choice([0, 1], n, p=[0.7, 0.3]),
        'Level_of_Hemoglobin': np.random.normal(14.5, 2.5, n).clip(8, 20),
        'Genetic_Pedigree_Coefficient': np.random.beta(2, 5, n),  # Skewed towards lower values
        'Age': np.random.randint(18, 85, n),
        'BMI': np.random.normal(25, 5, n).clip(15, 45),
        'Sex': np.random.choice([0, 1], n, p=[0.5, 0.5]),
        'Pregnancy': np.random.choice([0, 1], n, p=[0.85, 0.15]),
        'Smoking': np.random.choice([0, 1], n, p=[0.75, 0.25]),
        'salt_content_in_the_diet': np.random.normal(3500, 1000, n).clip(1000, 8000),
        'alcohol_consumption_per_day': np.random.exponential(20, n).clip(0, 200),
        'Level_of_Stress': np.random.choice([1, 2, 3], n, p=[0.3, 0.5, 0.2]),
        'Chronic_kidney_disease': np.random.choice([0, 1], n, p=[0.9, 0.1]),
        'Adrenal_and_thyroid_disorders': np.random.choice([0, 1], n, p=[0.85, 0.15])
    }
    
    # Add some correlations for realism
    df = pd.DataFrame(data)
    
    # Higher age and BMI correlate with blood pressure issues
    df.loc[df['Age'] > 60, 'Blood_Pressure_Abnormality'] = np.random.choice(
        [0, 1], sum(df['Age'] > 60), p=[0.5, 0.5]
    )
    
    # Smoking correlates with higher stress
    df.loc[df['Smoking'] == 1, 'Level_of_Stress'] = np.random.choice(
        [1, 2, 3], sum(df['Smoking'] == 1), p=[0.1, 0.3, 0.6]
    )
    
    # Pregnancy only for females
    df.loc[df['Sex'] == 0, 'Pregnancy'] = 0
    
    return df

def generate_dataset_2(n=20000):
    """
    Generate Health Dataset 2 with N=20,000 records
    Contains physical activity data for last 10 days per patient
    """
    # Assuming we have 2000 unique patients from dataset 1
    unique_patients = [f'P{i+1:05d}' for i in range(2000)]
    
    # Each patient has 10 days of data
    patient_numbers = []
    day_numbers = []
    physical_activities = []
    
    for patient in unique_patients:
        # Generate 10 days of step data per patient
        base_steps = np.random.normal(8000, 2000)  # Patient's average daily steps
        for day in range(1, 11):
            patient_numbers.append(patient)
            day_numbers.append(day)
            # Daily variation around base steps
            daily_steps = max(0, int(np.random.normal(base_steps, 1500)))
            physical_activities.append(daily_steps)
    
    # Add extra records to reach 20,000 if needed
    remaining = n - len(patient_numbers)
    if remaining > 0:
        for _ in range(remaining):
            patient = np.random.choice(unique_patients)
            day = np.random.randint(1, 11)
            base_steps = np.random.normal(8000, 2000)
            daily_steps = max(0, int(np.random.normal(base_steps, 1500)))
            
            patient_numbers.append(patient)
            day_numbers.append(day)
            physical_activities.append(daily_steps)
    
    data = {
        'Patient_Number': patient_numbers[:n],
        'Day_Number': day_numbers[:n],
        'Physical_activity': physical_activities[:n]
    }
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Generate datasets
    print("Generating Health Dataset 1 (N=2000)...")
    df1 = generate_dataset_1(2000)
    df1.to_csv("data/health_dataset_1.csv", index=False)
    print(f"✓ Generated {len(df1)} records")
    
    print("\nGenerating Health Dataset 2 (N=20,000)...")
    df2 = generate_dataset_2(20000)
    df2.to_csv("data/health_dataset_2.csv", index=False)
    print(f"✓ Generated {len(df2)} records")
    
    print("\n✓ Datasets generated successfully!")

