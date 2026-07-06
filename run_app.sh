#!/bin/bash

# Crop Yield Prediction System - Application Launcher

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py

# If there's an error, show it
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Application failed to start"
    echo "Check the error messages above"
    exit 1
fi
