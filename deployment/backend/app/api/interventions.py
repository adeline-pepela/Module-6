from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database.database import get_db
from app.database.models import Customer, Intervention

router = APIRouter()

class InterventionCreate(BaseModel):
    customer_id: str
    assigned_manager: str
    intervention_type: str
    contact_date: Optional[datetime] = None
    offer_type: Optional[str] = None
    notes: Optional[str] = None

class InterventionUpdate(BaseModel):
    customer_response: Optional[str] = None
    retention_outcome: Optional[str] = None
    notes: Optional[str] = None

@router.post("/interventions")
async def create_intervention(intervention: InterventionCreate, db: Session = Depends(get_db)):
    """Create new retention intervention"""
    customer = db.query(Customer).filter(Customer.pid == intervention.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    new_intervention = Intervention(
        customer_id=customer.id,
        pid=customer.pid,
        assigned_manager=intervention.assigned_manager,
        intervention_type=intervention.intervention_type,
        contact_date=intervention.contact_date or datetime.utcnow(),
        offer_type=intervention.offer_type,
        notes=intervention.notes
    )
    db.add(new_intervention)
    db.commit()
    db.refresh(new_intervention)
    
    return {"message": "Intervention created", "intervention_id": new_intervention.id}

@router.put("/interventions/{intervention_id}")
async def update_intervention(
    intervention_id: int,
    update: InterventionUpdate,
    db: Session = Depends(get_db)
):
    """Update intervention with customer response and outcome"""
    intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
    if not intervention:
        raise HTTPException(status_code=404, detail="Intervention not found")
    
    if update.customer_response:
        intervention.customer_response = update.customer_response
    if update.retention_outcome:
        intervention.retention_outcome = update.retention_outcome
    if update.notes:
        intervention.notes = update.notes
    
    intervention.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Intervention updated"}

@router.get("/interventions/{customer_id}")
async def get_customer_interventions(customer_id: str, db: Session = Depends(get_db)):
    """Get all interventions for a customer"""
    interventions = db.query(Intervention).filter(Intervention.pid == customer_id).all()
    
    return [{
        "id": i.id,
        "intervention_type": i.intervention_type,
        "assigned_manager": i.assigned_manager,
        "contact_date": i.contact_date,
        "offer_type": i.offer_type,
        "customer_response": i.customer_response,
        "retention_outcome": i.retention_outcome,
        "notes": i.notes,
        "created_at": i.created_at
    } for i in interventions]
