"""
Streamlit Web Interface for Healthcare GenAI Analytics
"""
import streamlit as st
import pandas as pd
from genai_pipeline import HealthcareGenAI

# Page configuration
st.set_page_config(
    page_title="Healthcare GenAI Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_pipeline(_use_sql=False):
    """
    Load the GenAI pipeline with selected data source
    Note: _use_sql prefix ensures separate cache for each data source
    """
    try:
        # Create a custom preprocessor that respects the data source choice
        from data_preprocessing import DataPreprocessor
        from genai_pipeline import HealthcareGenAI
        import config as cfg
        
        # Store original values
        original_sql_host = cfg.SQL_HOST
        original_sql_db = cfg.SQL_DATABASE
        
        if _use_sql:
            # Use SQL database (if configured)
            if not cfg.SQL_HOST or not cfg.SQL_DATABASE or cfg.SQL_HOST == "":
                return None, "SQL database not configured. Please set SQL connection details in .env file or use Sample Dataset option."
        else:
            # Force use of Excel file by temporarily clearing SQL config
            cfg.SQL_HOST = ""
            cfg.SQL_DATABASE = ""
        
        # Initialize pipeline
        pipeline = HealthcareGenAI()
        
        # Restore original config
        cfg.SQL_HOST = original_sql_host
        cfg.SQL_DATABASE = original_sql_db
        
        return pipeline, None
    except Exception as e:
        return None, str(e)

def main():
    """Main application"""
    st.markdown('<p class="main-header">🏥 Healthcare GenAI Analytics System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Data Source")
        data_source = st.radio(
            "Choose data source:",
            ["Sample Dataset (Excel)", "SQL Database"],
            help="Select whether to use the sample Excel dataset or connect to your SQL database"
        )
        
        use_sql = data_source == "SQL Database"
        
        if use_sql:
            st.info("📊 Using SQL Database")
            st.caption("Make sure SQL connection is configured in .env file")
        else:
            st.info("📁 Using Sample Dataset (Excel)")
            st.caption("Using: lu1828272yg3dhb.xlsm")
        
        st.divider()
        
        st.header("About")
        st.markdown("""
        GenAI-powered healthcare data analytics.
        Ask questions in natural language.
        """)
        
        st.header("Sample Queries")
        sample_queries = [
            "How many patients have abnormal blood pressure?",
            "What is the average age of patients with chronic kidney disease?",
            "Show me patients above 60 years with BMI over 30",
        ]
        
        for query in sample_queries:
            if st.button(query, key=f"sample_{hash(query)}"):
                st.session_state.user_query = query
    
    # Initialize pipeline based on selected data source
    pipeline, error = load_pipeline(_use_sql=use_sql)
    
    if error:
        st.error(f"Error loading pipeline: {error}")
        if use_sql:
            st.info("**For SQL Database:**")
            st.info("1. Configure SQL connection in .env file")
            st.info("2. Set SQL_HOST, SQL_DATABASE, SQL_USER, SQL_PASSWORD")
            st.info("3. Ensure SQL tables exist")
            st.info("4. Or switch to 'Sample Dataset' option")
        else:
            st.info("**For Sample Dataset:**")
            st.info("1. Ensure lu1828272yg3dhb.xlsm file exists")
            st.info("2. Or run: python data_preprocessing.py")
        st.info("3. Ensure GROQ_API_KEY or OPENAI_API_KEY is set in .env file")
        return
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Query Interface")
        
        # Query input
        user_query = st.text_area(
            "Enter your healthcare data query:",
            value=st.session_state.get('user_query', ''),
            height=100,
            placeholder="e.g., How many patients have abnormal blood pressure?"
        )
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            submit_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        with col_btn2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.session_state.user_query = ""
            st.rerun()
    
    with col2:
        st.header("System Status")
        st.success("✓ Pipeline Loaded")
        if use_sql:
            st.info("📊 SQL Database")
            st.caption("Connected to SQL")
        else:
            st.info("📁 Sample Dataset")
            st.caption("Using Excel file")
        st.info("✓ GenAI Model Ready")
    
    # Process query
    if submit_button and user_query:
        with st.spinner("Processing your query..."):
            # Process query
            result = pipeline.process_query(user_query)
            
            # Display results
            st.header("Results")
            
            # Error handling
            if result.get('error'):
                st.error(f"Error: {result['error']}")
                return
            
            # SQL Query
            with st.expander("🔧 Generated SQL Query", expanded=False):
                st.code(result.get('sql_query', 'N/A'), language='sql')
            
            # Query Results
            if result.get('query_results') is not None:
                query_results = result['query_results']
                if len(query_results) > 0:
                    st.subheader("📊 Query Results")
                    st.dataframe(query_results, width='stretch')
                    
                    # Download button
                    csv = query_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No results found for this query.")
            
            # Insights
            if result.get('insights'):
                st.subheader("💡 Generated Insights")
                st.markdown(result['insights'])
            
    
   

if __name__ == "__main__":
    main()

