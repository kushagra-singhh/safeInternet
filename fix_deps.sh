#!/bin/bash
echo "Fixing dependencies for Internet Security Checker..."

# Activate virtual environment
source venv/bin/activate

# Clean up any old conflicting packages
pip uninstall -y flask werkzeug

# Install the correct versions
pip install -r requirements.txt

echo "Dependencies fixed! You can now run the application with ./run.sh"
