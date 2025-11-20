#!/bin/bash

# OMFGG - Run script

echo "🎮 Starting OMFGG..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.13 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Check if gradio is installed
if ! python -c "import gradio" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the app
echo "🚀 Launching app on http://localhost:7860"
python app.py
