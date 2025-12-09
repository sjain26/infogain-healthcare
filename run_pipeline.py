"""
Main script to run the pipeline
"""
import argparse
from genai_pipeline import HealthcareGenAI
from evaluation import Evaluator

def main():
    parser = argparse.ArgumentParser(description='Healthcare GenAI Analytics Pipeline')
    parser.add_argument('--query', type=str, help='Single query to process')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--evaluate', action='store_true', help='Run evaluation suite')
    parser.add_argument('--python', action='store_true', help='Use Python queries instead of SQL')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    print("Initializing GenAI pipeline...")
    pipeline = HealthcareGenAI()
    
    if args.query:
        # Process single query
        print(f"\nProcessing query: {args.query}")
        result = pipeline.process_query(args.query, use_python=args.python)
        
        print("\n" + "="*80)
        print("RESULTS")
        print("="*80)
        if result.get('sql_query'):
            print(f"\nSQL Query:\n{result.get('sql_query', 'N/A')}")
        if result.get('python_query'):
            print(f"\nPython Query:\n{result.get('python_query', 'N/A')}")
        print(f"\nQuery Results:\n{result.get('query_results', 'N/A')}")
        print(f"\nInsights:\n{result.get('insights', 'N/A')}")
        if result.get('error'):
            print(f"\nError: {result['error']}")
    
    elif args.evaluate:
        # Run evaluation
        print("\nRunning evaluation suite...")
        evaluator = Evaluator(pipeline)
        results = evaluator.run_evaluation_suite()
        
        print("\n" + "="*80)
        print("EVALUATION RESULTS")
        print("="*80)
        print(f"Total Queries: {results['total_queries']}")
        print(f"Average SQL Score: {results['avg_sql_score']:.3f}")
        print(f"Average Relevance: {results['avg_relevance']:.3f}")
        print(f"Average Coherence: {results['avg_coherence']:.3f}")
        print(f"Average Safety: {results['avg_safety']:.3f}")
        print(f"Overall Score: {results['avg_overall_score']:.3f}")
        
        # Save report
        evaluator.save_evaluation_report(results)
        print("\n✓ Evaluation report saved")
    
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
            
            result = pipeline.process_query(query, use_python=args.python)
            
            if result.get('error'):
                print(f"\nError: {result['error']}")
            else:
                if result.get('sql_query'):
                    print(f"\nSQL Query:\n{result.get('sql_query', 'N/A')}")
                if result.get('python_query'):
                    print(f"\nPython Query:\n{result.get('python_query', 'N/A')}")
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

