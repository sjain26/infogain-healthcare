#!/bin/bash

# Setup script for Healthcare GenAI Analytics System

echo "=========================================="
echo "Healthcare GenAI Analytics - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data
mkdir -p reports
mkdir -p reports/figures
mkdir -p training_data
mkdir -p scripts

# Generate datasets
echo ""
echo "Generating sample datasets..."
python data_generator.py

# Setup database
echo ""
echo "Setting up database..."
python data_preprocessing.py

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "MODEL_NAME=gpt-3.5-turbo" >> .env
    echo ""
    echo "⚠️  Please edit .env file and add your OpenAI API key!"
fi

# Run data audit (optional)
read -p "Run data audit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running data audit..."
    python data_audit.py
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OPENAI_API_KEY"
echo "2. Run the web interface: streamlit run app.py"
echo "3. Or run in CLI mode: python run_pipeline.py --interactive"
echo ""

