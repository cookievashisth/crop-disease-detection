@echo off
REM Crop Yield Prediction System - Application Launcher

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
python main.py

REM If there's an error, show it
if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    pause
)
