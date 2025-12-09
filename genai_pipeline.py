"""
GenAI Pipeline for Healthcare Data Analytics
Converts natural language queries to SQL, executes queries, and generates insights
"""
import os
import re
from typing import Dict, List, Tuple, Optional
import pandas as pd
try:
    from langchain_openai import ChatOpenAI
    try:
        from langchain.schema import HumanMessage, SystemMessage
    except ImportError:
        from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    # Fallback for older langchain versions
    try:
        from langchain.chat_models import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
    except ImportError:
        from langchain_community.chat_models import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
from data_preprocessing import DataPreprocessor
from config import MODEL_NAME, TEMPERATURE, MAX_TOKENS, OPENAI_API_KEY, GROQ_API_KEY, MODEL_PROVIDER, ENABLE_SAFETY_CHECKS

class HealthcareGenAI:
    """Main GenAI pipeline for healthcare analytics"""
    
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.preprocessor.setup_database(
            *self.preprocessor.load_datasets()
        )
        self.schema_info = self.preprocessor.get_schema_info()
        
        # Initialize LLM (Groq or OpenAI)
        if MODEL_PROVIDER.lower() == "groq":
            try:
                from groq import Groq
                if not GROQ_API_KEY:
                    raise ValueError("GROQ_API_KEY not found. Please set it in .env file")
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                self.model_provider = "groq"
                print(f"✓ Using Groq model: {MODEL_NAME}")
            except ImportError:
                raise ImportError("groq package not installed. Run: pip install groq")
        else:
            # Use OpenAI
            if OPENAI_API_KEY:
                try:
                    self.llm = ChatOpenAI(
                        model_name=MODEL_NAME,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                        openai_api_key=OPENAI_API_KEY
                    )
                except TypeError:
                    # Handle different parameter names in different versions
                    self.llm = ChatOpenAI(
                        model=MODEL_NAME,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                        openai_api_key=OPENAI_API_KEY
                    )
                self.model_provider = "openai"
                print(f"✓ Using OpenAI model: {MODEL_NAME}")
            else:
                raise ValueError("OPENAI_API_KEY not found. Please set it in .env file")
        
        # Schema description for prompt
        self.schema_description = self._get_schema_description()
        
    def _get_schema_description(self) -> str:
        """Generate schema description for LLM prompts"""
        desc = """
DATABASE SCHEMA:

Table 1: health_dataset_1
- Patient_Number (TEXT): Unique patient identifier
- Blood_Pressure_Abnormality (INTEGER): 0=Normal, 1=Abnormal
- Level_of_Hemoglobin (REAL): Hemoglobin level in g/dl
- Genetic_Pedigree_Coefficient (REAL): 0-1, higher = closer family history
- Age (INTEGER): Patient age
- BMI (REAL): Body Mass Index
- Sex (INTEGER): 0=Male, 1=Female
- Pregnancy (INTEGER): 0=No, 1=Yes
- Smoking (INTEGER): 0=No, 1=Yes
- salt_content_in_the_diet (REAL): Salt intake in mg/day
- alcohol_consumption_per_day (REAL): Alcohol intake in ml/day
- Level_of_Stress (INTEGER): 1=Low, 2=Normal, 3=High
- Chronic_kidney_disease (INTEGER): 0=No, 1=Yes
- Adrenal_and_thyroid_disorders (INTEGER): 0=No, 1=Yes

Table 2: health_dataset_2
- Patient_Number (TEXT): Unique patient identifier (joins with health_dataset_1)
- Day_Number (INTEGER): Day number (1-10)
- Physical_activity (INTEGER): Number of steps per day

JOIN KEY: Patient_Number
"""
        return desc
    
    def _call_llm(self, messages):
        """Call LLM (Groq or OpenAI)"""
        if self.model_provider == "groq":
            # Convert messages to Groq format
            groq_messages = []
            for msg in messages:
                if isinstance(msg, SystemMessage):
                    groq_messages.append({"role": "system", "content": msg.content})
                elif isinstance(msg, HumanMessage):
                    groq_messages.append({"role": "user", "content": msg.content})
            
            completion = self.groq_client.chat.completions.create(
                model=MODEL_NAME,
                messages=groq_messages,
                temperature=TEMPERATURE,
                max_completion_tokens=MAX_TOKENS,
                top_p=1
            )
            return type('Response', (), {'content': completion.choices[0].message.content})()
        else:
            # OpenAI
            return self.llm(messages)
    
    def _create_sql_generation_prompt(self, user_query: str) -> str:
        """Create prompt for SQL generation"""
        system_prompt = f"""You are an expert SQL query generator for healthcare data analysis.

{self.schema_description}

INSTRUCTIONS:
1. Generate ONLY valid SQLite SQL queries based on the user's question
2. Use JOIN when data from both tables is needed
3. Use appropriate aggregations (COUNT, AVG, SUM, MAX, MIN) when needed
4. Use WHERE clauses for filtering
5. Return ONLY the SQL query, no explanations
6. Use proper column names as specified in the schema
7. For patient-specific queries, use Patient_Number for filtering
8. Always use table aliases: h1 for health_dataset_1, h2 for health_dataset_2

EXAMPLES:
User: "How many patients have abnormal blood pressure?"
SQL: SELECT COUNT(*) FROM health_dataset_1 WHERE Blood_Pressure_Abnormality = 1;

User: "What is the average physical activity for patients with high stress?"
SQL: SELECT AVG(h2.Physical_activity) FROM health_dataset_1 h1 JOIN health_dataset_2 h2 ON h1.Patient_Number = h2.Patient_Number WHERE h1.Level_of_Stress = 3;

User: "Show me patients above 60 years with BMI over 30"
SQL: SELECT Patient_Number, Age, BMI FROM health_dataset_1 WHERE Age > 60 AND BMI > 30;

Now generate SQL for this query:"""
        
        return f"{system_prompt}\n\nUser Query: {user_query}\n\nSQL Query:"
    
    def _extract_sql_from_response(self, response: str) -> str:
        """Extract SQL query from LLM response"""
        # Remove markdown code blocks if present
        response = re.sub(r'```sql\n?', '', response, flags=re.IGNORECASE)
        response = re.sub(r'```\n?', '', response)
        response = response.strip()
        
        # Find SQL query (usually ends with semicolon or is the entire response)
        sql_match = re.search(r'(SELECT.*?;)', response, re.DOTALL | re.IGNORECASE)
        if sql_match:
            return sql_match.group(1).strip()
        
        # If no semicolon, take the whole response if it starts with SELECT
        if response.upper().startswith('SELECT'):
            return response
        
        return response
    
    def _safety_check(self, sql_query: str) -> Tuple[bool, str]:
        """Perform safety checks on SQL query"""
        if not ENABLE_SAFETY_CHECKS:
            return True, ""
        
        # Check for dangerous SQL operations
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        sql_upper = sql_query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False, f"Safety check failed: Dangerous operation '{keyword}' detected"
        
        # Check that it's a SELECT query
        if not sql_upper.strip().startswith('SELECT'):
            return False, "Safety check failed: Only SELECT queries are allowed"
        
        return True, ""
    
    def _create_insight_generation_prompt(self, user_query: str, sql_query: str, query_results: pd.DataFrame) -> str:
        """Create prompt for generating natural language insights"""
        # Format query results more clearly
        if len(query_results) == 0:
            results_str = "No results found"
        elif len(query_results) == 1 and len(query_results.columns) == 1:
            # Single value result (like COUNT, AVG)
            col_name = query_results.columns[0]
            value = query_results.iloc[0, 0]
            results_str = f"Result: {col_name} = {value}"
        elif len(query_results) <= 10:
            # Small result set - show all
            results_str = query_results.to_string(index=False)
        else:
            # Large result set - show summary
            results_str = f"Total rows: {len(query_results)}\nFirst 10 rows:\n{query_results.head(10).to_string(index=False)}\n... (showing first 10 of {len(query_results)} total rows)"
        
        # Calculate total patients for context if needed
        total_patients = None
        try:
            if "COUNT" in sql_query.upper() and "WHERE" in sql_query.upper():
                # Try to get total count for percentage calculation
                total_df = self.preprocessor.execute_query("SELECT COUNT(*) as total FROM health_dataset_1")
                if len(total_df) > 0:
                    total_patients = total_df.iloc[0, 0]
        except:
            pass
        
        # Format results more clearly for LLM
        if len(query_results) == 1 and len(query_results.columns) == 1:
            # Single value - extract it clearly
            value = query_results.iloc[0, 0]
            col_name = query_results.columns[0]
            results_summary = f"The query returned: {col_name} = {value}"
            if total_patients and "COUNT" in col_name.upper():
                percentage = (value / total_patients * 100) if total_patients > 0 else 0
                results_summary += f"\nThis represents {value} out of {total_patients} total patients ({percentage:.1f}%)"
        else:
            results_summary = f"Query Results:\n{results_str}"
        
        prompt = f"""You are a healthcare data analyst. Based on the user's question and the EXACT query results, provide a clear, insightful response.

CRITICAL INSTRUCTIONS:
- Use ONLY the exact numbers from the results below
- If a count and total are provided, you may calculate the percentage
- Be precise and accurate - do not estimate or guess
- Write in a natural, professional manner

User's Question: {user_query}

SQL Query Executed:
{sql_query}

{results_summary}

Provide a clear, concise analysis (2-3 paragraphs) using the exact numbers above:"""
        
        return prompt
    
    def generate_sql_query(self, user_query: str) -> Tuple[str, Optional[str]]:
        """Generate SQL query from natural language"""
        try:
            prompt = self._create_sql_generation_prompt(user_query)
            messages = [
                SystemMessage(content="You are an expert SQL query generator."),
                HumanMessage(content=prompt)
            ]
            response = self._call_llm(messages)
            sql_query = self._extract_sql_from_response(response.content)
            
            # Safety check
            is_safe, error_msg = self._safety_check(sql_query)
            if not is_safe:
                return None, error_msg
            
            return sql_query, None
        except Exception as e:
            return None, f"Error generating SQL: {str(e)}"
    
    def execute_query(self, sql_query: str) -> Tuple[pd.DataFrame, Optional[str]]:
        """Execute SQL query and return results"""
        try:
            results = self.preprocessor.execute_query(sql_query)
            return results, None
        except Exception as e:
            return pd.DataFrame(), f"Error executing query: {str(e)}"
    
    def generate_insights(self, user_query: str, sql_query: str, query_results: pd.DataFrame) -> str:
        """Generate natural language insights from query results"""
        try:
            prompt = self._create_insight_generation_prompt(user_query, sql_query, query_results)
            messages = [
                SystemMessage(content="You are a healthcare data analyst providing insights."),
                HumanMessage(content=prompt)
            ]
            response = self._call_llm(messages)
            return response.content
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def process_query(self, user_query: str, use_python: bool = False) -> Dict:
        """
        Main method to process user query end-to-end
        
        CRITICAL: This implements the required architecture:
        1. Generate SQL/Python query (INTERMEDIATE OUTPUT)
        2. Execute query to fetch SUBSET of data
        3. Generate insights from SUBSET only (NOT full datasets)
        
        Args:
            user_query: Natural language query
            use_python: If True, use Python query instead of SQL
        """
        result = {
            'user_query': user_query,
            'sql_query': None,
            'python_query': None,
            'query_type': 'python' if use_python else 'sql',
            'query_results': None,
            'insights': None,
            'error': None
        }
        
        # Step 1: Generate SQL/Python query (INTERMEDIATE OUTPUT - as per requirements)
        if use_python:
            python_query, error = self.generate_python_query(user_query)
            if error:
                result['error'] = error
                return result
            result['python_query'] = python_query
            # For Python queries, we'd need to execute them differently
            # For now, we'll use SQL as primary method
            result['error'] = "Python query execution not yet implemented. Using SQL instead."
            use_python = False
        
        if not use_python:
            sql_query, error = self.generate_sql_query(user_query)
            if error:
                result['error'] = error
                return result
            result['sql_query'] = sql_query
        
        # Step 2: Execute query to fetch SUBSET of data (NOT full datasets)
        query_results, error = self.execute_query(sql_query)
        if error:
            result['error'] = error
            return result
        
        result['query_results'] = query_results
        
        # Step 3: Generate insights from SUBSET only
        # NOTE: Only the query results (subset) are sent to LLM, NOT the full datasets
        insights = self.generate_insights(user_query, sql_query, query_results)
        result['insights'] = insights
        
        return result
    
    def close(self):
        """Close database connections"""
        self.preprocessor.close()

