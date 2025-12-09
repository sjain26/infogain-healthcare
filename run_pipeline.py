"""
Main script to run the pipeline
"""
import argparse
from genai_pipeline import HealthcareGenAI

def main():
    parser = argparse.ArgumentParser(description='Healthcare GenAI Analytics Pipeline')
    parser.add_argument('--query', type=str, help='Single query to process')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    print("Initializing GenAI pipeline...")
    pipeline = HealthcareGenAI()
    
    if args.query:
        # Process single query
        print(f"\nProcessing query: {args.query}")
        result = pipeline.process_query(args.query)
        
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        print(f"\nSQL Query:\n{result.get('sql_query', 'N/A')}")
        print(f"\nQuery Results:\n{result.get('query_results', 'N/A')}")
        print(f"\nInsights:\n{result.get('insights', 'N/A')}")
        if result.get('error'):
            print(f"\nError: {result['error']}")
    
    elif args.interactive:
        # Interactive mode
        print("\n" + "="*80)
        print("Healthcare GenAI Analytics - Interactive Mode")
        print("="*80)
        print("Enter your queries (type 'exit' to quit)\n")
        
        while True:
            query = input("\nQuery: ").strip()
            if query.lower() in ['exit', 'quit', 'q']:
                break
            
            if not query:
                continue
            
            result = pipeline.process_query(query)
            
            if result.get('error'):
                print(f"\nError: {result['error']}")
            else:
                print(f"\nSQL Query:\n{result.get('sql_query', 'N/A')}")
                if result.get('query_results') is not None:
                    print(f"\nResults ({len(result['query_results'])} rows):")
                    print(result['query_results'].head(10))
                print(f"\nInsights:\n{result.get('insights', 'N/A')}")
    
    else:
        parser.print_help()
    
    # Cleanup
    pipeline.close()
    print("\n✓ Pipeline closed successfully")

if __name__ == "__main__":
    main()

