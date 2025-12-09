"""
Configuration file for the Healthcare GenAI Analytics System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Model Configuration
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "groq")  # Options: openai, groq
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")
TEMPERATURE = 0.3  # Lower temperature for more consistent SQL generation
MAX_TOKENS = 1024

# Database Configuration
DATABASE_PATH = "data/healthcare.db"  # Local SQLite for query execution

# SQL Database Configuration (for loading actual datasets)
SQL_DB_TYPE = os.getenv("SQL_DB_TYPE", "mysql")  # Options: mysql, postgresql, sqlserver, sqlite
SQL_HOST = os.getenv("SQL_HOST", "localhost")
SQL_PORT = os.getenv("SQL_PORT", "3306")
SQL_USER = os.getenv("SQL_USER", "root")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "")
SQL_DATABASE = os.getenv("SQL_DATABASE", "healthcare")
SQL_TABLE_1 = os.getenv("SQL_TABLE_1", "health_dataset_1")  # Table name for Dataset 1
SQL_TABLE_2 = os.getenv("SQL_TABLE_2", "health_dataset_2")  # Table name for Dataset 2

# Fallback paths (for sample data)
EXCEL_FILE_PATH = "lu1828272yg3dhb.xlsm"
DATASET1_PATH = "data/health_dataset_1.csv"
DATASET2_PATH = "data/health_dataset_2.csv"

# Data Processing
RANDOM_SEED = 42

# Evaluation Metrics
EVALUATION_METRICS = {
    "sql_accuracy": True,
    "response_relevance": True,
    "response_coherence": True,
    "response_safety": True
}

# Ethical Considerations
ENABLE_SAFETY_CHECKS = True
PRIVACY_MODE = True  # Don't log user queries with sensitive data

