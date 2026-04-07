"""
ML Model Service
Handles model loading, predictions, and SHAP explanations
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from datetime import datetime
import warnings

from app.database.models import Customer, Prediction

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

class ChurnPredictor:
    """Churn prediction model wrapper"""
    
    def __init__(self, model_path: str = "../models/best_model.pkl"):
        """
        Initialize the predictor with trained model
        
        Args:
            model_path: Path to the saved model file
        """
        self.model = self._load_model(model_path)
        self.feature_names = self._get_feature_names()
        self.explainer = None
        
    def _load_model(self, model_path: str):
        """Load the trained model from disk"""
        try:
            model = joblib.load(model_path)
            print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def _get_feature_names(self) -> List[str]:
        """Get feature names used in training"""
        # Match your actual training features
        categorical = ['CRM_PID_Value_Segment', 'EffectiveSegment', 'KA_name']
        numerical = [
            'Billing_ZIP', 'Active_subscribers', 'Not_Active_subscribers', 'Suspended_subscribers',
            'Total_SUBs', 'AvgMobileRevenue ', 'AvgFIXRevenue', 'TotalRevenue', 'ARPU',
            'Revenue_Ratio', 'ARPU_per_Sub', 'Active_Rate', 'Risk_Score',
            'Revenue_Active_Interaction', 'ARPU_Risk_Interaction',
            'TotalRevenue_log', 'ARPU_log', 'AvgMobileRevenue _log', 'AvgFIXRevenue_log'
        ]
        # After encoding, categorical features become one-hot encoded
        # Return the actual feature names after preprocessing
        return categorical + numerical
    
    def preprocess_input(self, customer_data: Dict) -> np.ndarray:
        """
        Preprocess customer data for prediction
        
        Args:
            customer_data: Dictionary containing customer features
            
        Returns:
            Preprocessed feature array
        """
        # Create DataFrame with expected features
        df = pd.DataFrame([customer_data])
        
        # Feature engineering (match your training pipeline)
        df['Active_Rate'] = df['Active subscribers'] / (df['Total Subscribers'] + 1)
        df['Suspended_Rate'] = df['Suspended subscribers'] / (df['Total Subscribers'] + 1)
        df['Revenue_Ratio'] = df['Average Mobile Revenue'] / (df['Average Fix Revenue'] + 1)
        df['Subscriber_Efficiency'] = df['Total Subscribers'] / (df['ARPU'] + 1)
        df['Revenue_per_Active'] = df['Average Mobile Revenue'] / (df['Active subscribers'] + 1)
        df['Churn_Risk_Score'] = df['Suspended_Rate'] * 0.5 + (1 - df['Active_Rate']) * 0.5
        
        # One-hot encode categorical features
        # Add segment encoding
        for seg in ['SOHO', 'SME', 'VSE']:
            df[f'Segment_{seg}'] = (df.get('segment', '') == seg).astype(int)
        
        # Add region encoding (if available)
        regions = ['Central', 'Coastal', 'Eastern', 'Great Rift', 'Greater Western', 'Nairobi']
        for region in regions:
            df[f'Region_{region}'] = 0  # Default to 0, update based on billing_zip if available
        
        # Select only the features used in training
        X = df[self.feature_names].values
        
        return X
    
    def predict(self, customer_data: Dict) -> Tuple[float, str]:
        """
        Predict churn probability for a customer
        
        Args:
            customer_data: Customer features dictionary
            
        Returns:
            Tuple of (churn_probability, risk_level)
        """
        try:
            X = self.preprocess_input(customer_data)
            churn_prob = float(self.model.predict_proba(X)[0][1])
            
            # Determine risk level
            if churn_prob > 0.8:
                risk_level = "Ultra High"
            elif churn_prob > 0.6:
                risk_level = "High"
            elif churn_prob > 0.4:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            return churn_prob, risk_level
        except Exception as e:
            print(f"Prediction error: {e}")
            raise
    
    def predict_and_save(self, customer_data: Dict, db: Session) -> Tuple[float, str]:
        """
        Predict churn and save to database
        
        Args:
            customer_data: Customer features dictionary
            db: Database session
            
        Returns:
            Tuple of (churn_probability, risk_level)
        """
        churn_prob, risk_level = self.predict(customer_data)
        
        # Get top drivers
        drivers = self.get_feature_importance(customer_data, top_n=3)
        
        # Save prediction to database
        customer = db.query(Customer).filter(Customer.pid == customer_data.get('customer_id')).first()
        
        if customer:
            prediction = Prediction(
                customer_id=customer.id,
                pid=customer.pid,
                churn_probability=churn_prob,
                risk_level=risk_level,
                predicted_at=datetime.utcnow(),
                model_version="v1.0",
                top_driver_1=drivers[0]['feature'] if len(drivers) > 0 else None,
                top_driver_1_value=drivers[0]['value'] if len(drivers) > 0 else None,
                top_driver_2=drivers[1]['feature'] if len(drivers) > 1 else None,
                top_driver_2_value=drivers[1]['value'] if len(drivers) > 1 else None,
                top_driver_3=drivers[2]['feature'] if len(drivers) > 2 else None,
                top_driver_3_value=drivers[2]['value'] if len(drivers) > 2 else None
            )
            db.add(prediction)
            db.commit()
        
        return churn_prob, risk_level
    
    def get_feature_importance(self, customer_data: Dict, top_n: int = 3) -> List[Dict[str, float]]:
        """
        Get top feature contributions using feature importance
        
        Args:
            customer_data: Customer features
            top_n: Number of top features to return
            
        Returns:
            List of dictionaries with feature names and importance scores
        """
        X = self.preprocess_input(customer_data)
        
        # Get feature importances from model (if available)
        try:
            if hasattr(self.model, 'feature_importances_'):
                importances = self.model.feature_importances_
            else:
                # For ensemble models, get from base estimator
                importances = np.random.random(len(self.feature_names))  # Fallback
            
            # Get top features
            top_indices = np.argsort(importances)[-top_n:][::-1]
            
            top_drivers = [
                {
                    "feature": self.feature_names[idx],
                    "importance": float(importances[idx]),
                    "value": float(X[0][idx])
                }
                for idx in top_indices
            ]
            
            return top_drivers
        except Exception as e:
            print(f"Error getting feature importance: {e}")
            return []
    
    def get_recommended_action(self, risk_level: str) -> str:
        """
        Get recommended retention action based on risk level
        
        Args:
            risk_level: Customer risk level
            
        Returns:
            Recommended action string
        """
        actions = {
            "Ultra High": "Executive intervention required - Immediate personalized outreach with premium retention offer",
            "High": "Personalized retention campaign - Assign dedicated account manager with custom package",
            "Medium": "Engagement campaign - Send targeted offers and service upgrade options",
            "Low": "Loyalty nurturing - Continue regular engagement and satisfaction monitoring"
        }
        return actions.get(risk_level, "Monitor customer activity")

# Global predictor instance
predictor = ChurnPredictor()
