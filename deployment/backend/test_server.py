"""
Minimal test server to check what's causing the error
"""
from fastapi import FastAPI
import sys
from pathlib import Path

app = FastAPI(title="Test Server")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/test-model")
async def test_model():
    """Test if model can be loaded"""
    try:
        import joblib
        model_path = "../models/best_model.pkl"
        model = joblib.load(model_path)
        return {"status": "success", "message": "Model loaded successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/test-db")
async def test_db():
    """Test database connection"""
    try:
        from app.database.database import SessionLocal
        from app.database.models import Customer
        db = SessionLocal()
        count = db.query(Customer).count()
        db.close()
        return {"status": "success", "customers": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
