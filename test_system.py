"""
Test script to verify the system is working correctly
"""
import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import pandas as pd
        import numpy as np
        from data_preprocessing import DataPreprocessor
        from config import DATASET1_PATH, DATASET2_PATH
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_files():
    """Test if data files exist"""
    print("\nTesting data files...")
    from config import DATASET1_PATH, DATASET2_PATH
    
    files_exist = True
    if not os.path.exists(DATASET1_PATH):
        print(f"✗ {DATASET1_PATH} not found. Run: python data_generator.py")
        files_exist = False
    else:
        print(f"✓ {DATASET1_PATH} exists")
    
    if not os.path.exists(DATASET2_PATH):
        print(f"✗ {DATASET2_PATH} not found. Run: python data_generator.py")
        files_exist = False
    else:
        print(f"✓ {DATASET2_PATH} exists")
    
    return files_exist

def test_database():
    """Test if database exists and is accessible"""
    print("\nTesting database...")
    from config import DATABASE_PATH
    
    if not os.path.exists(DATABASE_PATH):
        print(f"✗ {DATABASE_PATH} not found. Run: python data_preprocessing.py")
        return False
    
    try:
        from data_preprocessing import DataPreprocessor
        preprocessor = DataPreprocessor()
        schema = preprocessor.get_schema_info()
        print(f"✓ Database exists and is accessible")
        print(f"  Tables: {list(schema.keys())}")
        preprocessor.close()
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    from config import OPENAI_API_KEY, MODEL_NAME
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("⚠ Warning: OPENAI_API_KEY not set in .env file")
        print("  The system will work but GenAI features won't function")
        return False
    else:
        print(f"✓ OPENAI_API_KEY configured")
        print(f"✓ Model: {MODEL_NAME}")
        return True

def test_genai_pipeline():
    """Test GenAI pipeline (requires API key)"""
    print("\nTesting GenAI pipeline...")
    try:
        from genai_pipeline import HealthcareGenAI
        pipeline = HealthcareGenAI()
        print("✓ GenAI pipeline initialized")
        pipeline.close()
        return True
    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):
            print("⚠ GenAI pipeline requires OPENAI_API_KEY")
            return False
        else:
            print(f"✗ Error: {e}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Healthcare GenAI Analytics - System Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Database", test_database()))
    results.append(("Configuration", test_config()))
    
    # Only test GenAI if config is OK
    if results[-1][1]:
        results.append(("GenAI Pipeline", test_genai_pipeline()))
    else:
        results.append(("GenAI Pipeline", False))
        print("\n⚠ Skipping GenAI pipeline test (API key not configured)")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Or: python run_pipeline.py --interactive")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        print("\nSetup commands:")
        print("  1. python data_generator.py")
        print("  2. python data_preprocessing.py")
        print("  3. Edit .env file with your OPENAI_API_KEY")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

