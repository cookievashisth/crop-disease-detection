# Quick Reference Guide

## Running the Application

### Windows
```bash
setup.bat       # Install once
run_app.bat     # Run application
```

### macOS/Linux
```bash
chmod +x setup.sh && ./setup.sh    # Install once
./run_app.sh                        # Run application
```

### Direct Python
```bash
pip install -r requirements.txt
python main.py
```

---

## Application Tabs

### 1. Data Management
- **Load CSV Dataset** - Upload your own data
- **Load Sample Dataset** - Try with included example (46 rows)
- **View Data** - See all rows and columns
- **Data Statistics** - Min, max, mean, count per column

### 2. Model Training
- **Test Split %** - Adjust train/test ratio (default 20%)
- **Random State** - For reproducible results
- **Train All Models** - Trains: Linear Regression, Decision Tree, Gradient Boosting, Random Forest
- Progress bar shows training status

### 3. Predictions
- **Input Features** - Enter values for each crop parameter
- **Predict** - Get predictions from all 4 models
- **Clear** - Reset results

### 4. Analysis
- **Plot Predictions** - Scatter plot of actual vs predicted
- **Feature Importance** - Bar chart of most important features
- **Model Comparison** - Side-by-side performance metrics

---

## Sample Data Format

```csv
Rainfall,Area,Temperature,Humidity,Nitrogen,Phosphorus,Potassium,Lint Yield (Pounds/Harvested Acre)
850,120,28.5,65,80,40,50,850
720,100,27.2,62,75,35,45,780
950,140,29.1,68,90,50,60,920
```

**Important:**
- First row = column names
- All values must be numeric
- Target column: "Lint Yield (Pounds/Harvested Acre)"
- Minimum 20 rows recommended

---

## Model Performance Indicators

| Metric | What It Means | Good Range |
|--------|---------------|-----------|
| **R² Score** | Accuracy (0-1) | 0.8+ is excellent |
| **RMSE** | Prediction error | Lower is better |
| **MAE** | Average error | Lower is better |

---

## Sample Results (with included data)

```
Model                R² Score    RMSE    MAE
─────────────────────────────────────────────
Linear Regression    0.9899      11.43   8.93
Decision Tree        0.9861      13.42   11.00
Gradient Boosting    0.9964      6.84    5.99  ← Best
Random Forest        0.9905      11.08   9.22
```

---

## Common Tasks

### Load and Train
1. Click "Load Sample Dataset" (Data Management tab)
2. Go to "Model Training" tab
3. Click "Train All Models"
4. Wait 2-3 seconds for training

### Make a Prediction
1. Complete training (see above)
2. Go to "Predictions" tab
3. Enter all feature values
4. Click "Predict"
5. View results for all 4 models

### Analyze Performance
1. After training, go to "Analysis" tab
2. Click visualization buttons to see charts
3. Compare models and identify best performer

### Load Your Data
1. Prepare CSV file in correct format
2. Go to "Data Management" tab
3. Click "Load CSV Dataset"
4. Select your file
5. Continue with training

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Switch between UI elements |
| Enter | Activate buttons |
| Ctrl+C | Stop application (in terminal) |

---

## File Locations

| File | Purpose |
|------|---------|
| `main.py` | Main application |
| `data/sample_data.csv` | Sample data for testing |
| `app.log` | Application logs |
| `session.json` | Last session info (auto-saved) |

---

## Troubleshooting

**Q: Application won't start**
- Check Python version: `python --version` (need 3.8+)
- Try: `python main.py` in terminal to see error

**Q: "No module named" error**
- Run: `pip install -r requirements.txt`

**Q: Data won't load**
- Check CSV format is correct
- Verify all columns are numeric
- Check target column name is exact

**Q: Models not training**
- Need at least 20 rows of data
- All values must be valid numbers
- Check CSV file format

**Q: Application is slow**
- Normal for large datasets (1000+ rows)
- Close other applications
- Try with smaller dataset first

---

## Getting Help

1. **Check logs:** Open `app.log` in text editor
2. **Read docs:** See [README.md](README.md)
3. **Try sample:** Use "Load Sample Dataset" to test
4. **Manual install:** Run setup script again

---

## Tips for Best Results

✅ **Good Data**
- Clean, consistent formatting
- No missing values in important columns
- Reasonable number of rows (50+)
- Relevant features for prediction

✅ **Good Predictions**
- Use trained models on similar data
- Check R² score first
- Gradient Boosting often works best
- Compare all 4 models

✅ **Best Practice**
- Save your work regularly
- Test with sample data first
- Keep CSV files organized
- Review logs if issues occur

---

## Performance Expectations

- **Data load:** <1 second
- **Model train:** 2-5 seconds
- **Prediction:** <100ms
- **Visualization:** 1-2 seconds
- **File size:** Up to 100MB OK

---

## Version Information

- **Version:** 1.0.0
- **Status:** Production Ready
- **Python:** 3.8+
- **Platform:** Windows, macOS, Linux
- **Last Updated:** 2024

---

## Contact & Support

For issues or questions:
1. Check [INSTALLATION.md](INSTALLATION.md)
2. Review [README.md](README.md)
3. Check `app.log` for errors
4. Try sample data first

---

Good luck with your crop yield predictions! 🌾
