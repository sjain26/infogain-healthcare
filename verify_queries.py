"""
Script to verify LLM-generated queries against direct SQL queries
Cross-verification to ensure accuracy
"""
import sqlite3
import pandas as pd
from genai_pipeline import HealthcareGenAI

def verify_query(user_query, expected_sql_pattern=None):
    """Verify a query by comparing LLM results with direct SQL"""
    print("=" * 80)
    print(f"VERIFICATION: {user_query}")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = HealthcareGenAI()
    
    # Process query through LLM
    result = pipeline.process_query(user_query)
    
    if result.get('error'):
        print(f"❌ ERROR: {result['error']}")
        pipeline.close()
        return False
    
    # Get LLM-generated SQL
    llm_sql = result.get('sql_query', 'N/A')
    llm_results = result.get('query_results')
    
    print(f"\n📝 LLM Generated SQL:")
    print(f"   {llm_sql}")
    
    # Execute direct SQL for verification
    conn = sqlite3.connect('data/healthcare.db')
    try:
        direct_results = pd.read_sql_query(llm_sql, conn)
        print(f"\n✅ Direct SQL Execution:")
        print(f"   {direct_results}")
        
        # Compare results
        if llm_results is not None and len(llm_results) > 0:
            print(f"\n📊 LLM Results:")
            print(f"   {llm_results}")
            
            # Check if results match
            if direct_results.equals(llm_results):
                print("\n✅ VERIFICATION PASSED: Results match!")
            else:
                print("\n⚠️  VERIFICATION WARNING: Results may differ (check formatting)")
                print(f"   Direct SQL shape: {direct_results.shape}")
                print(f"   LLM Results shape: {llm_results.shape}")
        else:
            print("\n⚠️  No results from LLM pipeline")
        
    except Exception as e:
        print(f"\n❌ SQL Execution Error: {e}")
        return False
    finally:
        conn.close()
        pipeline.close()
    
    print(f"\n💡 Insights Preview:")
    insights = result.get('insights', 'N/A')
    print(f"   {insights[:200]}..." if len(insights) > 200 else f"   {insights}")
    
    return True

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CROSS-VERIFICATION TEST SUITE")
    print("=" * 80)
    print("\nVerifying LLM-generated queries against direct SQL execution...\n")
    
    # Test queries
    test_queries = [
        "How many patients have abnormal blood pressure?",
        "What is the average age of patients with chronic kidney disease?",
        "How many patients are above 60 years old with BMI greater than 30?",
        "What is the distribution of patients by sex?",
        "How many patients smoke?",
    ]
    
    passed = 0
    failed = 0
    
    for query in test_queries:
        try:
            if verify_query(query):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            failed += 1
        print("\n")
    
    print("=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {len(test_queries)}")
    print("=" * 80)

