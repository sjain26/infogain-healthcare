# Healthcare GenAI Analytics System

A comprehensive GenAI-powered solution for analyzing healthcare data using natural language queries. The system automatically generates SQL queries, executes them on separate datasets (joined on-the-fly), and provides intelligent insights and recommendations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

This project implements an end-to-end GenAI pipeline that:
- **Accepts natural language queries** about healthcare data
- **Generates SQL/Python queries** as intermediate output (as per requirements)
- **Executes queries** on separate datasets (no pre-consolidation)
- **Joins data dynamically** using SQL JOIN operations
- **Generates contextually relevant insights** in natural language
- **Provides a user-friendly web interface** for querying

## ✨ Key Features

### 🔍 Natural Language Query Interface
- Ask questions in plain English - no SQL knowledge required
- Supports complex queries with multiple conditions
- Handles aggregations, filtering, and joins automatically

### 🤖 Intelligent SQL Generation
- LLM-powered SQL query generation
- Schema-aware query construction
- Safety checks to prevent dangerous operations
- Supports both SQL and Python query generation

### 🔗 Dynamic Data Integration
- **No pre-consolidation** - datasets remain separate
- **On-the-fly joining** - SQL JOIN operations at query time
- Supports multiple data sources (SQL Database, Excel, CSV)
- Efficient query execution with indexed joins

### 🛡️ Safety & Ethics
- Medical safety checks - no diagnostic recommendations
- Descriptive analytics only
- Data privacy protection
- Appropriate disclaimers in responses

### 📊 Comprehensive Evaluation
- SQL accuracy metrics
- Response relevance scoring
- Coherence and readability evaluation
- Safety compliance checks

## 🏗️ Architecture

```
User Query (Natural Language)
    ↓
GenAI Pipeline
    ↓
SQL Query Generation (INTERMEDIATE OUTPUT)
    ↓
Query Execution (Database with Dynamic JOIN)
    ↓
Result Processing (Subset Only)
    ↓
Insight Generation (Natural Language)
    ↓
Response to User
```

**Critical Design:** Only query results (subset) are sent to LLM, NOT full datasets.

## 📋 Requirements Compliance

✅ **All Mandatory Deliverables Completed**

1. **Data Audit Report** (Optional) ✅
   - Comprehensive EDA and data quality analysis
   - Statistical summaries and visualizations

2. **End-to-End Pipeline** (Mandatory) ✅
   - Data extraction and preprocessing
   - GenAI integration with SQL/Python query generation
   - Model fine-tuning/instruction-tuning setup
   - Response generation and evaluation framework
   - Web-based interface (Streamlit)

3. **Presentation** (Mandatory) ✅
   - Complete presentation content in `PRESENTATION.md`

4. **Code and Documentation** (Optional) ✅
   - Comprehensive documentation
   - Setup instructions
   - Code comments

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (or OpenAI API key)
- Git (for cloning)

### Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/sjain26/infogain-healthcare.git
cd infogain-healthcare

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp ENV_EXAMPLE.txt .env
# Edit .env and add your API keys:
# GROQ_API_KEY=your_key_here
# Or OPENAI_API_KEY=your_key_here

# 5. Load sample data (if using Excel)
python data_preprocessing.py

# 6. Run web interface
streamlit run app.py
```

## 🚀 Usage

### Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Natural language query input
- Data source selection (Sample Dataset or SQL Database)
- Real-time SQL query visualization
- Results display and download
- Generated insights
- Evaluation metrics (optional)

### Command Line Interface

```bash
# Single query
python run_pipeline.py --query "How many patients have abnormal blood pressure?"

# Interactive mode
python run_pipeline.py --interactive

# Run evaluation
python run_pipeline.py --evaluate
```

### Python API

```python
from genai_pipeline import HealthcareGenAI

# Initialize pipeline
pipeline = HealthcareGenAI()

# Process query
result = pipeline.process_query("How many patients have abnormal blood pressure?")

# Access results
print(f"SQL Query: {result['sql_query']}")
print(f"Results: {result['query_results']}")
print(f"Insights: {result['insights']}")

# Close pipeline
pipeline.close()
```

## 📊 Data Sources

### Option 1: Sample Dataset (Excel)

The system includes a sample dataset: `lu1828272yg3dhb.xlsm`

- **Dataset 1:** Health Dataset 1 (N=2000)
  - Demographics, health metrics, lifestyle factors
  - 14 variables per patient

- **Dataset 2:** Health Dataset 2 (N=20,000)
  - Physical activity data (10 days per patient)
  - Time-series data

### Option 2: SQL Database

Configure your SQL database connection in `.env`:

```env
SQL_DB_TYPE=mysql  # or postgresql, sqlserver, sqlite
SQL_HOST=your_host
SQL_PORT=3306
SQL_USER=your_user
SQL_PASSWORD=your_password
SQL_DATABASE=your_database
SQL_TABLE_1=health_dataset_1
SQL_TABLE_2=health_dataset_2
```

**Supported Databases:**
- MySQL
- PostgreSQL
- SQL Server
- SQLite

See `SQL_SETUP.md` for detailed setup instructions.

## 💡 Example Queries

### Simple Queries
```
How many patients have abnormal blood pressure?
What is the average age of patients with chronic kidney disease?
How many patients smoke?
```

### Complex Queries
```
Show me patients above 60 years with BMI over 30
What is the average physical activity for patients with high stress?
Find patients who smoke and have abnormal blood pressure
```

### Aggregation Queries
```
What is the distribution of stress levels among female patients?
Show me the average hemoglobin level by age group
What is the correlation between salt intake and blood pressure abnormality?
```

## 🔧 Configuration

### Environment Variables

Create `.env` file from `ENV_EXAMPLE.txt`:

```env
# API Configuration
GROQ_API_KEY=your_groq_api_key_here
# Or
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
MODEL_PROVIDER=groq  # or openai
MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct

