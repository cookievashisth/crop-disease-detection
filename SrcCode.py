# 1. Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics  # for evaluation metrics
import matplotlib.pyplot as plt

# 2. Load the dataset
# Ensure you have the dataset file in the same directory or provide the correct path.
# The dataset should contain columns like 'Yield' (target) and features such as 'Rainfall', 'Area', etc.
data = pd.read_csv('dataset.csv')

# 3. Inspect the data (print first 5 rows to understand the structure)
print("Preview of dataset:")
print(data.head())

# 4. Preprocess the data
# (a) Handle missing values by filling with column mean
data = data.fillna(data.mean(numeric_only=True))
# (b) Encode categorical features if any (e.g., 'State' or 'Crop' columns)
# Here we assume 'State' and 'Crop' are categorical; we use one-hot encoding as an example.
if 'State' in data.columns:
    data = pd.get_dummies(data, columns=['State'])
if 'Crop' in data.columns:
    data = pd.get_dummies(data, columns=['Crop'])

# 5. Define feature matrix X and target variable y
# Assume the target column is named 'Yield'
# Define the target column based on your dataset
target_column = 'Lint Yield (Pounds/Harvested Acre)'

# Optionally, drop rows where the target is missing
data.dropna(subset=[target_column], inplace=True)

# Define feature matrix X and target variable y
X = data.drop([target_column], axis=1)
y = data[target_column]

# 6. Split the data into training and testing sets
# We use 80% of the data for training and 20% for testing.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# 7. Initialize the models
lr_model = LinearRegression()
dt_model = DecisionTreeRegressor(random_state=42)
gb_model = GradientBoostingRegressor(random_state=42)

# 8. Train the models on the training data
lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)
gb_model.fit(X_train, y_train)

# 9. Make predictions on the test set with each model
lr_predictions = lr_model.predict(X_test)
dt_predictions = dt_model.predict(X_test)
gb_predictions = gb_model.predict(X_test)

# 10. Evaluate the models using R^2 score and RMSE
lr_r2 = metrics.r2_score(y_test, lr_predictions)
dt_r2 = metrics.r2_score(y_test, dt_predictions)
gb_r2 = metrics.r2_score(y_test, gb_predictions)
print(f"Linear Regression R^2: {lr_r2:.3f}")
print(f"Decision Tree R^2: {dt_r2:.3f}")
print(f"Gradient Boosting R^2: {gb_r2:.3f}")

# Calculate RMSE for each model
lr_rmse = np.sqrt(metrics.mean_squared_error(y_test, lr_predictions))
dt_rmse = np.sqrt(metrics.mean_squared_error(y_test, dt_predictions))
gb_rmse = np.sqrt(metrics.mean_squared_error(y_test, gb_predictions))
print(f"Linear Regression RMSE: {lr_rmse:.3f}")
print(f"Decision Tree RMSE: {dt_rmse:.3f}")
print(f"Gradient Boosting RMSE: {gb_rmse:.3f}")

# 11. Plot actual vs predicted yields for the best model (Gradient Boosting) for visualization
plt.figure(figsize=(6,4))
plt.scatter(y_test, gb_predictions, color='green', alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # line y=x for reference
plt.xlabel('Actual Yield')
plt.ylabel('Predicted Yield')
plt.title('Actual vs Predicted Yield (Gradient Boosting)')
plt.savefig('predicted_vs_actual.png')

