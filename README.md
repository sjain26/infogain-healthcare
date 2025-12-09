# Healthcare GenAI Analytics System

A GenAI-powered solution for analyzing healthcare data using natural language queries. This system converts natural language questions into SQL/Python queries, executes them on separate datasets (joined dynamically), and generates descriptive insights.

## 🎯 Overview

This system addresses the challenge of extracting meaningful insights from complex healthcare datasets by:
- Converting natural language queries to SQL/Python queries (intermediate output)
- Dynamically joining multiple datasets on-the-fly (no pre-consolidation)
- Fetching only required data subsets (not full datasets)
- Generating context-aware insights and recommendations

## ✨ Features

- **Natural Language Interface**: Ask questions in plain English
- **SQL/Python Query Generation**: Generates queries as intermediate output
- **Dynamic Data Integration**: Joins datasets temporarily during query execution
- **Subset-Based Processing**: Only query results sent to LLM (not full datasets)
- **Web Interface**: Streamlit-based UI for easy interaction
- **Multiple Data Sources**: Supports SQL databases, Excel files, and CSVs
- **Evaluation Framework**: Comprehensive metrics for SQL accuracy and response quality
- **Ethical Safeguards**: Safety checks and privacy protection

## 📦 Quick Setup

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Key

Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_PROVIDER=groq
MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
```

### 3. Load Data

```bash
python data_preprocessing.py
```

### 4. Run Application

```bash
streamlit run app.py
```

Open browser to `http://localhost:8501`

## 🚀 Usage

### Web Interface

1. Select data source (Sample Dataset or SQL Database)
2. Enter your query in natural language
3. View generated SQL/Python query, results, and insights

### Command Line

```bash
# Single query
python run_pipeline.py --query "How many patients have abnormal blood pressure?"

# Interactive mode
python run_pipeline.py --interactive

# Use Python queries instead of SQL
python run_pipeline.py --query "Average age of patients" --python

# Run evaluation suite
python run_pipeline.py --evaluate
```

### Example Queries

- "How many patients have abnormal blood pressure?"
- "What is the average age of patients with chronic kidney disease?"
- "Show me patients above 60 years with BMI over 30"
- "What is the average physical activity for patients with high stress?"
- "Find patients who smoke and have abnormal blood pressure"

## 📁 Project Structure

```
├── app.py                      # Streamlit web interface
├── genai_pipeline.py           # Core GenAI pipeline (SQL/Python generation)
├── data_preprocessing.py      # Data loading and preprocessing
├── data_audit.py              # Data audit and EDA
├── evaluation.py              # Evaluation framework
├── instruction_tuning.py      # Model fine-tuning framework
├── run_pipeline.py            # CLI script
├── generate_audit_report.py   # Generate data audit report
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── PRESENTATION.md            # Approach and challenges (Mandatory)
├── lu1828272yg3dhb.xlsm      # Sample dataset
└── README.md                  # This file
```

## 📊 Deliverables

### ✅ Mandatory Deliverables

1. **End-to-End Pipeline**
   - ✅ Data extraction and preprocessing (`data_preprocessing.py`)
   - ✅ Data integration and feature engineering (on-the-fly joins)
   - ✅ SQL/Python query generation (`genai_pipeline.py`)
   - ✅ Response generation and insights
   - ✅ Evaluation framework (`evaluation.py`)
   - ✅ Web interface (`app.py` - Streamlit)

2. **Presentation**
   - ✅ See `PRESENTATION.md` for approach, challenges, and solutions

### ✅ Optional Deliverables

1. **Data Audit Report**
   - ✅ Script: `python generate_audit_report.py`
   - ✅ Generates comprehensive data analysis report

2. **Model Fine-Tuning**
   - ✅ Instruction tuning framework (`instruction_tuning.py`)
   - ✅ Training data generation
   - ✅ Fine-tuning scripts

3. **Documentation**
   - ✅ Comprehensive README
   - ✅ Code comments
   - ✅ Setup instructions

## 🔧 Configuration

### Using Sample Dataset (Excel)

The system automatically uses `lu1828272yg3dhb.xlsm` if SQL is not configured.

### Using SQL Database

Edit `.env` file:
```env
SQL_DB_TYPE=mysql
SQL_HOST=your_host
SQL_PORT=3306
SQL_USER=your_user
SQL_PASSWORD=your_password
SQL_DATABASE=your_database
SQL_TABLE_1=health_dataset_1
SQL_TABLE_2=health_dataset_2
```

## 📊 How It Works

### Architecture

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

### Key Features

1. **Query Generation**: LLM generates SQL or Python queries based on user question
2. **Dynamic Joins**: Datasets joined on-the-fly using SQL JOINs or Python merge()
3. **Subset Processing**: Only query results (subset) sent to LLM, not full datasets
4. **Insight Generation**: LLM analyzes subset and generates descriptive insights

**Important:** Only query results (subset) are sent to LLM, NOT full datasets.

## 🧪 Evaluation

Run evaluation suite:
```bash
python run_pipeline.py --evaluate
```

Metrics evaluated:
- SQL accuracy (syntax, correctness)
- Response relevance
- Coherence
- Safety checks

## 🔒 Ethical Considerations

- **No Medical Diagnoses**: System provides descriptive analytics only
- **Data Privacy**: Privacy mode enabled, no logging of sensitive data
- **Safety Checks**: Only SELECT queries allowed, no dangerous operations
- **Disclaimer**: Always consult healthcare professionals for medical advice

## 📝 Dataset Information

### Dataset 1: Health Dataset 1 (N=2000)
- Patient demographics
- Health metrics (BMI, Hemoglobin, Blood Pressure)
- Lifestyle factors (Smoking, Alcohol, Stress)
- Medical conditions (Chronic Kidney Disease, Thyroid Disorders)
- Genetic Pedigree Coefficient

### Dataset 2: Health Dataset 2 (N=20,000)
- Physical activity data (steps per day)
- Day-wise records for each patient

**Note:** Datasets are joined dynamically on `Patient_Number` when needed.

## 🛠️ Development

### Generate Data Audit Report
```bash
python generate_audit_report.py
```

### Generate Training Data for Fine-Tuning
```bash
python instruction_tuning.py
```

### Run Tests
```bash
python run_pipeline.py --query "test query"
```

## 📚 Additional Resources

- **Presentation**: See `PRESENTATION.md` for detailed approach and challenges
- **Configuration**: See `config.py` for all configuration options
- **Evaluation**: See `evaluation.py` for evaluation metrics



---

**Repository:** https://github.com/sjain26/infogain-healthcare