# SQL Database (if using SQL)
SQL_DB_TYPE=mysql
SQL_HOST=localhost
SQL_PORT=3306
SQL_USER=root
SQL_PASSWORD=your_password
SQL_DATABASE=healthcare
SQL_TABLE_1=health_dataset_1
SQL_TABLE_2=health_dataset_2
```

## 📁 Project Structure

```
infogain-healthcare/
├── app.py                      # Streamlit web interface
├── config.py                   # Configuration settings
├── data_preprocessing.py       # Data loading and preprocessing
├── genai_pipeline.py          # Core GenAI pipeline
├── evaluation.py              # Evaluation framework
├── instruction_tuning.py      # Fine-tuning setup
├── data_audit.py             # EDA and data audit
├── data_generator.py         # Sample data generation
├── run_pipeline.py           # CLI interface
├── setup.sh                  # Setup script
├── setup_sql.py              # SQL setup helper
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── ENV_EXAMPLE.txt          # Environment template
├── lu1828272yg3dhb.xlsm     # Sample dataset
├── data/                     # Data directory
│   └── .gitkeep
├── reports/                  # Generated reports
└── training_data/           # Fine-tuning data
```

## 🧪 Testing

### Run Verification Tests

```bash
# System test
python test_system.py

# Query verification
python verify_queries.py
```

### Evaluation

```bash
python evaluation.py
```

## 📚 Documentation

- **README.md** - This file (main documentation)
- **QUICKSTART.md** - Quick start guide
- **SQL_SETUP.md** - SQL database setup guide
- **DEPLOYMENT.md** - Deployment instructions
- **REQUIREMENTS_COMPLIANCE.md** - Detailed requirements compliance
- **PRESENTATION.md** - Presentation content
- **PROJECT_SUMMARY.md** - Project overview

## 🔐 Security & Privacy

### Data Privacy
- ✅ No user data logging
- ✅ Privacy mode enabled
- ✅ Anonymized datasets only
- ✅ Secure database connections

### Medical Safety
- ✅ Descriptive analytics only
- ✅ No diagnoses or treatment recommendations
- ✅ Safety checks in place
- ✅ Appropriate disclaimers

### API Keys
- ✅ Never commit API keys to repository
- ✅ Use `.env` file (included in `.gitignore`)
- ✅ Use `ENV_EXAMPLE.txt` as template

## 🐛 Troubleshooting

### Common Issues

**Issue:** "GROQ_API_KEY not found"
- **Solution:** Add your API key to `.env` file

**Issue:** "Dataset file not found"
- **Solution:** Run `python data_preprocessing.py` to load sample data

**Issue:** "SQL connection failed"
- **Solution:** Check SQL credentials in `.env` or use Sample Dataset option

**Issue:** "Import errors"
- **Solution:** Ensure virtual environment is activated and run `pip install -r requirements.txt`

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Add secrets (API keys) in Streamlit Cloud settings
5. Deploy!

### Local Deployment

```bash
streamlit run app.py
```

### Docker Deployment

See `DEPLOYMENT.md` for Docker and other deployment options.

## 📊 Evaluation Metrics

The system evaluates responses on multiple dimensions:

1. **SQL Accuracy** (30% weight)
   - Syntax correctness
   - Query structure
   - Safety compliance

2. **Response Relevance** (30% weight)
   - Keyword overlap
   - Query alignment
   - Data-driven insights

3. **Response Coherence** (20% weight)
   - Readability
   - Structure
   - Clarity

4. **Response Safety** (20% weight)
   - Medical appropriateness
   - No diagnoses
   - Appropriate disclaimers

## 🤝 Contributing

This is a project submission. For questions or issues, please refer to the documentation.

## 📝 License

This project is for educational and research purposes.

## 👥 Author

Developed as part of the Healthcare GenAI Analytics Challenge.

## 🙏 Acknowledgments

- Groq for LLM API
- Streamlit for web framework
- Open source community for libraries

---

## ⚠️ Disclaimer

**This system provides descriptive analytics only. It does not provide medical diagnoses or treatment recommendations. Always consult with healthcare professionals for medical advice.**

---

## 📞 Support

For setup help, see:
- `QUICKSTART.md` - Quick start guide
- `SQL_SETUP.md` - SQL database setup
- `DEPLOYMENT.md` - Deployment guide

---

**Repository:** https://github.com/sjain26/infogain-healthcare

**Status:** ✅ Production Ready
