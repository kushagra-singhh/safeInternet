#!/bin/bash
echo "Starting Internet Security Checker..."

# Activate virtual environment
source venv/bin/activate

# Check if this is the first run after fixing dependencies
if [ ! -f .deps_fixed ]; then
    echo "Updating dependencies to ensure compatibility..."
    pip install -r requirements.txt
    touch .deps_fixed
fi

# Run the application
python app.py
