#!/bin/bash

# Crop Yield Prediction System - Unix/Linux/macOS Setup Script

echo ""
echo "========================================"
echo "Crop Yield Prediction System - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    exit 1
fi

echo "[1/4] Python found: $(python3 --version)"

# Check for tkinter on Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo ""
        echo "WARNING: Tkinter not found"
        echo "Installing tkinter..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-tk python3-dev
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-tkinter python3-devel
        fi
    fi
fi

# Create virtual environment
echo ""
echo "[2/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo ""
echo "[4/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run: python main.py"
echo ""
echo "Or use the run script: ./run_app.sh"
echo ""
