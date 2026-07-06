"""
Yield Predictor - Machine Learning models for crop yield prediction
"""

import numpy as np
import pickle
import matplotlib.pyplot as plt
import time
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn import metrics
import logging

logger = logging.getLogger(__name__)


class YieldPredictor:
    def __init__(self):
        self.models = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.results = {}
        self.predictions = {}
        self.feature_names = None
        self.scaler = None
        
    def train_models(self, X_train, X_test, y_train, y_test, feature_names):
        """Train all ML models"""
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.feature_names = feature_names
        
        models_config = {
            'Linear Regression': LinearRegression(),
            'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=10),
            'Gradient Boosting': GradientBoostingRegressor(random_state=42, n_estimators=100),
            'Random Forest': RandomForestRegressor(random_state=42, n_estimators=100)
        }
        
        results = {}
        
        for name, model in models_config.items():
            try:
                logger.info(f"Training {name}...")
                
                start_time = time.time()
                model.fit(X_train, y_train)
                training_time = time.time() - start_time
                
                self.models[name] = model
                
                # Make predictions
                y_pred = model.predict(X_test)
                self.predictions[name] = y_pred
                
                # Calculate metrics
                r2 = metrics.r2_score(y_test, y_pred)
                rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
                mae = metrics.mean_absolute_error(y_test, y_pred)
                
                results[name] = {
                    'r2': r2,
                    'rmse': rmse,
                    'mae': mae,
                    'training_time': training_time
                }
                
                self.results[name] = results[name]
                
                logger.info(f"{name} - R²: {r2:.4f}, RMSE: {rmse:.4f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {str(e)}")
                results[name] = {'error': str(e)}
        
        return results
    
    def predict(self, features_dict, scaler):
        """Make prediction with new data"""
        if not self.models:
            raise ValueError("Models not trained yet")
        
        # Create feature vector in correct order
        feature_values = [features_dict.get(fname, 0) for fname in self.feature_names]
        X_new = np.array([feature_values])
        
        # Scale the features
        if scaler:
            X_new_scaled = scaler.transform(X_new)
        else:
            X_new_scaled = X_new
        
        predictions = {}
        for model_name, model in self.models.items():
            pred = model.predict(X_new_scaled)[0]
            predictions[model_name] = pred
        
        return predictions
    
    def plot_predictions(self):
        """Plot actual vs predicted values"""
        if not self.predictions:
            raise ValueError("No predictions available")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Actual vs Predicted Yield (Test Set)', fontsize=16, fontweight='bold')
        
        for idx, (model_name, y_pred) in enumerate(self.predictions.items()):
            ax = axes[idx // 2, idx % 2]
            
            ax.scatter(self.y_test, y_pred, alpha=0.6, s=50, edgecolors='k')
            
            # Add reference line
            min_val = min(self.y_test.min(), y_pred.min())
            max_val = max(self.y_test.max(), y_pred.max())
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
            
            ax.set_xlabel('Actual Yield', fontsize=10)
            ax.set_ylabel('Predicted Yield', fontsize=10)
            ax.set_title(f'{model_name}\nR² = {self.results[model_name]["r2"]:.4f}', 
                        fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_feature_importance(self):
        """Plot feature importance for tree-based models"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Feature Importance (Tree-Based Models)', fontsize=16, fontweight='bold')
        
        tree_models = {
            'Decision Tree': self.models.get('Decision Tree'),
            'Gradient Boosting': self.models.get('Gradient Boosting')
        }
        
        for idx, (model_name, model) in enumerate(tree_models.items()):
            if model and hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                indices = np.argsort(importances)[::-1][:10]  # Top 10
                
                axes[idx].barh(range(len(indices)), importances[indices], align='center')
                axes[idx].set_yticks(range(len(indices)))
                axes[idx].set_yticklabels([self.feature_names[i] for i in indices])
                axes[idx].set_xlabel('Importance', fontsize=10)
                axes[idx].set_title(model_name, fontweight='bold')
                axes[idx].invert_yaxis()
                axes[idx].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        return fig
    
    def plot_model_comparison(self):
        """Compare all models using metrics"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        
        model_names = list(self.results.keys())
        r2_scores = [self.results[m]['r2'] for m in model_names]
        rmse_scores = [self.results[m]['rmse'] for m in model_names]
        mae_scores = [self.results[m]['mae'] for m in model_names]
        
        # R² Score
        axes[0].bar(model_names, r2_scores, color='skyblue', edgecolor='black')
        axes[0].set_ylabel('R² Score', fontsize=10)
        axes[0].set_title('R² Score Comparison', fontweight='bold')
        axes[0].set_ylim(0, 1)
        axes[0].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(r2_scores):
            axes[0].text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold')
        
        # RMSE
        axes[1].bar(model_names, rmse_scores, color='lightcoral', edgecolor='black')
        axes[1].set_ylabel('RMSE', fontsize=10)
        axes[1].set_title('RMSE Comparison', fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(rmse_scores):
            axes[1].text(i, v + max(rmse_scores)*0.02, f'{v:.2f}', ha='center', fontweight='bold')
        
        # MAE
        axes[2].bar(model_names, mae_scores, color='lightgreen', edgecolor='black')
        axes[2].set_ylabel('MAE', fontsize=10)
        axes[2].set_title('MAE Comparison', fontweight='bold')
        axes[2].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(mae_scores):
            axes[2].text(i, v + max(mae_scores)*0.02, f'{v:.2f}', ha='center', fontweight='bold')
        
        plt.setp(axes, xticks=range(len(model_names)), xticklabels=model_names)
        plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def save_models(self, filepath):
        """Save trained models to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.models, f)
        logger.info(f"Models saved to {filepath}")
    
    def load_models(self, filepath):
        """Load trained models from disk"""
        with open(filepath, 'rb') as f:
            self.models = pickle.load(f)
        logger.info(f"Models loaded from {filepath}")
        
        models_config = {
            'Linear Regression': LinearRegression(),
            'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=10),
            'Gradient Boosting': GradientBoostingRegressor(random_state=42, n_estimators=100),
            'Random Forest': RandomForestRegressor(random_state=42, n_estimators=100)
        }
        
        results = {}
        
        for name, model in models_config.items():
            try:
                logger.info(f"Training {name}...")
                
                start_time = time.time()
                model.fit(X_train, y_train)
                training_time = time.time() - start_time
                
                self.models[name] = model
                
                # Make predictions
                y_pred = model.predict(X_test)
                self.predictions[name] = y_pred
                
                # Calculate metrics
                r2 = metrics.r2_score(y_test, y_pred)
                rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
                mae = metrics.mean_absolute_error(y_test, y_pred)
                
                results[name] = {
                    'r2': r2,
                    'rmse': rmse,
                    'mae': mae,
                    'training_time': training_time
                }
                
                self.results[name] = results[name]
                
                logger.info(f"{name} - R²: {r2:.4f}, RMSE: {rmse:.4f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {str(e)}")
                results[name] = {'error': str(e)}
        
        return results
    
    def predict(self, features_dict):
        """Make prediction with new data"""
        if not self.models:
            raise ValueError("Models not trained yet")
        
        # Create feature vector in correct order
        feature_values = [features_dict.get(fname, 0) for fname in self.feature_names]
        X_new = np.array([feature_values])
        
        predictions = {}
        for model_name, model in self.models.items():
            pred = model.predict(X_new)[0]
            predictions[model_name] = pred
        
        return predictions
    
    def plot_predictions(self):
        """Plot actual vs predicted values"""
        if not self.predictions:
            raise ValueError("No predictions available")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Actual vs Predicted Yield (Test Set)', fontsize=16, fontweight='bold')
        
        for idx, (model_name, y_pred) in enumerate(self.predictions.items()):
            ax = axes[idx // 2, idx % 2]
            
            ax.scatter(self.y_test, y_pred, alpha=0.6, s=50, edgecolors='k')
            
            # Add reference line
            min_val = min(self.y_test.min(), y_pred.min())
            max_val = max(self.y_test.max(), y_pred.max())
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
            
            ax.set_xlabel('Actual Yield', fontsize=10)
            ax.set_ylabel('Predicted Yield', fontsize=10)
            ax.set_title(f'{model_name}\nR² = {self.results[model_name]["r2"]:.4f}', 
                        fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_feature_importance(self):
        """Plot feature importance for tree-based models"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Feature Importance (Tree-Based Models)', fontsize=16, fontweight='bold')
        
        tree_models = {
            'Decision Tree': self.models.get('Decision Tree'),
            'Gradient Boosting': self.models.get('Gradient Boosting')
        }
        
        for idx, (model_name, model) in enumerate(tree_models.items()):
            if model and hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                indices = np.argsort(importances)[::-1][:10]  # Top 10
                
                axes[idx].barh(range(len(indices)), importances[indices], align='center')
                axes[idx].set_yticks(range(len(indices)))
                axes[idx].set_yticklabels([self.feature_names[i] for i in indices])
                axes[idx].set_xlabel('Importance', fontsize=10)
                axes[idx].set_title(model_name, fontweight='bold')
                axes[idx].invert_yaxis()
                axes[idx].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        return fig
    
    def plot_model_comparison(self):
        """Compare all models using metrics"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        
        model_names = list(self.results.keys())
        r2_scores = [self.results[m]['r2'] for m in model_names]
        rmse_scores = [self.results[m]['rmse'] for m in model_names]
        mae_scores = [self.results[m]['mae'] for m in model_names]
        
        # R² Score
        axes[0].bar(model_names, r2_scores, color='skyblue', edgecolor='black')
        axes[0].set_ylabel('R² Score', fontsize=10)
        axes[0].set_title('R² Score Comparison', fontweight='bold')
        axes[0].set_ylim(0, 1)
        axes[0].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(r2_scores):
            axes[0].text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold')
        
        # RMSE
        axes[1].bar(model_names, rmse_scores, color='lightcoral', edgecolor='black')
        axes[1].set_ylabel('RMSE', fontsize=10)
        axes[1].set_title('RMSE Comparison', fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(rmse_scores):
            axes[1].text(i, v + max(rmse_scores)*0.02, f'{v:.2f}', ha='center', fontweight='bold')
        
        # MAE
        axes[2].bar(model_names, mae_scores, color='lightgreen', edgecolor='black')
        axes[2].set_ylabel('MAE', fontsize=10)
        axes[2].set_title('MAE Comparison', fontweight='bold')
        axes[2].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(mae_scores):
            axes[2].text(i, v + max(mae_scores)*0.02, f'{v:.2f}', ha='center', fontweight='bold')
        
        plt.setp(axes, xticks=range(len(model_names)), xticklabels=model_names)
        plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def save_models(self, filepath):
        """Save trained models to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.models, f)
        logger.info(f"Models saved to {filepath}")
    
    def load_models(self, filepath):
        """Load trained models from disk"""
        with open(filepath, 'rb') as f:
            self.models = pickle.load(f)
        logger.info(f"Models loaded from {filepath}")
