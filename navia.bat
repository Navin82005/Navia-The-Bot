@echo off
setlocal EnableDelayedExpansion

REM ===== Navia AI Setup Script (Windows) =====
echo.
echo Setting up Navia AI environment on Windows...
echo.

REM 1. Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM 2. Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM 3. Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM 4. Run setup wizard
echo Launching setup wizard...
python setup.py

REM 5. Start the server
echo.
echo 🚀 Starting Navia AI server...
python run.py

pause
