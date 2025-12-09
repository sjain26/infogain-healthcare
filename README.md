# Healthcare GenAI Analytics System

A GenAI-powered solution for analyzing healthcare data using natural language queries.

## 🎯 Overview

This system allows users to query healthcare datasets using natural language. It automatically:
- Generates SQL queries from natural language
- Executes queries on separate datasets (joined dynamically)
- Provides insights and recommendations

## ✨ Features

- Natural language query interface
- Automatic SQL generation
- Dynamic data joining (no pre-consolidation)
- Web interface (Streamlit)
- Support for SQL Database or Excel files

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
3. View SQL query, results, and insights

### Example Queries

- "How many patients have abnormal blood pressure?"
- "What is the average age of patients with chronic kidney disease?"
- "Show me patients above 60 years with BMI over 30"

## 📁 Project Structure

```
├── app.py                 # Streamlit web interface
├── genai_pipeline.py      # Core GenAI pipeline
├── data_preprocessing.py  # Data loading and preprocessing
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── lu1828272yg3dhb.xlsm  # Sample dataset
└── README.md            # This file
```

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

1. **User Query** → Natural language question
2. **SQL Generation** → LLM generates SQL query
3. **Query Execution** → Executes on database
4. **Insight Generation** → LLM generates insights from results

**Important:** Only query results (subset) are sent to LLM, NOT full datasets.

## ⚠️ Disclaimer

This system provides descriptive analytics only. It does not provide medical diagnoses or treatment recommendations. Always consult healthcare professionals for medical advice.

## 📝 License

For educational and research purposes.

---

**Repository:** https://github.com/sjain26/infogain-healthcare
