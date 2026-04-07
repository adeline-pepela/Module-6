"""
Generate predictions for all customers in database
Run after loading customer data
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database.database import SessionLocal
from app.database.models import Customer, Prediction
from datetime import datetime
import numpy as np

def generate_predictions():
    """Generate predictions for all customers"""
    db = SessionLocal()
    
    try:
        customers = db.query(Customer).all()
        print(f"Generating predictions for {len(customers)} customers...")
        
        db.query(Prediction).delete()
        db.commit()
        
        for i, customer in enumerate(customers):
            try:
                # Prepare customer data
                customer_data = {
                    'customer_id': customer.pid,
                    'segment': customer.effective_segment,
                    'Active subscribers': customer.active_subscribers or 0,
                    'Total Subscribers': customer.total_subs or 0,
                    'Suspended subscribers': customer.suspended_subscribers or 0,
                    'Average Mobile Revenue': customer.avg_mobile_revenue or 0,
                    'Average Fix Revenue': customer.avg_fix_revenue or 0,
                    'ARPU': customer.arpu or 0
                }
                
                # Generate prediction (simplified - using random for demo)
                # In production, use actual model prediction
                churn_prob = np.random.beta(2, 10)  # Skewed towards lower probabilities
                
                if churn_prob > 0.8:
                    risk_level = "Ultra High"
                elif churn_prob >= 0.6:
                    risk_level = "High"
                elif churn_prob >= 0.4:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"
                
                # Top drivers (simplified)
                drivers = [
                    ("Suspended_subscribers", customer.suspended_subscribers or 0),
                    ("Active_Rate", (customer.active_subscribers or 0) / (customer.total_subs or 1)),
                    ("Revenue_Ratio", (customer.avg_mobile_revenue or 0) / ((customer.avg_fix_revenue or 0) + 1))
                ]
                
                # Save prediction
                prediction = Prediction(
                    customer_id=customer.id,
                    pid=customer.pid,
                    churn_probability=float(churn_prob),
                    risk_level=risk_level,
                    predicted_at=datetime.utcnow(),
                    model_version="v1.0",
                    top_driver_1=drivers[0][0],
                    top_driver_1_value=float(drivers[0][1]),
                    top_driver_2=drivers[1][0],
                    top_driver_2_value=float(drivers[1][1]),
                    top_driver_3=drivers[2][0],
                    top_driver_3_value=float(drivers[2][1])
                )
                db.add(prediction)
                
                if (i + 1) % 100 == 0:
                    db.commit()
                    print(f"Processed {i + 1}/{len(customers)} customers")
            
            except Exception as e:
                print(f"Error processing customer {customer.pid}: {e}")
                continue
        
        db.commit()
        print(f"\nSuccessfully generated predictions for {len(customers)} customers")
        
        # Print summary
        ultra_high = db.query(Prediction).filter(Prediction.risk_level == "Ultra High").count()
        high = db.query(Prediction).filter(Prediction.risk_level == "High").count()
        medium = db.query(Prediction).filter(Prediction.risk_level == "Medium").count()
        low = db.query(Prediction).filter(Prediction.risk_level == "Low").count()
        
        print("\nRisk Distribution:")
        print(f"  Ultra High: {ultra_high}")
        print(f"  High: {high}")
        print(f"  Medium: {medium}")
        print(f"  Low: {low}")
        
    except Exception as e:
        db.rollback()
        print(f"Error generating predictions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    generate_predictions()
