# Healthcare GenAI Analytics System

A comprehensive GenAI solution for analyzing healthcare data using natural language queries, SQL generation, and intelligent insights.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Components](#key-components)
- [Evaluation](#evaluation)
- [Ethical Considerations](#ethical-considerations)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

This project implements an end-to-end GenAI pipeline that:
- Accepts natural language queries about healthcare data
- Generates SQL queries to fetch relevant data subsets
- Executes queries on separate datasets (joined on-the-fly)
- Generates contextually relevant insights and recommendations
- Provides a user-friendly web interface

## ✨ Features

1. **Natural Language Query Interface**: Ask questions in plain English
2. **Intelligent SQL Generation**: Automatically converts queries to SQL
3. **On-the-Fly Data Joining**: Joins multiple datasets dynamically
4. **Safety Checks**: Prevents dangerous SQL operations
5. **Medical Safety**: Avoids providing diagnoses or treatment advice
6. **Comprehensive Evaluation**: Metrics for SQL accuracy, relevance, coherence, and safety
7. **Web Interface**: Streamlit-based user interface

## 🏗️ Architecture

```
User Query (Natural Language)
    ↓
GenAI Pipeline
    ↓
SQL Query Generation
    ↓
Query Execution (Database)
    ↓
Result Processing
    ↓
Insight Generation (Natural Language)
    ↓
Response to User
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (or alternative LLM provider)

### Steps

1. **Clone the repository**
   ```bash
   cd /home/dell/Music/infogain
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy example and configure
   cp ENV_EXAMPLE.txt .env
   # Edit .env and add:
   # - Your OPENAI_API_KEY
   # - Your SQL database connection details (if using SQL database)
   ```
   
   **For SQL Database Setup:**
   ```bash
   # Option 1: Use interactive setup script
   python setup_sql.py
   
   # Option 2: Manually edit .env file with your SQL connection details
   # See ENV_EXAMPLE.txt for configuration options
   ```

5. **Load your data**
   
   **Option A: From SQL Database (Recommended)**
   ```bash
   # Configure SQL connection in .env file first
   # Then run preprocessing to load from SQL
   python data_preprocessing.py
   ```
   
   **Option B: From Excel/CSV files (Fallback)**
   ```bash
   # If you have Excel/CSV files, place them in the project directory
   # The system will automatically detect and load them
   python data_preprocessing.py
   ```
   
   **Option C: Generate sample data (for testing)**
   ```bash
   python data_generator.py
   python data_preprocessing.py
   ```

7. **Run data audit (optional)**
   ```bash
   python data_audit.py
   ```

## 🚀 Usage

### Web Interface

Launch the Streamlit web interface:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Command Line Usage

```python
from genai_pipeline import HealthcareGenAI

# Initialize pipeline
pipeline = HealthcareGenAI()

# Process a query
result = pipeline.process_query("How many patients have abnormal blood pressure?")

# Access results
print(f"SQL Query: {result['sql_query']}")
print(f"Results: {result['query_results']}")
print(f"Insights: {result['insights']}")
```

### Evaluation

Run the evaluation suite:

```bash
python evaluation.py
```

### Instruction Tuning

Generate training data for fine-tuning:

```bash
python instruction_tuning.py
```

## 📁 Project Structure

```
infogain/
├── app.py                      # Streamlit web interface
├── config.py                   # Configuration settings
├── data_generator.py           # Generate sample datasets
├── data_preprocessing.py       # Data cleaning and database setup
├── data_audit.py              # EDA and data audit
├── genai_pipeline.py          # Main GenAI pipeline
├── instruction_tuning.py      # Fine-tuning data preparation
├── evaluation.py              # Evaluation framework
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── data/                      # Data directory
│   ├── health_dataset_1.csv
│   ├── health_dataset_2.csv
│   └── healthcare.db
├── reports/                   # Generated reports
│   ├── data_audit_report.txt
│   ├── evaluation_report.json
│   └── figures/
├── training_data/             # Fine-tuning data
│   └── training_data.jsonl
└── scripts/                   # Utility scripts
    └── fine_tune.sh
```

## 🔧 Key Components

### 1. Data Preprocessing (`data_preprocessing.py`)

- Loads and cleans both datasets
- Validates data quality
- Sets up SQLite database
- Creates indexes for efficient joins

### 2. GenAI Pipeline (`genai_pipeline.py`)

- **SQL Generation**: Converts natural language to SQL
- **Query Execution**: Runs SQL on database
- **Insight Generation**: Creates natural language responses
- **Safety Checks**: Prevents dangerous operations

### 3. Evaluation Framework (`evaluation.py`)

Metrics evaluated:
- **SQL Accuracy**: Syntax correctness, structure
- **Response Relevance**: Alignment with user query
- **Response Coherence**: Readability and structure
- **Response Safety**: Medical appropriateness

### 4. Web Interface (`app.py`)

- User-friendly query interface
- Real-time results display
- SQL query visualization
- Downloadable results
- Evaluation metrics display

## 📊 Evaluation

The system evaluates responses on multiple dimensions:

1. **SQL Syntax Score** (0-1): Valid SQL structure
2. **Relevance Score** (0-1): Alignment with query
3. **Coherence Score** (0-1): Readability
4. **Safety Score** (0-1): Medical appropriateness
5. **Overall Score**: Weighted combination

## ⚠️ Ethical Considerations

### Data Privacy
- No user data is logged or stored
- Privacy mode enabled by default
- Database contains only anonymized data

### Medical Safety
- System provides **descriptive analytics only**
- **No diagnoses** or treatment recommendations
- Appropriate disclaimers in responses
- Safety checks prevent inappropriate advice

### Model Training
- Uses publicly available models
- Fine-tuning data is domain-specific
- No proprietary data in training sets

## 🔮 Future Enhancements

1. **Multi-model Support**: Integration with other LLM providers
2. **Advanced Fine-tuning**: Domain-specific model training
3. **Query History**: Save and replay queries
4. **Visualization**: Automatic chart generation
5. **Multi-language Support**: Query in different languages
6. **Real-time Updates**: Live data integration
7. **Advanced Analytics**: Predictive modeling integration

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `.env` file exists with `OPENAI_API_KEY`
   - Check API key is valid and has credits

2. **Database Not Found**
   - Run `python data_generator.py` first
   - Then run `python data_preprocessing.py`

3. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

4. **Streamlit Issues**
   - Clear cache: `streamlit cache clear`
   - Restart the app

## 📝 License

This project is for educational and research purposes.

## 👥 Contributors

Developed as part of the Healthcare GenAI Analytics Challenge.

## 📧 Contact

For questions or issues, please refer to the project documentation.

---

**Disclaimer**: This system provides descriptive analytics only. It does not provide medical diagnoses or treatment recommendations. Always consult with healthcare professionals for medical advice.

