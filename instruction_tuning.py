"""
Instruction Tuning and Fine-tuning Module
Creates training data and fine-tunes the model for better SQL generation
"""
import json
import pandas as pd
from typing import List, Dict
import os

class InstructionTuner:
    """Handles instruction tuning data preparation and model fine-tuning"""
    
    def __init__(self):
        self.training_examples = []
        
    def create_training_examples(self) -> List[Dict]:
        """Create training examples for instruction tuning"""
        examples = [
            {
                "instruction": "How many patients have abnormal blood pressure?",
                "input": "",
                "output": "SELECT COUNT(*) as abnormal_bp_count FROM health_dataset_1 WHERE Blood_Pressure_Abnormality = 1;"
            },
            {
                "instruction": "What is the average age of patients with chronic kidney disease?",
                "input": "",
                "output": "SELECT AVG(Age) as avg_age FROM health_dataset_1 WHERE Chronic_kidney_disease = 1;"
            },
            {
                "instruction": "Show me patients above 60 years with BMI over 30",
                "input": "",
                "output": "SELECT Patient_Number, Age, BMI FROM health_dataset_1 WHERE Age > 60 AND BMI > 30;"
            },
            {
                "instruction": "What is the average physical activity for patients with high stress levels?",
                "input": "",
                "output": "SELECT AVG(h2.Physical_activity) as avg_steps FROM health_dataset_1 h1 JOIN health_dataset_2 h2 ON h1.Patient_Number = h2.Patient_Number WHERE h1.Level_of_Stress = 3;"
            },
            {
                "instruction": "Find patients who smoke and have abnormal blood pressure",
                "input": "",
                "output": "SELECT Patient_Number, Age, BMI, Smoking, Blood_Pressure_Abnormality FROM health_dataset_1 WHERE Smoking = 1 AND Blood_Pressure_Abnormality = 1;"
            },
            {
                "instruction": "What is the distribution of stress levels among female patients?",
                "input": "",
                "output": "SELECT Level_of_Stress, COUNT(*) as count FROM health_dataset_1 WHERE Sex = 1 GROUP BY Level_of_Stress ORDER BY Level_of_Stress;"
            },
            {
                "instruction": "Show me the average hemoglobin level by age group (18-30, 31-50, 51-70, 71+)",
                "input": "",
                "output": "SELECT CASE WHEN Age BETWEEN 18 AND 30 THEN '18-30' WHEN Age BETWEEN 31 AND 50 THEN '31-50' WHEN Age BETWEEN 51 AND 70 THEN '51-70' ELSE '71+' END as age_group, AVG(Level_of_Hemoglobin) as avg_hemoglobin FROM health_dataset_1 GROUP BY age_group;"
            },
            {
                "instruction": "Find patients with high genetic pedigree coefficient (>0.7) and their physical activity",
                "input": "",
                "output": "SELECT h1.Patient_Number, h1.Genetic_Pedigree_Coefficient, AVG(h2.Physical_activity) as avg_physical_activity FROM health_dataset_1 h1 JOIN health_dataset_2 h2 ON h1.Patient_Number = h2.Patient_Number WHERE h1.Genetic_Pedigree_Coefficient > 0.7 GROUP BY h1.Patient_Number, h1.Genetic_Pedigree_Coefficient;"
            },
            {
                "instruction": "What is the correlation between salt intake and blood pressure abnormality?",
                "input": "",
                "output": "SELECT Blood_Pressure_Abnormality, AVG(salt_content_in_the_diet) as avg_salt_intake, COUNT(*) as count FROM health_dataset_1 GROUP BY Blood_Pressure_Abnormality;"
            },
            {
                "instruction": "Show me patients with both chronic kidney disease and adrenal/thyroid disorders",
                "input": "",
                "output": "SELECT Patient_Number, Age, Chronic_kidney_disease, Adrenal_and_thyroid_disorders FROM health_dataset_1 WHERE Chronic_kidney_disease = 1 AND Adrenal_and_thyroid_disorders = 1;"
            },
            {
                "instruction": "What is the average daily physical activity for each patient?",
                "input": "",
                "output": "SELECT Patient_Number, AVG(Physical_activity) as avg_daily_steps, COUNT(*) as days_recorded FROM health_dataset_2 GROUP BY Patient_Number;"
            },
            {
                "instruction": "Find patients with low hemoglobin (<12) and high stress levels",
                "input": "",
                "output": "SELECT Patient_Number, Level_of_Hemoglobin, Level_of_Stress FROM health_dataset_1 WHERE Level_of_Hemoglobin < 12 AND Level_of_Stress = 3;"
            },
            {
                "instruction": "What is the relationship between BMI and physical activity?",
                "input": "",
                "output": "SELECT h1.BMI, AVG(h2.Physical_activity) as avg_physical_activity FROM health_dataset_1 h1 JOIN health_dataset_2 h2 ON h1.Patient_Number = h2.Patient_Number GROUP BY h1.BMI ORDER BY h1.BMI;"
            },
            {
                "instruction": "Show me pregnant patients and their health metrics",
                "input": "",
                "output": "SELECT Patient_Number, Age, BMI, Level_of_Hemoglobin, Blood_Pressure_Abnormality FROM health_dataset_1 WHERE Pregnancy = 1;"
            },
            {
                "instruction": "What is the average alcohol consumption for patients with abnormal blood pressure?",
                "input": "",
                "output": "SELECT AVG(alcohol_consumption_per_day) as avg_alcohol_consumption FROM health_dataset_1 WHERE Blood_Pressure_Abnormality = 1;"
            }
        ]
        
        return examples
    
    def save_training_data(self, output_file: str = "training_data.jsonl"):
        """Save training data in JSONL format for fine-tuning"""
        examples = self.create_training_examples()
        os.makedirs("training_data", exist_ok=True)
        
        with open(f"training_data/{output_file}", "w") as f:
            for example in examples:
                # Format for OpenAI fine-tuning
                formatted = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert SQL query generator for healthcare data analysis."
                        },
                        {
                            "role": "user",
                            "content": f"Generate a SQL query for: {example['instruction']}"
                        },
                        {
                            "role": "assistant",
                            "content": example['output']
                        }
                    ]
                }
                f.write(json.dumps(formatted) + "\n")
        
        print(f"✓ Training data saved to training_data/{output_file}")
        print(f"  Total examples: {len(examples)}")
        
        return examples
    
    def create_prompt_template(self) -> str:
        """Create prompt template for instruction tuning"""
        template = """You are an expert SQL query generator for healthcare data analysis.

Given a natural language question about healthcare data, generate the appropriate SQL query.

Database Schema:
{schema}

Examples:
{examples}

Question: {question}
SQL Query:"""
        return template
    
    def generate_fine_tuning_script(self):
        """Generate script for fine-tuning OpenAI models"""
        script = """#!/bin/bash
# Fine-tuning script for OpenAI models
# Requires: OpenAI CLI and API key

# Set your API key
export OPENAI_API_KEY="your_api_key_here"

# Upload training data
openai api fine_tunes.create \\
    -t training_data/training_data.jsonl \\
    -m gpt-3.5-turbo \\
    --suffix "healthcare-sql" \\
    --n_epochs 3

# Check status
openai api fine_tunes.list

# Use the fine-tuned model
# Update MODEL_NAME in config.py to use the fine-tuned model
"""
        os.makedirs("scripts", exist_ok=True)
        with open("scripts/fine_tune.sh", "w") as f:
            f.write(script)
        os.chmod("scripts/fine_tune.sh", 0o755)
        print("✓ Fine-tuning script created at scripts/fine_tune.sh")

if __name__ == "__main__":
    tuner = InstructionTuner()
    examples = tuner.save_training_data()
    tuner.generate_fine_tuning_script()
    print(f"\n✓ Created {len(examples)} training examples")

