import os
import pickle
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
import structlog

logger = structlog.get_logger()

class ModelService:
    """Service for managing ML models"""
    
    def __init__(self):
        self.loaded_models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_store_path = os.getenv("MODEL_STORE_PATH", "/app/models")
        
    async def initialize(self):
        """Initialize the model service and load default models"""
        logger.info("Initializing ModelService...")
        
        # Create model store directory if it doesn't exist
        os.makedirs(self.model_store_path, exist_ok=True)
        
        # Load or create default models
        await self._load_or_create_models()
        
        logger.info("ModelService initialized", models_loaded=len(self.loaded_models))
    
    async def _load_or_create_models(self):
        """Load existing models or create new ones with dummy data"""
        
        # Credit Risk Model
        credit_model_path = os.path.join(self.model_store_path, "credit_risk_model.pkl")
        if os.path.exists(credit_model_path):
            self.loaded_models["credit_risk"] = joblib.load(credit_model_path)
            logger.info("Loaded existing credit risk model")
        else:
            self.loaded_models["credit_risk"] = self._create_dummy_credit_model()
            joblib.dump(self.loaded_models["credit_risk"], credit_model_path)
            logger.info("Created new credit risk model")
        
        # Fraud Detection Model
        fraud_model_path = os.path.join(self.model_store_path, "fraud_detection_model.pkl")
        if os.path.exists(fraud_model_path):
            self.loaded_models["fraud_detection"] = joblib.load(fraud_model_path)
            logger.info("Loaded existing fraud detection model")
        else:
            self.loaded_models["fraud_detection"] = self._create_dummy_fraud_model()
            joblib.dump(self.loaded_models["fraud_detection"], fraud_model_path)
            logger.info("Created new fraud detection model")
    
    def _create_dummy_credit_model(self):
        """Create a dummy credit risk model for demonstration"""
        # Generate dummy training data
        np.random.seed(42)
        n_samples = 1000
        
        # Features: income, debt_ratio, credit_history, age, loan_amount
        X = np.random.rand(n_samples, 5)
        X[:, 0] *= 100000  # annual_income (0-100k)
        X[:, 1] *= 0.8     # debt_to_income_ratio (0-0.8)
        X[:, 2] *= 20      # credit_history_length (0-20 years)
        X[:, 3] = X[:, 3] * 40 + 18  # age (18-58)
        X[:, 4] *= 50000   # loan_amount (0-50k)
        
        # Simple risk score: higher income and longer credit history = lower risk
        y = (X[:, 1] * 0.5 + (1 - X[:, 0]/100000) * 0.3 + (1 - X[:, 2]/20) * 0.2) * 100
        y = np.clip(y, 0, 100)  # Risk score 0-100
        
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        return model
    
    def _create_dummy_fraud_model(self):
        """Create a dummy fraud detection model for demonstration"""
        # Generate dummy training data
        np.random.seed(42)
        n_samples = 10000
        
        # Features: amount, time_of_day, day_of_week, card_present, prev_transactions
        X = np.random.rand(n_samples, 5)
        X[:, 0] *= 10000   # amount (0-10k)
        X[:, 1] *= 24      # time_of_day (0-24)
        X[:, 2] *= 7       # day_of_week (0-7)
        X[:, 3] = np.random.choice([0, 1], n_samples)  # card_present
        X[:, 4] *= 100     # previous_transactions_count
        
        # Fraud probability: high amounts at odd hours = higher fraud probability
        fraud_prob = (X[:, 0] / 10000 * 0.4 + 
                     (np.abs(X[:, 1] - 12) / 12) * 0.3 + 
                     (1 - X[:, 3]) * 0.3)
        y = (fraud_prob > 0.7).astype(int)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        return model
    
    async def predict(self, model_name: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction using specified model"""
        if model_name not in self.loaded_models:
            raise ValueError(f"Model '{model_name}' not found")
        
        model = self.loaded_models[model_name]
        
        try:
            if model_name == "credit_risk":
                return await self._predict_credit_risk(model, features)
            elif model_name == "fraud_detection":
                return await self._predict_fraud(model, features)
            else:
                raise ValueError(f"Unknown model type: {model_name}")
                
        except Exception as e:
            logger.error("Prediction error", model_name=model_name, error=str(e))
            raise
    
    async def _predict_credit_risk(self, model, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make credit risk prediction"""
        # Convert features to model input format
        feature_array = np.array([[
            features.get("annual_income", 50000),
            features.get("debt_to_income_ratio", 0.3),
            features.get("credit_history_length", 5),
            features.get("age", 35),
            features.get("loan_amount", 25000)
        ]])
        
        # Make prediction
        risk_score = model.predict(feature_array)[0]
        
        # Calculate risk category
        if risk_score < 30:
            risk_category = "LOW"
        elif risk_score < 70:
            risk_category = "MEDIUM"
        else:
            risk_category = "HIGH"
        
        return {
            "prediction": {
                "risk_score": float(risk_score),
                "risk_category": risk_category,
                "approval_recommendation": risk_score < 60
            },
            "confidence": min(100 - abs(risk_score - 50), 95) / 100
        }
    
    async def _predict_fraud(self, model, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make fraud detection prediction"""
        # Convert features to model input format
        feature_array = np.array([[
            features.get("amount", 100),
            features.get("time_of_day", 12),
            features.get("day_of_week", 3),
            1 if features.get("card_present", True) else 0,
            features.get("previous_transactions_count", 10)
        ]])
        
        # Make prediction
        fraud_probability = model.predict_proba(feature_array)[0]
        is_fraud = model.predict(feature_array)[0]
        
        return {
            "prediction": {
                "is_fraud": bool(is_fraud),
                "fraud_probability": float(fraud_probability[1]),
                "risk_level": "HIGH" if fraud_probability[1] > 0.7 else "MEDIUM" if fraud_probability[1] > 0.3 else "LOW"
            },
            "confidence": float(max(fraud_probability))
        }
    
    async def load_model(self, model_name: str, model_path: str):
        """Load a model from file"""
        try:
            if model_path.endswith('.pkl'):
                model = joblib.load(model_path)
            elif model_path.endswith('.pickle'):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
            else:
                raise ValueError(f"Unsupported model format: {model_path}")
            
            self.loaded_models[model_name] = model
            logger.info("Model loaded successfully", model_name=model_name, path=model_path)
            
        except Exception as e:
            logger.error("Failed to load model", model_name=model_name, error=str(e))
            raise
    
    async def unload_model(self, model_name: str):
        """Unload a model from memory"""
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            logger.info("Model unloaded", model_name=model_name)
        else:
            logger.warning("Model not found for unloading", model_name=model_name)
    
    async def cleanup(self):
        """Cleanup resources"""
        self.loaded_models.clear()
        self.scalers.clear()
        self.encoders.clear()
        logger.info("ModelService cleanup completed")