# 🌾 Crop Disease Detection using Gradient Boosting and Decision Trees

A machine learning-based project that predicts crop yield variations caused by plant diseases using ensemble models. Designed to support early diagnosis and smarter decision-making in agriculture.

## 📌 Overview

This project explores the effectiveness of different supervised regression models—**Linear Regression**, **Decision Tree Regressor**, and **Gradient Boosting Regressor**—to predict crop yield as an indirect measure of disease impact.

Gradient Boosting achieved the highest performance with an R² score of **0.84**, indicating its suitability for complex agricultural datasets.

---

## 🧠 Models Implemented

- ✅ Linear Regression *(Baseline)*
- ✅ Decision Tree Regressor
- ✅ Gradient Boosting Regressor *(Best Performer)*

---

## 📊 Evaluation Metrics

| Model                  | R² Score | RMSE  |
|------------------------|----------|--------|
| Linear Regression      | 0.65     | 45.2   |
| Decision Tree Regressor| 0.72     | 38.9   |
| Gradient Boosting      | 0.84     | 28.5   |

---

## 📁 Dataset Features

- **Input features**: Rainfall, Area, Crop Type, State, etc.
- **Target variable**: Lint Yield (Pounds/Harvested Acre)
- Categorical columns were one-hot encoded.
- Missing values handled using mean imputation.

---

## 📦 Tech Stack

- **Python**
- **scikit-learn**
- **pandas**
- **matplotlib**
- **NumPy**

---

## 📈 Visualization

The model includes a plot comparing actual vs. predicted yields using Gradient Boosting.

---

## 📄 How to Run

1. Clone the repo  
   ```bash
   git clone https://github.com/Ujjwal-44/crop-disease-detection.git
   cd crop-disease-detection
pip install -r requirements.txt
python crop_disease_model.py

