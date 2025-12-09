"""
Script to explore the Excel dataset structure
"""
import pandas as pd
import openpyxl

excel_file = "lu1828272yg3dhb.xlsm"

print("=" * 80)
print("Exploring Excel Dataset")
print("=" * 80)

try:
    # Read Excel file
    excel_file_obj = pd.ExcelFile(excel_file, engine='openpyxl')
    
    print(f"\nFile: {excel_file}")
    print(f"Sheet names: {excel_file_obj.sheet_names}")
    print(f"Number of sheets: {len(excel_file_obj.sheet_names)}")
    
    # Explore each sheet
    for sheet_name in excel_file_obj.sheet_names:
        print("\n" + "-" * 80)
        print(f"Sheet: {sheet_name}")
        print("-" * 80)
        
        df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
        
        print(f"Shape: {df.shape} (rows, columns)")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())
        print(f"\nData types:")
        print(df.dtypes)
        print(f"\nMissing values:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("No missing values")
        print(f"\nBasic statistics:")
        print(df.describe())
        
except Exception as e:
    print(f"Error reading Excel file: {e}")
    print("\nTrying with different engine...")
    try:
        excel_file_obj = pd.ExcelFile(excel_file, engine='xlrd')
        print(f"Sheet names: {excel_file_obj.sheet_names}")
    except Exception as e2:
        print(f"Error with xlrd: {e2}")

