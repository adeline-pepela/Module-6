@echo off
echo 🚀 Starting Telecom Churn Prediction System...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if model exists
if not exist "..\models\best_model.pkl" (
    echo ⚠️  Warning: Model file not found at ..\models\best_model.pkl
    echo Please ensure your trained model is in the correct location
)

REM Start the server
echo 🌐 Starting FastAPI server...
echo Dashboard will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
