"""
Data preprocessing and integration module
Handles data cleaning, validation, and on-the-fly joining
"""
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
from config import (
    DATABASE_PATH, DATASET1_PATH, DATASET2_PATH, EXCEL_FILE_PATH, RANDOM_SEED,
    SQL_DB_TYPE, SQL_HOST, SQL_PORT, SQL_USER, SQL_PASSWORD, SQL_DATABASE,
    SQL_TABLE_1, SQL_TABLE_2
)
import os

class DataPreprocessor:
    """Handles data preprocessing and database setup"""
    
    def __init__(self):
        self.engine = None
        self.conn = None
        
    def _get_sql_connection_string(self):
        """Generate SQL connection string based on database type"""
        if SQL_DB_TYPE.lower() == "mysql":
            return f"mysql+pymysql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}"
        elif SQL_DB_TYPE.lower() == "postgresql" or SQL_DB_TYPE.lower() == "postgres":
            return f"postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}"
        elif SQL_DB_TYPE.lower() == "sqlserver" or SQL_DB_TYPE.lower() == "mssql":
            return f"mssql+pyodbc://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
        elif SQL_DB_TYPE.lower() == "sqlite":
            return f"sqlite:///{SQL_DATABASE}"
        else:
            raise ValueError(f"Unsupported database type: {SQL_DB_TYPE}")
    
    def load_datasets(self):
        """Load datasets from SQL database, Excel file, or CSV files (in priority order)"""
        # Priority 1: Try to load from SQL database
        if SQL_HOST and SQL_DATABASE and SQL_TABLE_1:
            try:
                print(f"Attempting to load from SQL database: {SQL_DB_TYPE}://{SQL_HOST}/{SQL_DATABASE}")
                connection_string = self._get_sql_connection_string()
                sql_engine = create_engine(connection_string)
                
                # Load Dataset 1
                query1 = f"SELECT * FROM {SQL_TABLE_1}"
                df1 = pd.read_sql(query1, sql_engine)
                print(f"✓ Loaded Dataset 1 from SQL table '{SQL_TABLE_1}': {len(df1)} records")
                
                # Load Dataset 2 if table exists
                df2 = None
                if SQL_TABLE_2:
                    try:
                        query2 = f"SELECT * FROM {SQL_TABLE_2}"
                        df2 = pd.read_sql(query2, sql_engine)
                        print(f"✓ Loaded Dataset 2 from SQL table '{SQL_TABLE_2}': {len(df2)} records")
                    except Exception as e:
                        print(f"⚠ Dataset 2 table '{SQL_TABLE_2}' not found or error: {e}")
                        df2 = pd.DataFrame(columns=['Patient_Number', 'Day_Number', 'Physical_activity'])
                
                sql_engine.dispose()
                return df1, df2 if df2 is not None else pd.DataFrame(columns=['Patient_Number', 'Day_Number', 'Physical_activity'])
            except Exception as e:
                print(f"⚠ Error loading from SQL database: {e}")
                print("Falling back to file-based loading...")
        
        # Priority 2: Try to load from Excel file
        if os.path.exists(EXCEL_FILE_PATH):
            try:
                # Read Excel file
                excel_file = pd.ExcelFile(EXCEL_FILE_PATH, engine='openpyxl')
                print(f"Loading from Excel file: {EXCEL_FILE_PATH}")
                
                # Load Dataset 1 from first sheet
                df1 = pd.read_excel(EXCEL_FILE_PATH, sheet_name='Health Dataset 1 (N=2000)', engine='openpyxl')
                print(f"✓ Loaded Dataset 1: {len(df1)} records")
                
                # Try to find Dataset 2 in another sheet
                df2 = None
                for sheet_name in excel_file.sheet_names:
                    if 'Dataset 2' in sheet_name or 'Physical' in sheet_name or 'activity' in sheet_name.lower():
                        df2 = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name, engine='openpyxl')
                        print(f"✓ Loaded Dataset 2 from sheet '{sheet_name}': {len(df2)} records")
                        break
                
                # If Dataset 2 not found, try CSV or generate
                if df2 is None:
                    if os.path.exists(DATASET2_PATH):
                        df2 = pd.read_csv(DATASET2_PATH)
                        print(f"✓ Loaded Dataset 2 from CSV: {len(df2)} records")
                    else:
                        print("⚠ Dataset 2 not found. Creating empty dataset (will be skipped in joins).")
                        df2 = pd.DataFrame(columns=['Patient_Number', 'Day_Number', 'Physical_activity'])
                
                return df1, df2
            except Exception as e:
                print(f"Error loading from Excel: {e}")
                print("Falling back to CSV files...")
        
        # Priority 3: Fallback to CSV files
        try:
            if os.path.exists(DATASET1_PATH):
                df1 = pd.read_csv(DATASET1_PATH)
                if os.path.exists(DATASET2_PATH):
                    df2 = pd.read_csv(DATASET2_PATH)
                else:
                    df2 = pd.DataFrame(columns=['Patient_Number', 'Day_Number', 'Physical_activity'])
                return df1, df2
            else:
                raise FileNotFoundError("No data source found. Please configure SQL connection or provide data files.")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Dataset file not found: {e}. Please configure SQL connection in .env file or provide data files.")
    
    def clean_dataset_1(self, df):
        """Clean and validate Health Dataset 1"""
        df_clean = df.copy()
        
        # Ensure Patient_Number is string
        df_clean['Patient_Number'] = df_clean['Patient_Number'].astype(str)
        
        # Handle missing values
        # Fill missing Genetic_Pedigree_Coefficient with median or 0
        if 'Genetic_Pedigree_Coefficient' in df_clean.columns:
            df_clean['Genetic_Pedigree_Coefficient'] = df_clean['Genetic_Pedigree_Coefficient'].fillna(
                df_clean['Genetic_Pedigree_Coefficient'].median() if df_clean['Genetic_Pedigree_Coefficient'].notna().sum() > 0 else 0
            )
        
        # Fill missing Pregnancy with 0 (default to not pregnant)
        if 'Pregnancy' in df_clean.columns:
            df_clean['Pregnancy'] = df_clean['Pregnancy'].fillna(0)
        
        # Fill missing alcohol_consumption with 0
        if 'alcohol_consumption_per_day' in df_clean.columns:
            df_clean['alcohol_consumption_per_day'] = df_clean['alcohol_consumption_per_day'].fillna(0)
        
        # Validate binary columns
        binary_cols = ['Blood_Pressure_Abnormality', 'Sex', 'Pregnancy', 
                      'Smoking', 'Chronic_kidney_disease', 'Adrenal_and_thyroid_disorders']
        for col in binary_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0).clip(0, 1).astype(int)
        
        # Validate continuous variables
        if 'Level_of_Hemoglobin' in df_clean.columns:
            df_clean['Level_of_Hemoglobin'] = pd.to_numeric(df_clean['Level_of_Hemoglobin'], errors='coerce').clip(8, 20)
        if 'Genetic_Pedigree_Coefficient' in df_clean.columns:
            df_clean['Genetic_Pedigree_Coefficient'] = pd.to_numeric(df_clean['Genetic_Pedigree_Coefficient'], errors='coerce').clip(0, 1)
        if 'Age' in df_clean.columns:
            df_clean['Age'] = pd.to_numeric(df_clean['Age'], errors='coerce').fillna(50).clip(18, 100).astype(int)
        if 'BMI' in df_clean.columns:
            df_clean['BMI'] = pd.to_numeric(df_clean['BMI'], errors='coerce').clip(15, 50)
        if 'salt_content_in_the_diet' in df_clean.columns:
            df_clean['salt_content_in_the_diet'] = pd.to_numeric(df_clean['salt_content_in_the_diet'], errors='coerce').clip(0, 10000)
        if 'alcohol_consumption_per_day' in df_clean.columns:
            df_clean['alcohol_consumption_per_day'] = pd.to_numeric(df_clean['alcohol_consumption_per_day'], errors='coerce').clip(0, 500)
        
        # Validate ordinal variable
        if 'Level_of_Stress' in df_clean.columns:
            df_clean['Level_of_Stress'] = pd.to_numeric(df_clean['Level_of_Stress'], errors='coerce').fillna(2).clip(1, 3).astype(int)
        
        # Logical validation: Pregnancy only for females
        if 'Sex' in df_clean.columns and 'Pregnancy' in df_clean.columns:
            df_clean.loc[df_clean['Sex'] == 0, 'Pregnancy'] = 0
        
        return df_clean
    
    def clean_dataset_2(self, df):
        """Clean and validate Health Dataset 2"""
        df_clean = df.copy()
        
        # Ensure Patient_Number is string
        df_clean['Patient_Number'] = df_clean['Patient_Number'].astype(str)
        
        # Validate Day_Number
        df_clean['Day_Number'] = df_clean['Day_Number'].clip(1, 10).astype(int)
        
        # Validate Physical_activity (steps should be non-negative)
        df_clean['Physical_activity'] = df_clean['Physical_activity'].clip(0, 50000).astype(int)
        
        return df_clean
    
    def setup_database(self, df1, df2):
        """Create SQLite database and load datasets as separate tables"""
        # Create database engine
        self.engine = create_engine(f'sqlite:///{DATABASE_PATH}')
        self.conn = sqlite3.connect(DATABASE_PATH)
        
        # Clean datasets
        df1_clean = self.clean_dataset_1(df1)
        df2_clean = self.clean_dataset_2(df2)
        
        # Load to database as separate tables
        df1_clean.to_sql('health_dataset_1', self.engine, if_exists='replace', index=False)
        df2_clean.to_sql('health_dataset_2', self.engine, if_exists='replace', index=False)
        
        # Create indexes for faster joins
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_patient_1 ON health_dataset_1(Patient_Number)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_patient_2 ON health_dataset_2(Patient_Number)")
        
        self.conn.commit()
        print(f"✓ Database created at {DATABASE_PATH}")
        print(f"  - health_dataset_1: {len(df1_clean)} records")
        print(f"  - health_dataset_2: {len(df2_clean)} records")
        
        return df1_clean, df2_clean
    
    def get_schema_info(self):
        """Get schema information for both tables"""
        if not self.conn:
            self.conn = sqlite3.connect(DATABASE_PATH)
        
        schema_info = {}
        
        # Get schema for table 1
        cursor = self.conn.execute("PRAGMA table_info(health_dataset_1)")
        schema_info['health_dataset_1'] = [row[1] for row in cursor.fetchall()]
        
        # Get schema for table 2
        cursor = self.conn.execute("PRAGMA table_info(health_dataset_2)")
        schema_info['health_dataset_2'] = [row[1] for row in cursor.fetchall()]
        
        return schema_info
    
    def execute_query(self, query):
        """Execute SQL query and return results"""
        if not self.conn:
            self.conn = sqlite3.connect(DATABASE_PATH)
        
        try:
            result = pd.read_sql_query(query, self.conn)
            return result
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    df1, df2 = preprocessor.load_datasets()
    preprocessor.setup_database(df1, df2)
    schema = preprocessor.get_schema_info()
    print("\nSchema Information:")
    print(f"Dataset 1 columns: {schema['health_dataset_1']}")
    print(f"Dataset 2 columns: {schema['health_dataset_2']}")

