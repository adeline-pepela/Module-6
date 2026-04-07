"""
Add this cell to your modeling_3.ipynb notebook after training your best_model
This will extract feature importance and save it to the database
"""

# Extract feature importance from your EasyEnsembleClassifier
import sys
sys.path.append('deployment/backend')

from deployment.backend.app.database.database import SessionLocal
from deployment.backend.app.database.models import FeatureImportance
from datetime import datetime
import numpy as np

# Get feature importance from your model
# EasyEnsembleClassifier doesn't have direct feature_importances_
# So we'll use permutation importance or get from base estimators

# Option 1: If you have feature names from your preprocessing
feature_names = [
    'Active_subscribers', 'Not_Active_subscribers', 'Suspended_subscribers',
    'Total_SUBs', 'AvgMobileRevenue', 'AvgFIXRevenue', 'TotalRevenue', 'ARPU',
    'Active_Rate', 'Suspended_Rate', 'Revenue_per_Sub', 'Mobile_Revenue_Ratio',
    'Fix_Revenue_Ratio', 'Subscriber_Stability', 'Revenue_Concentration',
    'Service_Diversity', 'Engagement_Score', 'Value_Score', 'Risk_Score',
    'CRM_PID_Value_Segment_encoded', 'EffectiveSegment_encoded', 'KA_name_encoded'
]

# Option 2: Calculate average feature importance from base estimators
try:
    # Get feature importance from base estimators
    importances = []
    for estimator in best_model.estimators_:
        if hasattr(estimator, 'feature_importances_'):
            importances.append(estimator.feature_importances_)
    
    # Average importance across all estimators
    avg_importance = np.mean(importances, axis=0)
    
    # Create feature importance list
    feature_importance_list = list(zip(feature_names, avg_importance))
    feature_importance_list.sort(key=lambda x: x[1], reverse=True)
    
    # Save to database
    db = SessionLocal()
    db.query(FeatureImportance).filter(FeatureImportance.model_version == 'v1.0').delete()
    
    for rank, (feature, importance) in enumerate(feature_importance_list, 1):
        fi = FeatureImportance(
            model_version='v1.0',
            feature_name=feature,
            importance_score=float(importance),
            rank=rank
        )
        db.add(fi)
    
    db.commit()
    print(f"✓ Saved {len(feature_importance_list)} feature importances to database")
    
    # Display top 10
    print("\nTop 10 Most Important Features:")
    for rank, (feature, importance) in enumerate(feature_importance_list[:10], 1):
        print(f"{rank}. {feature}: {importance:.4f}")
    
    db.close()
    
except Exception as e:
    print(f"Error: {e}")
    print("\nAlternative: Use permutation importance")
    print("Run this code instead:")
    print("""
from sklearn.inspection import permutation_importance

# Calculate permutation importance
perm_importance = permutation_importance(
    best_model, X_test, y_test, 
    n_repeats=10, random_state=42, n_jobs=-1
)

# Get feature importance
feature_importance_list = list(zip(feature_names, perm_importance.importances_mean))
feature_importance_list.sort(key=lambda x: x[1], reverse=True)

# Save to database (same code as above)
""")
