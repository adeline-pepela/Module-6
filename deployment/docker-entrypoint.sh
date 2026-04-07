#!/bin/bash
set -e

echo "🚀 Initializing Churn Prediction System..."

cd /app/backend

# Check if database exists
if [ ! -f "churn_prediction.db" ]; then
    echo "📊 Database not found. Creating and initializing..."
    
    # Create tables
    python -c "from app.database.database import engine, Base; from app.database.models import *; Base.metadata.create_all(bind=engine); print('✓ Tables created')"
    
    # Load data
    echo "📥 Loading customer data..."
    python -m app.database.load_data
    
    echo "🔮 Generating predictions..."
    python -m app.database.generate_predictions
    
    echo "📈 Saving model comparison..."
    python -m app.database.save_model_comparison
    
    echo "🎯 Saving feature importance..."
    python -m app.database.save_feature_importance
    
    echo "✅ Database initialization complete!"
else
    echo "✓ Database already exists"
fi

echo "🌐 Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
