# Deployment Guide

## GitHub Deployment

### Step 1: Initialize Git Repository

```bash
cd /home/dell/Music/infogain
git init
git add .
git commit -m "Initial commit: Healthcare GenAI Analytics System"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `healthcare-genai-analytics`)
3. **DO NOT** initialize with README (we already have one)

### Step 3: Push to GitHub

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/healthcare-genai-analytics.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Set Up Secrets (for GitHub Actions/Deployment)

If deploying to cloud platforms, add these secrets:
- `GROQ_API_KEY` or `OPENAI_API_KEY`
- `SQL_HOST`, `SQL_USER`, `SQL_PASSWORD`, etc. (if using SQL)

---

## Local Deployment

### Requirements
- Python 3.8+
- Virtual environment
- API key (Groq or OpenAI)

### Steps

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/healthcare-genai-analytics.git
cd healthcare-genai-analytics

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp ENV_EXAMPLE.txt .env
# Edit .env and add your API keys

# 5. Load data
python data_preprocessing.py

# 6. Run application
streamlit run app.py
```

---

## Cloud Deployment Options

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud settings:
   - `GROQ_API_KEY`
   - Other environment variables
5. Deploy!

### Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## Important Notes

⚠️ **Never commit:**
- `.env` file (contains API keys)
- `data/` folder (may contain sensitive data)
- `*.db` files
- Lock files

✅ **Always include:**
- `requirements.txt`
- `README.md`
- `ENV_EXAMPLE.txt` (template for .env)
- All Python source files

