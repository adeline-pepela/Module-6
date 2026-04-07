"""
Main FastAPI Application
Churn Prediction System for Telecommunication Industry
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.api import dashboard, prediction, monitoring
from app.api.interventions import router as interventions_router
from app.api.evaluation import router as evaluation_router
from app.database.database import engine
from app.database.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Telecom Churn Prediction API",
    description="ML-powered customer churn prediction and retention system",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path("../frontend/static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include API routers
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["Prediction"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])
app.include_router(interventions_router, prefix="/api", tags=["Interventions"])
app.include_router(evaluation_router, tags=["Evaluation"])

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard page"""
    try:
        html_path = Path("../frontend/templates/index.html")
        if html_path.exists():
            return html_path.read_text(encoding='utf-8')
        else:
            return "<h1>Churn Prediction API</h1><p>Visit <a href='/docs'>/docs</a> for API documentation</p><p>HTML file not found at: " + str(html_path.absolute()) + "</p>"
    except Exception as e:
        return f"<h1>Error Loading Dashboard</h1><p>{str(e)}</p><p>Visit <a href='/docs'>/docs</a> for API documentation</p>"

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}
