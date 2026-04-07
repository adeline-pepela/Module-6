"""
Prediction API Endpoints
Real-time churn prediction and batch scoring
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import pandas as pd
from io import StringIO

from app.models.schemas import CustomerInput, PredictionResponse
from app.services.predictor import predictor

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_churn(customer: CustomerInput):
    """
    Predict churn probability for a single customer
    
    Args:
        customer: Customer input data
        
    Returns:
        PredictionResponse: Churn prediction with explanations
    """
    try:
        # Convert input to dictionary
        customer_data = customer.dict()
        
        # Get prediction
        churn_prob, risk_level = predictor.predict(customer_data)
        
        # Get feature importance
        top_drivers = predictor.get_feature_importance(customer_data, top_n=3)
        
        # Get recommended action
        recommended_action = predictor.get_recommended_action(risk_level)
        
        return PredictionResponse(
            customer_id=customer.customer_id,
            churn_probability=churn_prob,
            risk_level=risk_level,
            top_drivers=top_drivers,
            recommended_action=recommended_action
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):
    """
    Batch prediction from CSV file upload
    
    Args:
        file: CSV file with customer data
        
    Returns:
        List of predictions for all customers
    """
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        predictions = []
        
        # Process each customer
        for _, row in df.iterrows():
            customer_data = row.to_dict()
            
            # Get prediction
            churn_prob, risk_level = predictor.predict(customer_data)
            
            # Get top drivers
            top_drivers = predictor.get_feature_importance(customer_data, top_n=3)
            
            predictions.append({
                "customer_id": customer_data.get("customer_id", "Unknown"),
                "churn_probability": churn_prob,
                "risk_level": risk_level,
                "top_drivers": top_drivers
            })
        
        return {
            "total_customers": len(predictions),
            "predictions": predictions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@router.get("/risk-score/{customer_id}")
async def get_risk_score(customer_id: str):
    """
    Get quick risk score for a customer
    
    Args:
        customer_id: Customer identifier
        
    Returns:
        Risk score and level
    """
    # In production, fetch customer data from database
    # For now, return mock response
    return {
        "customer_id": customer_id,
        "risk_score": 0.75,
        "risk_level": "High",
        "last_updated": "2024-01-15T10:30:00"
    }
