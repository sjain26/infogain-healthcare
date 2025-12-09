# Healthcare GenAI Analytics System
## Presentation: Approach, Challenges & Solution

---

## 🎯 Problem Statement

Healthcare datasets contain rich information about patient demographics, genetics, and lifestyle factors. However, extracting meaningful insights requires:
- Complex SQL queries
- Data science expertise
- Time-consuming analysis

**Solution:** Develop a GenAI system that converts natural language queries into actionable insights.

---

## 📋 Objectives Achieved

✅ **Natural Language Query Interface**
- Users ask questions in plain English
- System understands complex healthcare queries

✅ **Dynamic Data Integration**
- Joins multiple datasets on-the-fly (temporarily)
- No pre-consolidation of datasets
- Maintains data separation

✅ **SQL/Python Query Generation**
- Generates SQL or Python queries as intermediate output
- Fetches only required data subset
- Sends subset to LLM (not full datasets)

✅ **Context-Aware Insights**
- Generates descriptive analytics
- Provides recommendations based on data
- Maintains ethical boundaries

---

## 🏗️ Architecture

### Pipeline Flow

```
User Query (Natural Language)
    ↓
[GenAI Model] → SQL/Python Query (Intermediate Output)
    ↓
[Query Execution] → Data Subset (NOT full datasets)
    ↓
[GenAI Model] → Natural Language Insights
    ↓
User receives insights
```

### Key Components

1. **Data Preprocessing** (`data_preprocessing.py`)
   - Loads from SQL, Excel, or CSV
   - Cleans and validates data
   - Sets up SQLite for query execution

2. **GenAI Pipeline** (`genai_pipeline.py`)
   - SQL/Python query generation
   - Query execution
   - Insight generation

3. **Evaluation Framework** (`evaluation.py`)
   - SQL accuracy metrics
   - Response relevance
   - Coherence and safety checks

4. **Web Interface** (`app.py`)
   - Streamlit-based UI
   - Real-time query processing
   - Results visualization

---

## 🔧 Technical Implementation

### 1. Data Integration Strategy

**Challenge:** Avoid consolidating datasets while enabling cross-dataset queries.

**Solution:**
- Keep datasets separate in database
- Use SQL JOINs dynamically when needed
- Temporary joins only during query execution
- No permanent data consolidation

```sql
-- Example: Joining datasets on-the-fly
SELECT AVG(h2.Physical_activity) 
FROM health_dataset_1 h1 
JOIN health_dataset_2 h2 
ON h1.Patient_Number = h2.Patient_Number 
WHERE h1.Level_of_Stress = 3;
```

### 2. Query Generation (SQL/Python)

**SQL Approach:**
- LLM generates SQLite-compatible queries
- Schema-aware generation
- Safety checks (SELECT only, no DROP/DELETE)

**Python Approach:**
- Alternative pandas-based queries
- Uses merge() for joins
- Executes in safe environment

### 3. Subset-Based Processing

**Critical Requirement:** Don't send full datasets to LLM.

**Implementation:**
- Execute query first → Get subset
- Send only query results to LLM
- LLM generates insights from subset
- Reduces token usage and improves accuracy

### 4. Model Integration

**Provider:** Groq (meta-llama/llama-4-scout-17b-16e-instruct)
- Fast inference
- Cost-effective
- Good SQL generation capability

**Prompt Engineering:**
- Clear schema descriptions
- Example-based learning
- Safety constraints

---

## 📊 Deliverables

### ✅ Mandatory Deliverables

1. **End-to-End Pipeline**
   - ✅ Data extraction and preprocessing
   - ✅ Data integration (on-the-fly joins)
   - ✅ SQL/Python query generation
   - ✅ Response generation
   - ✅ Evaluation framework
   - ✅ Web interface (Streamlit)

2. **Presentation**
   - ✅ This document
   - ✅ Approach explanation
   - ✅ Challenges and solutions

