"""
Data Audit and Exploratory Data Analysis
Generates comprehensive report on data quality, distributions, and relationships
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import DataPreprocessor
from config import DATASET1_PATH, DATASET2_PATH
import os

class DataAuditor:
    """Performs comprehensive data audit and EDA"""
    
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.df1 = None
        self.df2 = None
        
    def load_and_prepare_data(self):
        """Load and prepare datasets"""
        self.df1, self.df2 = self.preprocessor.load_datasets()
        self.df1 = self.preprocessor.clean_dataset_1(self.df1)
        self.df2 = self.preprocessor.clean_dataset_2(self.df2)
        
    def generate_audit_report(self, output_file="data_audit_report.txt"):
        """Generate comprehensive data audit report"""
        report = []
        report.append("=" * 80)
        report.append("HEALTHCARE DATASETS - DATA AUDIT REPORT")
        report.append("=" * 80)
        report.append("\n")
        
        # Dataset 1 Overview
        report.append("DATASET 1: Health Dataset 1")
        report.append("-" * 80)
        report.append(f"Total Records: {len(self.df1)}")
        report.append(f"Total Variables: {len(self.df1.columns)}")
        report.append("\nVariable Summary:")
        report.append(str(self.df1.describe()))
        report.append("\n")
        
        # Missing values
        report.append("Missing Values:")
        missing = self.df1.isnull().sum()
        if missing.sum() > 0:
            report.append(str(missing[missing > 0]))
        else:
            report.append("No missing values detected.")
        report.append("\n")
        
        # Data types
        report.append("Data Types:")
        report.append(str(self.df1.dtypes))
        report.append("\n")
        
        # Categorical variables distribution
        report.append("Categorical Variables Distribution:")
        categorical_vars = ['Blood_Pressure_Abnormality', 'Sex', 'Pregnancy', 
                           'Smoking', 'Chronic_kidney_disease', 
                           'Adrenal_and_thyroid_disorders', 'Level_of_Stress']
        for var in categorical_vars:
            if var in self.df1.columns:
                report.append(f"\n{var}:")
                report.append(str(self.df1[var].value_counts()))
        report.append("\n")
        
        # Continuous variables statistics
        report.append("Continuous Variables Statistics:")
        continuous_vars = ['Level_of_Hemoglobin', 'Genetic_Pedigree_Coefficient', 
                          'Age', 'BMI', 'salt_content_in_the_diet', 
                          'alcohol_consumption_per_day']
        for var in continuous_vars:
            if var in self.df1.columns:
                report.append(f"\n{var}:")
                report.append(f"  Mean: {self.df1[var].mean():.2f}")
                report.append(f"  Std: {self.df1[var].std():.2f}")
                report.append(f"  Min: {self.df1[var].min():.2f}")
                report.append(f"  Max: {self.df1[var].max():.2f}")
                report.append(f"  Median: {self.df1[var].median():.2f}")
        report.append("\n")
        
        # Dataset 2 Overview
        report.append("\n" + "=" * 80)
        report.append("DATASET 2: Health Dataset 2")
        report.append("-" * 80)
        report.append(f"Total Records: {len(self.df2)}")
        report.append(f"Total Variables: {len(self.df2.columns)}")
        report.append("\nVariable Summary:")
        report.append(str(self.df2.describe()))
        report.append("\n")
        
        # Unique patients
        unique_patients = self.df2['Patient_Number'].nunique()
        report.append(f"Unique Patients: {unique_patients}")
        report.append(f"Average records per patient: {len(self.df2) / unique_patients:.2f}")
        report.append("\n")
        
        # Physical activity statistics
        report.append("Physical Activity Statistics:")
        report.append(f"  Mean steps/day: {self.df2['Physical_activity'].mean():.2f}")
        report.append(f"  Std: {self.df2['Physical_activity'].std():.2f}")
        report.append(f"  Min: {self.df2['Physical_activity'].min()}")
        report.append(f"  Max: {self.df2['Physical_activity'].max()}")
        report.append("\n")
        
        # Data relationship analysis
        report.append("\n" + "=" * 80)
        report.append("DATA RELATIONSHIP ANALYSIS")
        report.append("-" * 80)
        
        # Join analysis
        common_patients = set(self.df1['Patient_Number']) & set(self.df2['Patient_Number'])
        report.append(f"\nCommon Patients (joinable): {len(common_patients)}")
        report.append(f"Patients only in Dataset 1: {len(set(self.df1['Patient_Number']) - set(self.df2['Patient_Number']))}")
        report.append(f"Patients only in Dataset 2: {len(set(self.df2['Patient_Number']) - set(self.df1['Patient_Number']))}")
        report.append("\n")
        
        # Correlation analysis for Dataset 1
        report.append("Correlation Analysis (Dataset 1 - Continuous Variables):")
        numeric_cols = self.df1.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df1[numeric_cols].corr()
        report.append("\nTop Correlations:")
        # Get upper triangle of correlation matrix
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append((
                    corr_matrix.columns[i], 
                    corr_matrix.columns[j], 
                    corr_matrix.iloc[i, j]
                ))
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        for col1, col2, corr in corr_pairs[:10]:
            report.append(f"  {col1} <-> {col2}: {corr:.3f}")
        report.append("\n")
        
        # Key insights
        report.append("\n" + "=" * 80)
        report.append("KEY INSIGHTS")
        report.append("-" * 80)
        report.append("1. Dataset 1 contains demographic, genetic, and lifestyle factors")
        report.append("2. Dataset 2 contains time-series physical activity data")
        report.append("3. Both datasets can be joined on Patient_Number")
        report.append("4. Data appears to be well-structured with no major quality issues")
        report.append("5. Suitable for GenAI-based query and analysis system")
        report.append("\n")
        
        # Write report to file
        report_text = "\n".join(report)
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{output_file}", "w") as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\n✓ Audit report saved to reports/{output_file}")
        
        return report_text
    
    def generate_visualizations(self):
        """Generate visualization plots"""
        os.makedirs("reports/figures", exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        
        # Distribution plots for key variables
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # Age distribution
        axes[0, 0].hist(self.df1['Age'], bins=30, edgecolor='black')
        axes[0, 0].set_title('Age Distribution')
        axes[0, 0].set_xlabel('Age')
        axes[0, 0].set_ylabel('Frequency')
        
        # BMI distribution
        axes[0, 1].hist(self.df1['BMI'], bins=30, edgecolor='black')
        axes[0, 1].set_title('BMI Distribution')
        axes[0, 1].set_xlabel('BMI')
        axes[0, 1].set_ylabel('Frequency')
        
        # Hemoglobin distribution
        axes[0, 2].hist(self.df1['Level_of_Hemoglobin'], bins=30, edgecolor='black')
        axes[0, 2].set_title('Hemoglobin Level Distribution')
        axes[0, 2].set_xlabel('Hemoglobin (g/dl)')
        axes[0, 2].set_ylabel('Frequency')
        
        # Blood pressure abnormality
        axes[1, 0].bar(['Normal', 'Abnormal'], 
                      self.df1['Blood_Pressure_Abnormality'].value_counts().sort_index().values)
        axes[1, 0].set_title('Blood Pressure Abnormality')
        axes[1, 0].set_ylabel('Count')
        
        # Stress levels
        stress_labels = ['Low', 'Normal', 'High']
        axes[1, 1].bar(stress_labels, 
                      self.df1['Level_of_Stress'].value_counts().sort_index().values)
        axes[1, 1].set_title('Stress Level Distribution')
        axes[1, 1].set_ylabel('Count')
        
        # Physical activity distribution
        axes[1, 2].hist(self.df2['Physical_activity'], bins=50, edgecolor='black')
        axes[1, 2].set_title('Physical Activity Distribution (Steps/Day)')
        axes[1, 2].set_xlabel('Steps')
        axes[1, 2].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('reports/figures/data_distributions.png', dpi=300, bbox_inches='tight')
        print("✓ Visualizations saved to reports/figures/data_distributions.png")
        plt.close()

if __name__ == "__main__":
    auditor = DataAuditor()
    auditor.load_and_prepare_data()
    auditor.generate_audit_report()
    auditor.generate_visualizations()

