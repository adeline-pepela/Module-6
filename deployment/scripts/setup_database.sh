#!/bin/bash

echo "=========================================="
echo "Churn Prediction System - Database Setup"
echo "=========================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

echo "Step 1: Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Creating database and loading customer data..."
cd app
python -m database.load_data

echo ""
echo "Step 3: Generating predictions for all customers..."
python -m database.generate_predictions

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Database created: churn_prediction.db"
echo "Tables: customers, predictions, interventions, model_metrics"
echo ""
echo "To start the server:"
echo "  cd backend"
echo "  uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Then open: http://localhost:8000"
echo "=========================================="