### ✅ Optional Deliverables

1. **Data Audit Report**
   - ✅ Script: `generate_audit_report.py`
   - ✅ Comprehensive data analysis
   - ✅ Quality metrics

2. **Model Fine-Tuning**
   - ✅ Instruction tuning framework
   - ✅ Training data generation
   - ✅ Fine-tuning scripts

3. **Documentation**
   - ✅ Comprehensive README
   - ✅ Code comments
   - ✅ Setup instructions

---

## 🚧 Challenges Faced

### 1. **LLM Accuracy Issues**

**Problem:** LLM sometimes generated incorrect numerical insights (e.g., "0.0%" or wrong percentages).

**Solution:**
- Improved prompt engineering
- Explicit instructions to use exact numbers
- Automatic percentage calculation when total available
- Better result formatting

### 2. **Data Source Flexibility**

**Problem:** Need to support SQL databases, Excel files, and CSVs.

**Solution:**
- Priority-based loading (SQL → Excel → CSV)
- Fallback mechanisms
- User selection in UI

### 3. **Dynamic Joins**

**Problem:** Joining datasets without pre-consolidation.

**Solution:**
- SQL JOINs executed on-the-fly
- Python merge() for alternative approach
- Temporary joins only during query execution

### 4. **Token Efficiency**

**Problem:** Sending full datasets to LLM is expensive and slow.

**Solution:**
- Query-first approach
- Send only query results (subset)
- Format results efficiently

### 5. **Safety & Ethics**

**Problem:** Prevent dangerous queries and medical diagnoses.

**Solution:**
- SQL safety checks (SELECT only)
- Ethical disclaimers
- No diagnostic recommendations
- Privacy mode enabled

---

## 🎯 How Solution Addresses Requirements

### ✅ Requirement 1: Natural Language to Insights
- Users ask questions in English
- System generates SQL/Python queries
- Executes queries and provides insights

### ✅ Requirement 2: Multiple Data Sources
- Supports SQL databases
- Supports Excel files
- Supports CSV files
- Dynamic joins without consolidation

### ✅ Requirement 3: Query as Intermediate Output
- SQL/Python queries generated first
- Visible to users (transparency)
- Executed to fetch subset
- Subset sent to LLM (not full data)

### ✅ Requirement 4: Evaluation Framework
- SQL accuracy metrics
- Response relevance scoring
- Coherence evaluation
- Safety checks

### ✅ Requirement 5: Web Interface
- Streamlit-based UI
- Real-time processing
- Results visualization
- Download capabilities

### ✅ Requirement 6: Ethical Considerations
- No medical diagnoses
- Data privacy mode
- Safety checks
- Clear disclaimers

---

## 📈 Evaluation Metrics

### SQL Accuracy
- Syntax validation
- Query correctness
- Safety compliance

### Response Quality
- Relevance to query
- Coherence
- Accuracy of numbers

### Safety
- No dangerous operations
- Ethical compliance
- Privacy protection

---

## 🔮 Future Enhancements

1. **Model Fine-Tuning**
   - Fine-tune on healthcare-specific queries
   - Improve SQL generation accuracy

2. **Advanced Analytics**
   - Statistical analysis
   - Trend detection
   - Predictive insights

3. **Multi-Model Support**
   - Support multiple LLM providers
   - Model comparison

4. **Enhanced UI**
   - Query history
   - Saved queries
   - Export capabilities

---

## 📝 Conclusion

This GenAI solution successfully:
- ✅ Converts natural language to actionable insights
- ✅ Handles multiple data sources dynamically
- ✅ Generates SQL/Python queries as intermediate output
- ✅ Processes only data subsets (not full datasets)
- ✅ Provides comprehensive evaluation framework
- ✅ Maintains ethical standards

**Ready for validation on interview queries.**

---

## 📚 Repository

**GitHub:** https://github.com/sjain26/infogain-healthcare

**Setup:** See README.md for installation and usage instructions.

