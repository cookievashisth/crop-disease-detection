@echo off
REM Crop Yield Prediction System - Windows Setup Script

echo.
echo ========================================
echo Crop Yield Prediction System - Setup
echo ========================================
echo.

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version

REM Create virtual environment
echo.
echo [2/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip first
echo.
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: pip upgrade had issues, continuing anyway...
)

REM Install dependencies
echo.
echo [4/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the application:
echo   1. Run: run_app.bat
echo      OR
echo   2. Activate venv: venv\Scripts\activate.bat
echo   3. Run: python main.py
echo.
pause
