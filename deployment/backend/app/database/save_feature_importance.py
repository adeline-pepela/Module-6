"""
Save feature importance to database
Update these values with actual importance from your notebook
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.database import SessionLocal
from app.database.models import FeatureImportance
from datetime import datetime

def save_feature_importance():
    """Save feature importance for the 22 features"""
    
    db = SessionLocal()
    
    # Clear existing
    db.query(FeatureImportance).filter(FeatureImportance.model_version == 'v1.0').delete()
    
    # Your 22 features with REAL importance scores from permutation_importance
    features = [
        ('Active_Rate', 0.014311),
        ('Not_Active_subscribers', 0.009344),
        ('Billing_ZIP', 0.005795),
        ('Revenue_Active_Interaction', 0.000651),
        ('Active_subscribers', 0.000177),
        ('CRM_PID_Value_Segment', 0.000000),
        ('EffectiveSegment', 0.000000),
        ('Suspended_subscribers', 0.000000),
        ('AvgFIXRevenue', 0.000000),
        ('TotalRevenue', 0.000000),
        ('Revenue_Ratio', 0.000000),
        ('Risk_Score', 0.000000),
        ('TotalRevenue_log', 0.000000),
        ('ARPU_log', 0.000000),
        ('AvgMobileRevenue_log', 0.000000),
        ('AvgFIXRevenue_log', 0.000000),
        ('ARPU', -0.000177),
        ('ARPU_Risk_Interaction', -0.001183),
        ('ARPU_per_Sub', -0.001597),
        ('AvgMobileRevenue', -0.001774),
        ('KA_name', -0.005500),
        ('Total_SUBs', -0.011118)
    ]
    
    for rank, (feature, importance) in enumerate(features, 1):
        fi = FeatureImportance(
            model_version='v1.0',
            feature_name=feature,
            importance_score=importance,
            rank=rank
        )
        db.add(fi)
    
    db.commit()
    print(f"✓ Saved {len(features)} feature importances to database")
    print("\nTop 10 Features:")
    for rank, (feature, importance) in enumerate(features[:10], 1):
        print(f"  {rank}. {feature}: {importance:.6f}")
    
    db.close()

if __name__ == "__main__":
    save_feature_importance()
