"""
Save model comparison metrics to database
Run this after training all models in your notebook
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.database import SessionLocal
from app.database.models import ModelComparison
from datetime import datetime

def save_model_metrics():
    """Save metrics for all models tested in research"""
    
    db = SessionLocal()
    
    # Clear existing comparisons
    db.query(ModelComparison).delete()
    
    # Model metrics from your research
    models = [
        {
            'model_name': 'EasyEnsembleClassifier',
            'f1_score': 0.1286,
            'recall': 0.3818,
            'precision': 0.0773,
            'accuracy': 0.6635,
            'roc_auc': 0.5510,
            'pr_auc': 0.0786,
            'sampling_method': 'SVMSMOTE',
            'is_selected': True,
            'notes': 'Best model - Highest F1 score and balanced recall'
        },
        {
            'model_name': 'CatBoost',
            'f1_score': 0.1247,
            'recall': 0.5364,
            'precision': 0.0706,
            'accuracy': 0.5103,
            'roc_auc': 0.5421,
            'pr_auc': 0.0804,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Highest recall but lower precision'
        },
        {
            'model_name': 'RUSBoost',
            'f1_score': 0.1214,
            'recall': 0.2091,
            'precision': 0.0855,
            'accuracy': 0.8031,
            'roc_auc': 0.5884,
            'pr_auc': 0.0838,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Highest ROC-AUC and PR-AUC'
        },
        {
            'model_name': 'DeepLearning',
            'f1_score': 0.1210,
            'recall': 0.9091,
            'precision': 0.0648,
            'accuracy': 0.1407,
            'roc_auc': 0.5213,
            'pr_auc': 0.0740,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Highest recall but very low precision'
        },
        {
            'model_name': 'XGBoost_Advanced',
            'f1_score': 0.1091,
            'recall': 0.2182,
            'precision': 0.0727,
            'accuracy': 0.7682,
            'roc_auc': 0.5472,
            'pr_auc': 0.0806,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Good balance but lower F1'
        },
        {
            'model_name': 'VotingClassifier',
            'f1_score': 0.0833,
            'recall': 0.0727,
            'precision': 0.0976,
            'accuracy': 0.8959,
            'roc_auc': 0.5847,
            'pr_auc': 0.0813,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Ensemble approach with moderate performance'
        },
        {
            'model_name': 'StackingClassifier',
            'f1_score': 0.0552,
            'recall': 0.0364,
            'precision': 0.1143,
            'accuracy': 0.9190,
            'roc_auc': 0.5117,
            'pr_auc': 0.0722,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Highest precision but very low recall'
        },
        {
            'model_name': 'BalancedBagging',
            'f1_score': 0.0462,
            'recall': 0.0364,
            'precision': 0.0635,
            'accuracy': 0.9024,
            'roc_auc': 0.5757,
            'pr_auc': 0.0767,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Low performance across metrics'
        },
        {
            'model_name': 'HistGradientBoosting',
            'f1_score': 0.0435,
            'recall': 0.0273,
            'precision': 0.1071,
            'accuracy': 0.9219,
            'roc_auc': 0.5659,
            'pr_auc': 0.0834,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Highest PR-AUC but very low recall'
        },
        {
            'model_name': 'MLP_Advanced',
            'f1_score': 0.0404,
            'recall': 0.0364,
            'precision': 0.0455,
            'accuracy': 0.8876,
            'roc_auc': 0.4682,
            'pr_auc': 0.0674,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Neural network with poor performance'
        },
        {
            'model_name': 'LightGBM_Advanced',
            'f1_score': 0.0390,
            'recall': 0.0273,
            'precision': 0.0682,
            'accuracy': 0.9125,
            'roc_auc': 0.5705,
            'pr_auc': 0.0803,
            'sampling_method': 'SVMSMOTE',
            'is_selected': False,
            'notes': 'Lowest F1 score'
        }
    ]
    
    for model_data in models:
        model = ModelComparison(
            model_name=model_data['model_name'],
            f1_score=model_data['f1_score'],
            recall=model_data['recall'],
            precision=model_data['precision'],
            accuracy=model_data['accuracy'],
            roc_auc=model_data['roc_auc'],
            pr_auc=model_data['pr_auc'],
            sampling_method=model_data['sampling_method'],
            training_date=datetime.utcnow(),
            is_selected=model_data['is_selected'],
            notes=model_data['notes']
        )
        db.add(model)
    
    db.commit()
    print(f"✓ Saved {len(models)} model comparisons to database")
    db.close()

if __name__ == "__main__":
    save_model_metrics()
