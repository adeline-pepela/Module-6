import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.database import engine, SessionLocal
from app.database.models import Base, Customer, ModelMetrics
from datetime import datetime

def load_data_from_csv(csv_url: str):
    """Load customer data from CSV into database"""
    Base.metadata.create_all(bind=engine)
    
    df = pd.read_csv(csv_url)
    print(f"Loaded {len(df)} records from CSV")
    
    # Remove duplicates based on PID
    df = df.drop_duplicates(subset=['PID'], keep='first')
    print(f"After removing duplicates: {len(df)} unique customers")
    
    db = SessionLocal()
    try:
        db.query(Customer).delete()
        db.commit()
        
        batch_size = 100
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            for _, row in batch.iterrows():
                customer = Customer(
                    pid=str(row['PID']),
                    crm_pid_value_segment=row.get('CRM_PID_Value_Segment'),
                    effective_segment=row.get('EffectiveSegment'),
                    billing_zip=row.get('Billing_ZIP'),
                    ka_name=row.get('KA_name'),
                    active_subscribers=int(row.get('Active_subscribers', 0)),
                    not_active_subscribers=row.get('Not_Active_subscribers'),
                    suspended_subscribers=row.get('Suspended_subscribers'),
                    total_subs=int(row.get('Total_SUBs', 0)),
                    avg_mobile_revenue=row.get('AvgMobileRevenue '),
                    avg_fix_revenue=row.get('AvgFIXRevenue'),
                    total_revenue=row.get('TotalRevenue'),
                    arpu=row.get('ARPU'),
                    churn=row.get('CHURN')
                )
                db.add(customer)
            db.commit()
            print(f"Loaded {min(i+batch_size, len(df))}/{len(df)} customers")
        
        print(f"Successfully loaded {len(df)} customers into database")
        
        existing_metrics = db.query(ModelMetrics).filter_by(model_version="v1.0").first()
        if not existing_metrics:
            metrics = ModelMetrics(
                model_version="v1.0",
                f1_score=0.1286,
                recall=0.3818,
                precision=0.0773,
                roc_auc=0.5510,
                pr_auc=0.0786,
                accuracy=0.9227,
                training_date=datetime.utcnow(),
                sampling_strategy="SVMSMOTE",
                feature_count=22,
                is_active=True
            )
            db.add(metrics)
            db.commit()
            print("Model metrics initialized")
        
    except Exception as e:
        db.rollback()
        print(f"Error loading data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    csv_url = "https://raw.githubusercontent.com/adeline-pepela/Dissertation/main/data/dataset.csv"
    load_data_from_csv(csv_url)
