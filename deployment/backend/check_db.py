"""
Quick diagnostic script to check database status
"""
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.database import SessionLocal
from app.database.models import Customer, Prediction, ModelMetrics

def check_database():
    print("🔍 Checking database status...\n")
    
    db = SessionLocal()
    
    try:
        # Check customers
        start = time.time()
        customer_count = db.query(Customer).count()
        customer_time = time.time() - start
        print(f"✓ Customers: {customer_count} (Query time: {customer_time:.2f}s)")
        
        # Check predictions
        start = time.time()
        prediction_count = db.query(Prediction).count()
        prediction_time = time.time() - start
        print(f"✓ Predictions: {prediction_count} (Query time: {prediction_time:.2f}s)")
        
        # Check model metrics
        start = time.time()
        metrics_count = db.query(ModelMetrics).count()
        metrics_time = time.time() - start
        print(f"✓ Model Metrics: {metrics_count} (Query time: {metrics_time:.2f}s)")
        
        # Test a complex query
        start = time.time()
        at_risk = db.query(Prediction).filter(Prediction.churn_probability >= 0.6).count()
        complex_time = time.time() - start
        print(f"✓ At-risk customers: {at_risk} (Query time: {complex_time:.2f}s)")
        
        print("\n" + "="*50)
        if customer_time > 2 or prediction_time > 2 or complex_time > 2:
            print("⚠️  WARNING: Slow queries detected!")
            print("Consider adding database indexes or reducing data size")
        else:
            print("✓ Database performance looks good!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database()
