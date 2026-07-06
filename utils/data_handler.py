"""
Data Handler - Utilities for data preprocessing and preparation
"""

import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)


class DataHandler:
    def __init__(self):
        self.dataset_path = None
        self.original_data = None
        self.processed_data = None
        self.target_column = 'Lint Yield (Pounds/Harvested Acre)'
        self.column_names = []
        self.scaler = None
    
    def load_data(self, filepath):
        """Load data from CSV file"""
        try:
            self.dataset_path = filepath
            data = self._read_csv(filepath)
            self.original_data = data
            logger.info(f"Data loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _read_csv(self, filepath):
        """Read CSV file into dict of lists"""
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            raise ValueError("CSV file is empty")
        
        # Get column names
        self.column_names = list(rows[0].keys())
        
        # Convert to dict of lists with numeric values
        data = {col: [] for col in self.column_names}
        for row in rows:
            for col in self.column_names:
                try:
                    data[col].append(float(row[col]))
                except ValueError:
                    data[col].append(None)
        
        return data
    
    def preprocess_data(self, data):
        """Preprocess the dataset"""
        self.processed_data = {}
        
        for col, values in data.items():
            # Handle missing values by filling with mean
            numeric_vals = [v for v in values if v is not None]
            if numeric_vals:
                mean_val = sum(numeric_vals) / len(numeric_vals)
                processed_vals = [v if v is not None else mean_val for v in values]
            else:
                processed_vals = values
            
            self.processed_data[col] = processed_vals
        
        logger.info("Data preprocessing completed")
        return self.processed_data
    
    def prepare_data(self, data, test_split=0.2, random_state=42):
        """Prepare data for model training"""
        try:
            # Accept pandas DataFrame or dict of lists
            if hasattr(data, 'columns') and hasattr(data, 'to_dict'):
                data = {col: data[col].tolist() for col in data.columns}

            # Preprocess
            processed = self.preprocess_data(data)
            
            # Check if target column exists
            if self.target_column not in processed:
                # Try to find similar column name
                target_candidates = [col for col in processed.keys() if 'yield' in col.lower()]
                if target_candidates:
                    self.target_column = target_candidates[0]
                    logger.warning(f"Target column not found, using {self.target_column}")
                else:
                    raise ValueError(f"Target column '{self.target_column}' not found in dataset")
            
            # Extract target
            y = np.array(processed[self.target_column])
            
            # Extract features (all columns except target)
            feature_cols = [col for col in processed.keys() if col != self.target_column]
            X = np.column_stack([processed[col] for col in feature_cols])
            
            logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_split, random_state=random_state
            )
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            logger.info(f"Data split: Train={len(X_train_scaled)}, Test={len(X_test_scaled)}")
            
            # Store feature columns for later use
            self.feature_columns = feature_cols
            
            return X_train_scaled, X_test_scaled, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise
    
    def validate_data(self, data):
        """Validate data quality"""
        issues = []
        
        # Check for empty data
        if not data:
            issues.append("Dataset is empty")
            return issues
        
        # Check for all missing values in a column
        for col, values in data.items():
            numeric_vals = [v for v in values if v is not None]
            if not numeric_vals:
                issues.append(f"Column '{col}' has all missing values")
        
        # Check for sufficient features
        numeric_cols = len([col for col in data.keys() if col != self.target_column])
        if numeric_cols < 2:
            issues.append("Insufficient numeric features for modeling")
        
        return issues
    
    def get_statistics(self, data):
        """Get descriptive statistics"""
        stats = {}
        for col, values in data.items():
            numeric_vals = [v for v in values if v is not None]
            if numeric_vals:
                stats[col] = {
                    'min': min(numeric_vals),
                    'max': max(numeric_vals),
                    'mean': sum(numeric_vals) / len(numeric_vals),
                    'count': len(numeric_vals)
                }
        return stats

