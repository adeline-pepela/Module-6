#!/bin/bash

# Telecom Churn Prediction System - Startup Script

echo "🚀 Starting Telecom Churn Prediction System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if model exists
if [ ! -f "../models/best_model.pkl" ]; then
    echo "⚠️  Warning: Model file not found at ../models/best_model.pkl"
    echo "Please ensure your trained model is in the correct location"
fi

# Start the server
echo "🌐 Starting FastAPI server..."
echo "Dashboard will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
