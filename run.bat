@echo off
echo Starting Internet Security Checker...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Check if this is the first run after fixing dependencies
if not exist .deps_fixed (
    echo Updating dependencies to ensure compatibility...
    pip install -r requirements.txt
    type nul > .deps_fixed
)

:: Run the application
python app.py
