# Installation Guide

Comprehensive setup instructions for the Crop Yield Prediction System across different platforms.

## ⚡ Quick Start

### Windows Users

1. **Download and Install Python**
   - Visit https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - **IMPORTANT:** Check "Add Python to PATH" during installation

2. **Open Command Prompt**
   - Press `Win + R`
   - Type `cmd` and press Enter

3. **Navigate to Project Directory**
   ```cmd
   cd path\to\crop-disease-detection
   ```

4. **Run Setup**
   ```cmd
   setup.bat
   ```

5. **Launch Application**
   ```cmd
   run_app.bat
   ```

---

### macOS Users

1. **Install Python (if not installed)**
   ```bash
   brew install python3
   ```

2. **Clone Repository and Navigate**
   ```bash
   git clone https://github.com/cookievashisth/crop-disease-detection.git
   cd crop-disease-detection
   ```

3. **Make Scripts Executable**
   ```bash
   chmod +x setup.sh run_app.sh
   ```

4. **Run Setup**
   ```bash
   ./setup.sh
   ```

5. **Launch Application**
   ```bash
   ./run_app.sh
   ```

---

### Linux Users (Ubuntu/Debian)

1. **Install Python and Dependencies**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip python3-venv python3-tk python3-dev
   ```

2. **Clone Repository and Navigate**
   ```bash
   git clone https://github.com/cookievashisth/crop-disease-detection.git
   cd crop-disease-detection
   ```

3. **Make Scripts Executable**
   ```bash
   chmod +x setup.sh run_app.sh
   ```

4. **Run Setup**
   ```bash
   ./setup.sh
   ```

5. **Launch Application**
   ```bash
   ./run_app.sh
   ```

---

## 🔍 Detailed Manual Installation

If you prefer to install manually or automated scripts don't work:

### Step 1: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- pandas==2.0.3 - Data manipulation
- numpy==1.24.3 - Numerical computing
- scikit-learn==1.3.0 - Machine learning
- matplotlib==3.7.2 - Visualization
- python-dotenv==1.0.0 - Environment variables

### Step 4: Run Application

```bash
python main.py
```

---

## 🐛 Troubleshooting Installation

### Issue: "Python not found"

**Solution:** 
- Reinstall Python and ensure "Add Python to PATH" is checked
- Verify installation: `python --version` or `python3 --version`

### Issue: "ModuleNotFoundError: No module named 'tkinter'"

**Windows:** 
- Reinstall Python, ensure "tcl/tk and IDLE" is selected

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo yum install python3-tkinter
```

**macOS:**
```bash
brew install python-tk@3.9  # or your version
```

### Issue: "Permission denied" (on macOS/Linux)

**Solution:**
```bash
chmod +x setup.sh run_app.sh
./setup.sh
```

### Issue: Virtual environment activation fails

**Solution:** Delete venv folder and try again:
```bash
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
python -m venv venv
```

### Issue: Dependencies installation fails

**Solution:**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

### Issue: Application won't start

**Check logs:**
```bash
cat app.log  # macOS/Linux
type app.log  # Windows
```

---

## ✅ Verify Installation

After installation, verify everything works:

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.bat  # Windows

# Test imports
python -c "import pandas; import numpy; import sklearn; import matplotlib; print('All packages installed correctly!')"

# Start application
python main.py
```

---

## 🔄 Updating Dependencies

To update packages to latest versions:

```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.bat  # Windows

pip install --upgrade -r requirements.txt
```

---

## 🗑️ Uninstalling

To completely remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Remove project directory (if desired)
cd ..
rm -rf crop-disease-detection  # macOS/Linux
rmdir /s crop-disease-detection  # Windows
```

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Python | 3.8 | 3.9+ |
| RAM | 2GB | 4GB+ |
| Disk Space | 200MB | 500MB |
| OS | Windows 7+, macOS 10.9+, Linux | Windows 10+, macOS 10.15+, Linux (recent) |

---

## 🆘 Still Having Issues?

1. **Check Python version:**
   ```bash
   python --version
   ```
   Should be 3.8 or higher

2. **Verify virtual environment is active:**
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```
   Should show path inside `venv` folder

3. **Check installed packages:**
   ```bash
   pip list
   ```
   Should show all packages from requirements.txt

4. **Check application logs:**
   ```bash
   cat app.log  # macOS/Linux
   type app.log  # Windows
   ```

5. **Create a GitHub issue:**
   - Include OS and Python version
   - Share error messages
   - Describe steps to reproduce

---

## 📞 Support

For help with installation:
- GitHub Issues: https://github.com/cookievashisth/crop-disease-detection/issues
- Check existing issues first

---

**Last Updated:** 2024  
**Tested On:** Python 3.8, 3.9, 3.10, 3.11
