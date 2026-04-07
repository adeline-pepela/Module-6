from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    pid = Column(String, unique=True, index=True, nullable=False)
    crm_pid_value_segment = Column(String)
    effective_segment = Column(String, index=True)
    billing_zip = Column(Float)
    ka_name = Column(String, index=True)
    active_subscribers = Column(Integer)
    not_active_subscribers = Column(Float)
    suspended_subscribers = Column(Float)
    total_subs = Column(Integer)
    avg_mobile_revenue = Column(Float)
    avg_fix_revenue = Column(Float)
    total_revenue = Column(Float, index=True)
    arpu = Column(Float)
    churn = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    predictions = relationship("Prediction", back_populates="customer")
    interventions = relationship("Intervention", back_populates="customer")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)
    pid = Column(String, index=True)
    churn_probability = Column(Float, nullable=False)
    risk_level = Column(String, index=True)
    predicted_at = Column(DateTime, default=datetime.utcnow, index=True)
    model_version = Column(String)
    top_driver_1 = Column(String)
    top_driver_1_value = Column(Float)
    top_driver_2 = Column(String)
    top_driver_2_value = Column(Float)
    top_driver_3 = Column(String)
    top_driver_3_value = Column(Float)
    
    customer = relationship("Customer", back_populates="predictions")

class Intervention(Base):
    __tablename__ = "interventions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True)
    pid = Column(String, index=True)
    assigned_manager = Column(String)
    intervention_type = Column(String)
    contact_date = Column(DateTime)
    offer_type = Column(String)
    customer_response = Column(String)
    retention_outcome = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="interventions")

class ModelMetrics(Base):
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String, nullable=False)
    f1_score = Column(Float)
    recall = Column(Float)
    precision = Column(Float)
    roc_auc = Column(Float)
    pr_auc = Column(Float)
    accuracy = Column(Float)
    training_date = Column(DateTime)
    sampling_strategy = Column(String)
    feature_count = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelComparison(Base):
    __tablename__ = "model_comparison"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    f1_score = Column(Float)
    recall = Column(Float)
    precision = Column(Float)
    accuracy = Column(Float)
    roc_auc = Column(Float)
    pr_auc = Column(Float)
    sampling_method = Column(String)
    training_date = Column(DateTime)
    is_selected = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class FeatureImportance(Base):
    __tablename__ = "feature_importance"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String, nullable=False)
    feature_name = Column(String, nullable=False)
    importance_score = Column(Float, nullable=False)
    rank = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
