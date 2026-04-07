"""
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    """Customer risk level categories"""
    ULTRA_HIGH = "Ultra High"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class CustomerSegment(str, Enum):
    """Business customer segments"""
    SOHO = "SOHO"
    SME = "SME"
    VSE = "VSE"

class CustomerInput(BaseModel):
    """Input schema for single customer prediction"""
    customer_id: str = Field(..., description="Unique customer identifier")
    segment: str = Field(..., description="Customer segment")
    active_subscribers: int = Field(..., ge=0)
    suspended_subscribers: int = Field(..., ge=0)
    total_subscribers: int = Field(..., ge=0)
    average_mobile_revenue: float = Field(..., ge=0)
    average_fix_revenue: float = Field(..., ge=0)
    arpu: float = Field(..., ge=0)
    billing_zip: Optional[str] = None
    
class PredictionResponse(BaseModel):
    """Response schema for churn prediction"""
    customer_id: str
    churn_probability: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    top_drivers: List[Dict[str, float]]
    recommended_action: str
    timestamp: datetime = Field(default_factory=datetime.now)

class DashboardMetrics(BaseModel):
    """Executive dashboard KPI metrics"""
    total_customers: int
    current_churn_rate: float
    predicted_at_risk: int
    revenue_at_risk: float
    prevention_rate: float
    campaign_efficiency: float

class FeatureDriver(BaseModel):
    """Feature importance driver"""
    feature: str
    importance: float
    value: float

class CustomerDetail(BaseModel):
    """Detailed customer information"""
    customer_id: str
    segment: CustomerSegment
    total_revenue: float
    arpu: float
    active_subscribers: int
    suspended_subscribers: int
    risk_score: float
    churn_probability: float
    top_churn_drivers: List[FeatureDriver]
    account_manager: Optional[str] = None

class RetentionAction(BaseModel):
    """Retention intervention tracking"""
    customer_id: str
    account_manager: str
    intervention_type: str
    contact_date: datetime
    offer_type: str
    customer_response: Optional[str] = None
    retention_outcome: Optional[bool] = None

class ModelMetrics(BaseModel):
    """Model performance monitoring"""
    model_config = {"protected_namespaces": ()}
    
    model_version: str
    last_retrain_date: datetime
    f1_score: float
    pr_auc: float
    recall: float
    precision: float
    feature_count: int
    sampling_strategy: str
