# Fixing the Werkzeug/Flask Compatibility Issue

You encountered an error that says:
```
ImportError: cannot import name 'url_quote' from 'werkzeug.urls'
```

This is a known compatibility issue between Flask and Werkzeug versions. Here's how to fix it:

## Quick Fix

### For Linux/Mac:
```bash
# Run the dependency fix script
./fix_deps.sh

# Then start the application
./run.sh
```

### For Windows:
```cmd
# Run the dependency fix script
fix_deps.bat

# Then start the application
run.bat
```

## What's Happening?

1. The error occurs because newer versions of Werkzeug removed or renamed the `url_quote` function
2. Flask 2.2.3 requires Werkzeug 2.2.3 specifically to work correctly
3. Our fix script:
   - Uninstalls the current Flask and Werkzeug packages
   - Reinstalls them with pinned compatible versions from requirements.txt

## Manual Fix

If the scripts don't work, you can fix this manually:

1. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate.bat  # Windows
   ```

2. Uninstall the incompatible packages:
   ```bash
   pip uninstall -y flask werkzeug
   ```

3. Install compatible versions:
   ```bash
   pip install flask==2.2.3 werkzeug==2.2.3
   ```

4. Restart the application:
   ```bash
   python app.py
   ```

## Prevention

We've updated the requirements.txt file to include specific compatible versions and modified the run scripts to check and update dependencies automatically. This should prevent the issue from occurring in the future.
