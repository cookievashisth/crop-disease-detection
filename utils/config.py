"""
Configuration - Application settings and constants
"""

import os
from pathlib import Path

# Application Info
APP_NAME = "Crop Yield Prediction System"
APP_VERSION = "1.0.0"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models_saved"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Data Settings
TARGET_COLUMN = 'Lint Yield (Pounds/Harvested Acre)'
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model Settings
MODEL_PARAMETERS = {
    'LinearRegression': {},
    'DecisionTree': {
        'random_state': 42,
        'max_depth': 10
    },
    'GradientBoosting': {
        'random_state': 42,
        'n_estimators': 100,
        'learning_rate': 0.1
    },
    'RandomForest': {
        'random_state': 42,
        'n_estimators': 100,
        'n_jobs': -1
    }
}

# Logging Settings
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class Config:
    """Configuration class for application settings"""
    APP_NAME = APP_NAME
    APP_VERSION = APP_VERSION
    BASE_DIR = BASE_DIR
    DATA_DIR = DATA_DIR
    MODELS_DIR = MODELS_DIR
    LOGS_DIR = LOGS_DIR
    TARGET_COLUMN = TARGET_COLUMN
    TEST_SIZE = TEST_SIZE
    RANDOM_STATE = RANDOM_STATE
    MODEL_PARAMETERS = MODEL_PARAMETERS
    LOG_LEVEL = LOG_LEVEL
    LOG_FORMAT = LOG_FORMAT

