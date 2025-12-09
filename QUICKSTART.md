# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment

```bash
# Run the setup script
bash setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure API Key

Edit `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
MODEL_NAME=gpt-3.5-turbo
```

### Step 3: Generate Data

```bash
python data_generator.py
```

This creates:
- `data/health_dataset_1.csv` (2000 records)
- `data/health_dataset_2.csv` (20000 records)

### Step 4: Setup Database

```bash
python data_preprocessing.py
```

This creates:
- `data/healthcare.db` (SQLite database)

### Step 5: Launch Web Interface

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

## 📝 Example Queries

Try these queries in the web interface:

1. **Simple Count**
   ```
   How many patients have abnormal blood pressure?
   ```

2. **Average Calculation**
   ```
   What is the average age of patients with chronic kidney disease?
   ```

3. **Filtering**
   ```
   Show me patients above 60 years with BMI over 30
   ```

4. **Join Query**
   ```
   What is the average physical activity for patients with high stress?
   ```

5. **Complex Query**
   ```
   Find patients who smoke and have abnormal blood pressure
   ```

## 🔧 Alternative Usage

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

pipeline = HealthcareGenAI()
result = pipeline.process_query("Your query here")
print(result['insights'])
```

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Make sure `.env` file exists and contains your API key

### Issue: "Dataset file not found"
**Solution**: Run `python data_generator.py` first

### Issue: "Database not found"
**Solution**: Run `python data_preprocessing.py` after generating data

### Issue: Import errors
**Solution**: 
```bash
pip install -r requirements.txt
```

## 📊 Optional: Run Data Audit

```bash
python data_audit.py
```

This generates:
- `reports/data_audit_report.txt`
- `reports/figures/data_distributions.png`

## ✅ Verification

To verify everything works:

```bash
python run_pipeline.py --query "How many patients are in the database?"
```

You should see:
- SQL query generated
- Results returned
- Insights generated

## 🎯 Next Steps

1. Explore the web interface
2. Try different queries
3. Review evaluation metrics
4. Check the comprehensive README.md for advanced usage

---

**Need Help?** Check the main README.md for detailed documentation.

