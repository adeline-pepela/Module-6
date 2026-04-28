# Churn Prediction System - Deployment Guide

## System Status:  READY FOR DISSERTATION

### What's Complete

**Backend API** - FastAPI with 7 functional endpoints  
**Database** - SQLite with 8,436 real customers  
**Predictions** - 8,436 predictions generated  
**Model Evaluation** - 11 models compared with real metrics  
**Feature Importance** - 22 features with real permutation scores  
**Frontend** - 7 pages with interactive charts  
**Bulk Prediction** - CSV template with 10 real customers  

---

## Quick Start

### 1. Start the System

```bash
cd deployment/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access the Dashboard

Open browser: **http://localhost:8000**

---

## System Architecture

```
deployment/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── churn_prediction.db        # SQLite database (3.7MB)
│   ├── app/
│   │   ├── api/
│   │   │   ├── dashboard.py       # Dashboard metrics & charts
│   │   │   ├── prediction.py      # Single & bulk predictions
│   │   │   ├── interventions.py   # Retention campaigns
│   │   │   └── evaluation.py      # Model evaluation metrics
│   │   ├── database/
│   │   │   ├── models.py          # SQLAlchemy ORM models
│   │   │   ├── load_data.py       # Load customers from CSV
│   │   │   ├── generate_predictions.py
│   │   │   ├── save_model_comparison.py
│   │   │   └── save_feature_importance.py
│   │   └── services/
│   │       └── predictor.py       # ML model wrapper
│   └── models/
│       └── best_model.pkl         # EasyEnsembleClassifier (896KB)
├── frontend/
│   ├── templates/
│   │   └── index.html             # Single-page application
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
└── bulk_prediction_template.csv   # Sample CSV with 10 customers
```

---

## Database Schema

### Tables (6)
1. **customers** - 8,436 records
2. **predictions** - 8,436 records  
3. **interventions** - Retention campaigns
4. **model_comparison** - 11 models
5. **feature_importance** - 22 features
6. **model_metrics** - Training history

---

## API Endpoints

### Dashboard
- `GET /api/dashboard/metrics` - 6 KPIs
- `GET /api/dashboard/trends` - Monthly churn trends
- `GET /api/dashboard/risk-distribution` - 4 risk buckets
- `GET /api/dashboard/customers` - Customer list with filters
- `GET /api/dashboard/customer/{pid}` - Customer details

### Predictions
- `POST /api/predict` - Single customer prediction
- `POST /api/predict/bulk` - CSV upload (max 10,000 rows)

### Interventions
- `POST /api/interventions` - Create retention campaign
- `GET /api/interventions` - List all campaigns

### Model Evaluation
- `GET /api/evaluation/model-comparison` - 11 models
- `GET /api/evaluation/feature-importance` - 22 features
- `GET /api/evaluation/confusion-matrix` - TP/FP/TN/FN
- `GET /api/evaluation/roc-curve` - ROC data points
- `GET /api/evaluation/pr-curve` - Precision-Recall curve

---

## Frontend Pages (7)

1. **Overview** - 6 KPIs + 4 charts + 4 risk buckets
2. **Customers** - Searchable table with 8,436 customers
3. **Risk Analysis** - Risk distribution by segment/region
4. **Predict** - Single prediction + bulk CSV upload
5. **Interventions** - Create & track retention campaigns
6. **Model Governance** - Model version & performance tracking
7. **Model Evaluation** - PhD-level analysis with 4 charts

---

## Testing Checklist

### Backend Tests
```bash
# Test database connection
cd deployment/backend
python -c "from app.database.database import SessionLocal; db = SessionLocal(); print(f'✓ Database connected'); db.close()"

# Test API endpoints
curl http://localhost:8000/api/dashboard/metrics
curl http://localhost:8000/api/evaluation/model-comparison
curl http://localhost:8000/api/evaluation/feature-importance
```

### Frontend Tests
- [ ] Navigate to all 7 pages
- [ ] Verify all charts render with data
- [ ] Test customer search/filter
- [ ] Test single prediction form
- [ ] Upload bulk_prediction_template.csv
- [ ] Download prediction results
- [ ] Export customer list to CSV
- [ ] Create intervention campaign
- [ ] Verify hover tooltips on charts

### Data Validation
- [ ] Total customers: 8,436
- [ ] Predictions generated: 8,436
- [ ] High risk customers: 7
- [ ] Medium risk customers: 255
- [ ] Low risk customers: 8,174
- [ ] Models compared: 11
- [ ] Features tracked: 22

---

## Bulk Prediction Format

### Required Columns (12)
```csv
PID,CRM_PID_Value_Segment,EffectiveSegment,Billing_ZIP,KA_name,Active_subscribers,Not_Active_subscribers,Suspended_subscribers,Total_Subscribers,Average_Mobile_Revenue,Average_Fix_Revenue,ARPU
```

### Sample Data
See `bulk_prediction_template.csv` - contains 10 real customers

### Output Columns (7 additional)
- Churn_Probability
- Risk_Level
- Top_Driver_1, Top_Driver_2, Top_Driver_3
- Recommended_Action
- Prediction_Date

---

## Model Performance (Real Data)

### Selected Model: EasyEnsembleClassifier
- **F1 Score**: 0.1286
- **Recall**: 0.3818 (38.18%)
- **Precision**: 0.0773 (7.73%)
- **Accuracy**: 0.6635 (66.35%)
- **ROC-AUC**: 0.5510
- **PR-AUC**: 0.0786

### Confusion Matrix (Test Set: 1,691)
- True Positives: 42
- False Positives: 501
- True Negatives: 1,080
- False Negatives: 68

### Top 5 Features
1. Active_Rate: 0.014311
2. Not_Active_subscribers: 0.009344
3. Billing_ZIP: 0.005795
4. Revenue_Active_Interaction: 0.000651
5. Active_subscribers: 0.000177

---

## Troubleshooting

### Database Issues
```bash
# Recreate database
cd deployment/backend
rm churn_prediction.db
python -c "from app.database.database import engine, Base; from app.database.models import *; Base.metadata.create_all(bind=engine)"
python -m app.database.load_data
python -m app.database.generate_predictions
python -m app.database.save_model_comparison
python -m app.database.save_feature_importance
```

### Port Already in Use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
# Or use different port
uvicorn main:app --reload --port 8001
```

### Model Not Found
```bash
# Verify model exists
ls -lh ../models/best_model.pkl
# Should show: 896KB file
```

---

## Dissertation Screenshots Needed

1. **Dashboard Overview** - All 6 KPIs + 4 charts
2. **Customer List** - Table with filters
3. **Risk Distribution** - Doughnut chart
4. **Single Prediction** - Form + results with drivers
5. **Bulk Prediction** - CSV upload interface
6. **Model Comparison** - Table with 11 models
7. **Feature Importance** - Horizontal bar chart
8. **Confusion Matrix** - Bar chart visualization
9. **ROC Curve** - With AUC score
10. **PR Curve** - Precision-Recall visualization

---

## Production Deployment (Future)

### Recommended Changes
1. Switch to PostgreSQL
2. Add authentication (JWT)
3. Implement rate limiting
4. Add logging (ELK stack)
5. Containerize with Docker
6. Deploy to AWS/Azure
7. Add CI/CD pipeline
8. Implement model versioning
9. Add A/B testing framework
10. Set up monitoring (Prometheus/Grafana)

---

## Contact & Support

**Author**: Adeline Makokha  
**Adm No**: 191199  
**Course**: Dissertation

---

## License

Academic use only - Dissertation Project
