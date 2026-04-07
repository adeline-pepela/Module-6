"""
Dashboard API Endpoints
Executive and operational dashboard data
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import random

from app.models.schemas import DashboardMetrics, CustomerDetail, RiskLevel
from app.database.database import get_db
from app.database.models import Customer, Prediction, Intervention, ModelMetrics

router = APIRouter()

@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Get executive dashboard KPI metrics from database
    """
    total_customers = db.query(Customer).count()
    churned = db.query(Customer).filter(Customer.churn == 'Yes').count()
    churn_rate = (churned / total_customers) if total_customers > 0 else 0
    
    at_risk = db.query(Prediction).filter(Prediction.churn_probability >= 0.6).count()
    revenue_at_risk = db.query(func.sum(Customer.total_revenue)).join(
        Prediction, Customer.pid == Prediction.pid
    ).filter(Prediction.churn_probability >= 0.6).scalar() or 0
    
    metrics = db.query(ModelMetrics).filter(ModelMetrics.is_active == True).first()
    
    return DashboardMetrics(
        total_customers=total_customers,
        current_churn_rate=round(churn_rate, 4),
        predicted_at_risk=at_risk,
        revenue_at_risk=float(revenue_at_risk),
        prevention_rate=round(metrics.recall, 4) if metrics else 0.3818,
        campaign_efficiency=round(metrics.precision, 4) if metrics else 0.0773
    )

@router.get("/churn-trend")
async def get_churn_trend(months: int = 12):
    """
    Get monthly churn trend data
    
    Args:
        months: Number of months to retrieve
        
    Returns:
        List of monthly churn data points
    """
    # Generate mock trend data
    trend_data = []
    base_date = datetime.now() - timedelta(days=30 * months)
    
    for i in range(months):
        date = base_date + timedelta(days=30 * i)
        trend_data.append({
            "month": date.strftime("%Y-%m"),
            "actual_churn": round(random.uniform(0.12, 0.18), 3),
            "predicted_churn": round(random.uniform(0.13, 0.17), 3),
            "customers_churned": random.randint(50, 100)
        })
    
    return trend_data

@router.get("/risk-distribution")
async def get_risk_distribution():
    """
    Get customer distribution by risk level
    
    Returns:
        Risk level distribution data
    """
    return {
        "Ultra High": {"count": 150, "revenue_at_risk": 750000},
        "High": {"count": 300, "revenue_at_risk": 900000},
        "Medium": {"count": 500, "revenue_at_risk": 600000},
        "Low": {"count": 4050, "revenue_at_risk": 250000}
    }

@router.get("/segment-analysis")
async def get_segment_analysis():
    """
    Get churn analysis by customer segment
    
    Returns:
        Segment-wise churn metrics
    """
    return [
        {
            "segment": "SOHO",
            "total_customers": 2000,
            "at_risk": 300,
            "churn_rate": 0.15,
            "avg_revenue": 5000
        },
        {
            "segment": "SME",
            "total_customers": 2500,
            "at_risk": 350,
            "churn_rate": 0.14,
            "avg_revenue": 15000
        },
        {
            "segment": "VSE",
            "total_customers": 500,
            "at_risk": 100,
            "churn_rate": 0.20,
            "avg_revenue": 50000
        }
    ]

@router.get("/customers/at-risk")
async def get_at_risk_customers(
    risk_level: Optional[RiskLevel] = None,
    segment: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of at-risk customers from database with filters
    """
    query = db.query(Customer, Prediction).join(
        Prediction, Customer.pid == Prediction.pid
    ).filter(Prediction.churn_probability >= 0.4)
    
    if segment:
        query = query.filter(Customer.effective_segment == segment)
    
    if risk_level:
        if risk_level.value == "Ultra High":
            query = query.filter(Prediction.churn_probability > 0.8)
        elif risk_level.value == "High":
            query = query.filter(Prediction.churn_probability.between(0.6, 0.8))
        elif risk_level.value == "Medium":
            query = query.filter(Prediction.churn_probability.between(0.4, 0.6))
    
    results = query.order_by(desc(Prediction.churn_probability)).limit(limit).all()
    
    customers = []
    for customer, prediction in results:
        risk_lvl = "Ultra High" if prediction.churn_probability > 0.8 else \
                   "High" if prediction.churn_probability >= 0.6 else "Medium"
        
        customers.append({
            "customer_id": customer.pid,
            "segment": customer.effective_segment or "N/A",
            "churn_probability": round(prediction.churn_probability, 4),
            "risk_level": risk_lvl,
            "arpu": round(customer.arpu or 0, 2),
            "revenue_at_risk": round(customer.total_revenue or 0, 2),
            "account_manager": customer.ka_name or "Unassigned"
        })
    
    return customers

@router.get("/customer/{customer_id}", response_model=CustomerDetail)
async def get_customer_detail(customer_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific customer from database
    """
    customer = db.query(Customer).filter(Customer.pid == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    prediction = db.query(Prediction).filter(
        Prediction.pid == customer_id
    ).order_by(desc(Prediction.predicted_at)).first()
    
    intervention = db.query(Intervention).filter(
        Intervention.pid == customer_id
    ).order_by(desc(Intervention.created_at)).first()
    
    churn_prob = prediction.churn_probability if prediction else 0
    
    drivers = []
    if prediction:
        if prediction.top_driver_1:
            drivers.append({"feature": prediction.top_driver_1, "importance": 0.35, "value": prediction.top_driver_1_value or 0})
        if prediction.top_driver_2:
            drivers.append({"feature": prediction.top_driver_2, "importance": 0.28, "value": prediction.top_driver_2_value or 0})
        if prediction.top_driver_3:
            drivers.append({"feature": prediction.top_driver_3, "importance": 0.22, "value": prediction.top_driver_3_value or 0})
    
    return CustomerDetail(
        customer_id=customer.pid,
        segment=customer.effective_segment or "N/A",
        total_revenue=float(customer.total_revenue or 0),
        arpu=float(customer.arpu or 0),
        active_subscribers=customer.active_subscribers or 0,
        suspended_subscribers=int(customer.suspended_subscribers or 0),
        risk_score=round(churn_prob, 4),
        churn_probability=round(churn_prob, 4),
        top_churn_drivers=drivers,
        account_manager=customer.ka_name or "Unassigned",
        last_intervention=intervention.contact_date.strftime("%Y-%m-%d") if intervention and intervention.contact_date else None,
        intervention_type=intervention.intervention_type if intervention else None
    )
