import sys
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def load_data(path: str | None = None):
    base_path = Path(__file__).resolve().parent
    if path:
        file_path = Path(path)
        if file_path.exists():
            return pd.read_csv(file_path)
        raise FileNotFoundError(f'Dataset file not found: {file_path}')

    default_path = base_path / 'data' / 'sample_data.csv'
    fallback_path = base_path / 'dataset.csv'

    if default_path.exists():
        return pd.read_csv(default_path)
    if fallback_path.exists():
        return pd.read_csv(fallback_path)

    raise FileNotFoundError(
        'No dataset found. Place dataset.csv in the project root or use data/sample_data.csv.'
    )


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data = data.fillna(data.mean(numeric_only=True))
    if 'State' in data.columns:
        data = pd.get_dummies(data, columns=['State'])
    if 'Crop' in data.columns:
        data = pd.get_dummies(data, columns=['Crop'])
    return data


def train_and_evaluate(data: pd.DataFrame):
    target_column = 'Lint Yield (Pounds/Harvested Acre)'
    if target_column not in data.columns:
        raise ValueError(f'Target column not found: {target_column}')

    data = preprocess_data(data)
    data = data.dropna(subset=[target_column])

    X = data.drop(columns=[target_column])
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42)
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'r2': metrics.r2_score(y_test, y_pred),
            'rmse': np.sqrt(metrics.mean_squared_error(y_test, y_pred)),
            'predictions': y_pred
        }

    return y_test, results


def plot_results(y_test, gb_predictions):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, gb_predictions, color='green', alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('Actual Yield')
    plt.ylabel('Predicted Yield')
    plt.title('Actual vs Predicted Yield (Gradient Boosting)')
    plt.tight_layout()
    plt.savefig('predicted_vs_actual.png')
    print('Saved plot to predicted_vs_actual.png')


if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else None
    data = load_data(input_path)
    print('Loaded dataset with', len(data), 'rows and', len(data.columns), 'columns')
    print(data.head())

    y_test, results = train_and_evaluate(data)
    for name, metrics_data in results.items():
        print(f"{name} R^2: {metrics_data['r2']:.3f}")
        print(f"{name} RMSE: {metrics_data['rmse']:.3f}\n")

    plot_results(y_test, results['Gradient Boosting']['predictions'])

    if input_path:
        print(f"Used dataset: {input_path}")
    else:
        print('Used default dataset file.')

