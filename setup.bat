@echo off
echo Setting up Internet Security Checker...

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Copying .env.example to .env...
copy .env.example .env

echo Setup complete!
echo.
echo To start the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the application: python app.py
echo.
echo The application will be available at http://localhost:5000

pause
