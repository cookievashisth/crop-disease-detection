"""
Crop Yield Prediction Desktop Application
A professional desktop application for predicting crop yields using machine learning
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import json
import os
from pathlib import Path
from datetime import datetime
import logging

from models.yield_predictor import YieldPredictor
from utils.data_handler import DataHandler
from utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CropYieldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crop Yield Prediction System")
        self.root.geometry("1400x800")
        self.root.minsize(1000, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.predictor = YieldPredictor()
        self.data_handler = DataHandler()
        self.current_data = None
        self.models_trained = False
        
        self.setup_ui()
        self.load_previous_session()
        logger.info("Application started successfully")

    def setup_ui(self):
        """Setup the main user interface"""
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.data_tab = ttk.Frame(self.notebook)
        self.training_tab = ttk.Frame(self.notebook)
        self.prediction_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.data_tab, text="Data Management")
        self.notebook.add(self.training_tab, text="Model Training")
        self.notebook.add(self.prediction_tab, text="Predictions")
        self.notebook.add(self.analysis_tab, text="Analysis")
        
        self.setup_data_tab()
        self.setup_training_tab()
        self.setup_prediction_tab()
        self.setup_analysis_tab()

    def setup_data_tab(self):
        """Setup data management tab"""
        frame = ttk.LabelFrame(self.data_tab, text="Dataset Management", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Load CSV Dataset", 
                  command=self.load_dataset).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load Sample Dataset", 
                  command=self.load_sample_dataset).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Data", 
                  command=self.view_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Data Statistics", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(frame, text="Dataset Info", padding=10)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.data_status_text = tk.Text(status_frame, height=10, width=80)
        self.data_status_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, 
                                 command=self.data_status_text.yview)
        self.data_status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_training_tab(self):
        """Setup model training tab"""
        frame = ttk.LabelFrame(self.training_tab, text="Model Training", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control frame
        ctrl_frame = ttk.LabelFrame(frame, text="Training Configuration", padding=10)
        ctrl_frame.pack(fill=tk.X, pady=10)
        
        # Test split
        ttk.Label(ctrl_frame, text="Test Split (%):", width=15).pack(side=tk.LEFT, padx=5)
        self.test_split_var = tk.DoubleVar(value=20.0)
        ttk.Spinbox(ctrl_frame, from_=5, to=50, textvariable=self.test_split_var, 
                   width=10).pack(side=tk.LEFT, padx=5)
        
        # Random state
        ttk.Label(ctrl_frame, text="Random State:", width=15).pack(side=tk.LEFT, padx=5)
        self.random_state_var = tk.IntVar(value=42)
        ttk.Spinbox(ctrl_frame, from_=0, to=1000, textvariable=self.random_state_var, 
                   width=10).pack(side=tk.LEFT, padx=5)
        
        # Training button
        ttk.Button(ctrl_frame, text="Train All Models", 
                  command=self.start_training).pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(frame, text="Training Progress", padding=10)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to train...")
        self.progress_label.pack(fill=tk.X)
        
        # Results frame
        results_frame = ttk.LabelFrame(frame, text="Model Performance", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_text = tk.Text(results_frame, height=15, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                 command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_prediction_tab(self):
        """Setup prediction tab"""
        frame = ttk.LabelFrame(self.prediction_tab, text="Make Predictions", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Feature input frame
        input_frame = ttk.LabelFrame(frame, text="Input Features", padding=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        self.feature_inputs = {}
        
        # Prediction button
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Predict", 
                  command=self.make_prediction).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", 
                  command=self.clear_prediction).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(frame, text="Prediction Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.prediction_result_text = tk.Text(results_frame, height=15, width=80)
        self.prediction_result_text.pack(fill=tk.BOTH, expand=True)

    def setup_analysis_tab(self):
        """Setup analysis tab"""
        frame = ttk.LabelFrame(self.analysis_tab, text="Model Analysis", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Plot Predictions", 
                  command=self.plot_predictions).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Feature Importance", 
                  command=self.plot_feature_importance).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Model Comparison", 
                  command=self.plot_model_comparison).pack(side=tk.LEFT, padx=5)
        
        # Canvas frame for plots
        self.canvas_frame = ttk.LabelFrame(frame, text="Visualization", padding=10)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def load_dataset(self):
        """Load dataset from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.current_data = self.data_handler.load_data(file_path)
                self.update_data_status()
                messagebox.showinfo("Success", f"Dataset loaded successfully!\nRows: {len(self.current_data.get(list(self.current_data.keys())[0], []))}")
                logger.info(f"Dataset loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")
                logger.error(f"Error loading dataset: {str(e)}")

    def load_sample_dataset(self):
        """Load sample dataset"""
        try:
            sample_path = Path(__file__).parent / "data" / "sample_data.csv"
            if sample_path.exists():
                self.current_data = self.data_handler.load_data(str(sample_path))
                self.update_data_status()
                num_rows = len(self.current_data.get(list(self.current_data.keys())[0], []))
                messagebox.showinfo("Success", f"Sample dataset loaded!\nRows: {num_rows}")
                logger.info("Sample dataset loaded")
            else:
                messagebox.showwarning("Warning", "Sample dataset not found. Please load a CSV file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sample dataset: {str(e)}")
            logger.error(f"Error loading sample dataset: {str(e)}")

    def update_data_status(self):
        """Update data status display"""
        if self.current_data is not None:
            num_rows = len(self.current_data.get(list(self.current_data.keys())[0], []))
            num_cols = len(self.current_data)
            
            status = f"Dataset Information:\n"
            status += f"{'='*50}\n"
            status += f"Rows: {num_rows}\n"
            status += f"Columns: {num_cols}\n"
            status += f"\nColumn Names:\n"
            for i, col in enumerate(self.current_data.keys(), 1):
                status += f"  {i}. {col}\n"
            
            # Calculate statistics
            status += f"\nBasic Statistics:\n"
            for col in list(self.current_data.keys())[:min(5, num_cols)]:
                values = [v for v in self.current_data[col] if v is not None]
                if values:
                    status += f"  {col}: min={min(values):.2f}, max={max(values):.2f}, mean={sum(values)/len(values):.2f}\n"
            
            self.data_status_text.config(state=tk.NORMAL)
            self.data_status_text.delete(1.0, tk.END)
            self.data_status_text.insert(1.0, status)
            self.data_status_text.config(state=tk.DISABLED)

    def view_data(self):
        """Show data in new window"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No dataset loaded")
            return
        
        view_window = tk.Toplevel(self.root)
        view_window.title("Dataset Preview")
        view_window.geometry("900x600")
        
        text_widget = tk.Text(view_window)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Format data for display
        cols = list(self.current_data.keys())
        num_rows = len(self.current_data[cols[0]])
        
        data_str = "\t".join(cols) + "\n"
        data_str += "-" * 80 + "\n"
        
        for i in range(min(num_rows, 100)):  # Show first 100 rows
            row_vals = []
            for col in cols:
                val = self.current_data[col][i]
                row_vals.append(f"{val:.2f}" if isinstance(val, (int, float)) else str(val))
            data_str += "\t".join(row_vals) + "\n"
        
        if num_rows > 100:
            data_str += f"\n... ({num_rows - 100} more rows)\n"
        
        text_widget.insert(1.0, data_str)
        text_widget.config(state=tk.DISABLED)

    def show_statistics(self):
        """Show dataset statistics"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "No dataset loaded")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Dataset Statistics")
        stats_window.geometry("900x600")
        
        text_widget = tk.Text(stats_window)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        stats = self.data_handler.get_statistics(self.current_data)
        
        stats_str = "DATASET STATISTICS\n"
        stats_str += "=" * 70 + "\n\n"
        
        for col, col_stats in stats.items():
            stats_str += f"{col}:\n"
            for key, val in col_stats.items():
                stats_str += f"  {key}: {val:.4f}\n"
            stats_str += "\n"
        
        text_widget.insert(1.0, stats_str)
        text_widget.config(state=tk.DISABLED)

    def start_training(self):
        """Start model training in background thread"""
        if self.current_data is None:
            messagebox.showwarning("Warning", "Please load a dataset first")
            return
        
        thread = threading.Thread(target=self.train_models)
        thread.daemon = True
        thread.start()

    def train_models(self):
        """Train all models"""
        try:
            self.progress_label.config(text="Preprocessing data...")
            self.progress_var.set(0)
            self.root.update()
            
            # Prepare data
            test_split = self.test_split_var.get() / 100
            random_state = self.random_state_var.get()
            
            X_train, X_test, y_train, y_test = self.data_handler.prepare_data(
                self.current_data, test_split, random_state
            )
            
            self.progress_var.set(20)
            self.progress_label.config(text="Training models...")
            self.root.update()
            
            # Train models
            results = self.predictor.train_models(X_train, X_test, y_train, y_test, 
                                                 self.data_handler.feature_columns)
            
            self.progress_var.set(100)
            self.progress_label.config(text="Training completed!")
            self.models_trained = True
            
            # Display results
            self.display_results(results)
            logger.info("Models trained successfully")
            messagebox.showinfo("Success", "All models trained successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")
            logger.error(f"Error during training: {str(e)}")
            self.progress_label.config(text="Training failed!")

    def display_results(self, results):
        """Display training results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        results_str = "MODEL TRAINING RESULTS\n"
        results_str += "=" * 70 + "\n\n"
        
        for model_name, metrics in results.items():
            results_str += f"{model_name.upper()}\n"
            results_str += "-" * 70 + "\n"
            results_str += f"  R² Score: {metrics['r2']:.4f}\n"
            results_str += f"  RMSE: {metrics['rmse']:.4f}\n"
            results_str += f"  MAE: {metrics['mae']:.4f}\n"
            results_str += f"  Training Time: {metrics['training_time']:.4f} seconds\n"
            results_str += "\n"
        
        self.results_text.insert(1.0, results_str)
        self.results_text.config(state=tk.DISABLED)

    def make_prediction(self):
        """Make prediction with input values"""
        if not self.models_trained:
            messagebox.showwarning("Warning", "Please train models first")
            return
        
        try:
            prediction_window = tk.Toplevel(self.root)
            prediction_window.title("Prediction Input")
            prediction_window.geometry("400x500")
            
            frame = ttk.Frame(prediction_window, padding=10)
            frame.pack(fill=tk.BOTH, expand=True)
            
            if self.current_data is None:
                messagebox.showwarning("Warning", "No dataset loaded")
                return
            
            # Get feature columns
            features = self.data_handler.feature_columns if hasattr(self.data_handler, 'feature_columns') else []
            
            inputs = {}
            for i, feature in enumerate(features):
                ttk.Label(frame, text=f"{feature}:").grid(row=i, column=0, sticky=tk.W, pady=5)
                entry = ttk.Entry(frame, width=20)
                entry.grid(row=i, column=1, sticky=tk.EW, pady=5)
                inputs[feature] = entry
            
            def predict():
                try:
                    values = {}
                    for feature in features:
                        values[feature] = float(inputs[feature].get())
                    
                    result = self.predictor.predict(values, self.data_handler.scaler)
                    
                    self.prediction_result_text.config(state=tk.NORMAL)
                    self.prediction_result_text.delete(1.0, tk.END)
                    
                    pred_str = "PREDICTION RESULTS\n"
                    pred_str += "=" * 50 + "\n\n"
                    
                    for model_name, pred_value in result.items():
                        pred_str += f"{model_name}: {pred_value:.2f} Pounds/Harvested Acre\n"
                    
                    self.prediction_result_text.insert(1.0, pred_str)
                    self.prediction_result_text.config(state=tk.DISABLED)
                    
                    messagebox.showinfo("Prediction", "Prediction completed!")
                    prediction_window.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers")
            
            ttk.Button(frame, text="Predict", command=predict).grid(row=len(features), 
                                                                     column=0, columnspan=2, 
                                                                     pady=20, sticky=tk.EW)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create prediction dialog: {str(e)}")

    def clear_prediction(self):
        """Clear prediction results"""
        self.prediction_result_text.config(state=tk.NORMAL)
        self.prediction_result_text.delete(1.0, tk.END)
        self.prediction_result_text.config(state=tk.DISABLED)

    def plot_predictions(self):
        """Plot actual vs predicted values"""
        if not self.models_trained:
            messagebox.showwarning("Warning", "Please train models first")
            return
        
        try:
            # Clear previous plots
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig = self.predictor.plot_predictions()
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create plot: {str(e)}")

    def plot_feature_importance(self):
        """Plot feature importance"""
        if not self.models_trained:
            messagebox.showwarning("Warning", "Please train models first")
            return
        
        try:
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig = self.predictor.plot_feature_importance()
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create plot: {str(e)}")

    def plot_model_comparison(self):
        """Plot model comparison"""
        if not self.models_trained:
            messagebox.showwarning("Warning", "Please train models first")
            return
        
        try:
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            fig = self.predictor.plot_model_comparison()
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create plot: {str(e)}")

    def load_previous_session(self):
        """Load previous session data"""
        try:
            if os.path.exists("session.json"):
                with open("session.json", "r") as f:
                    session = json.load(f)
                    last_dataset = session.get("last_dataset", "")
                    if os.path.exists(last_dataset):
                        self.current_data = pd.read_csv(last_dataset)
                        self.data_handler.dataset_path = last_dataset
                        self.update_data_status()
                        logger.info("Previous session loaded")
        except Exception as e:
            logger.warning(f"Could not load previous session: {str(e)}")

    def save_session(self):
        """Save current session"""
        try:
            if self.current_data is not None and self.data_handler.dataset_path:
                session = {
                    "last_dataset": self.data_handler.dataset_path,
                    "timestamp": datetime.now().isoformat()
                }
                with open("session.json", "w") as f:
                    json.dump(session, f)
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")

    def on_closing(self):
        """Handle application closing"""
        self.save_session()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CropYieldApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
