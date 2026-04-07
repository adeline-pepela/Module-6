# Database-Driven Churn Prediction System

## Overview
This deployment now uses a **dynamic database system** instead of hardcoded mock data. All customer data, predictions, interventions, and model metrics are stored in a relational database (SQLite by default, easily upgradeable to PostgreSQL).

## Architecture

### Database Schema

**customers** - Customer master data from CSV
- PID, segment, revenue, ARPU, subscribers, etc.

**predictions** - ML model predictions with timestamps
- churn_probability, risk_level, top_drivers, model_version

**interventions** - Retention actions tracking
- assigned_manager, intervention_type, customer_response, retention_outcome

**model_metrics** - Model performance monitoring
- f1_score, recall, precision, training_date, is_active

## Quick Start

### 1. Install Dependencies
```bash
cd deployment/backend
pip install -r requirements.txt
```

### 2. Load Data into Database
```bash
cd app
python -m database.load_data
```

This will:
- Create database tables
- Load 8,453 customers from GitHub CSV
- Initialize model metrics (F1=0.1286, Recall=0.3818)

### 3. Start Server
```bash
cd ..
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Dashboard
Open: http://localhost:8000

## Database Configuration

### SQLite (Default)
```python
DATABASE_URL = "sqlite:///./churn_prediction.db"
```

### PostgreSQL (Production)
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/churn_db"
```

## API Endpoints

### Dashboard (Dynamic Data)
- `GET /api/dashboard/metrics` - Real KPIs from database
- `GET /api/dashboard/customers/at-risk` - Filtered customer list
- `GET /api/dashboard/customer/{id}` - Customer detail with predictions

### Predictions (Saves to DB)
- `POST /api/prediction/predict` - Predict and save to database
- `POST /api/prediction/batch` - Batch predictions

### Interventions (New)
- `POST /api/interventions` - Create retention action
- `PUT /api/interventions/{id}` - Update with outcome
- `GET /api/interventions/{customer_id}` - Get customer history

### Monitoring
- `GET /api/monitoring/metrics` - Model performance from DB
- `GET /api/monitoring/drift` - Data drift detection

## Data Flow

1. **CSV → Database**: `load_data.py` imports customer data
2. **Prediction → Database**: Each prediction saved with timestamp
3. **Dashboard → Database**: Real-time queries for metrics
4. **Intervention → Database**: Track retention campaigns

## Key Features

### 1. Dynamic Metrics
- Total customers: Live count from DB
- Churn rate: Calculated from actual data
- At-risk customers: Based on prediction table
- Revenue at risk: Aggregated from customer revenue

### 2. Risk Segmentation
Filter customers by:
- Risk level (Ultra High, High, Medium, Low)
- Segment (SOHO, SME, VSE)
- Account manager
- Revenue range

### 3. Intervention Tracking
- Assign retention actions
- Track customer responses
- Measure campaign ROI
- A/B testing support

### 4. Model Governance
- Version tracking
- Performance monitoring
- Drift detection
- Audit trail

## Database Queries Examples

### Get high-risk customers
```python
db.query(Customer, Prediction).join(
    Prediction, Customer.pid == Prediction.pid
).filter(Prediction.churn_probability > 0.8).all()
```

### Calculate revenue at risk
```python
db.query(func.sum(Customer.total_revenue)).join(
    Prediction, Customer.pid == Prediction.pid
).filter(Prediction.churn_probability >= 0.6).scalar()
```

### Track intervention success
```python
db.query(Intervention).filter(
    Intervention.retention_outcome == 'Retained'
).count()
```

## Upgrading to PostgreSQL

1. Install psycopg2:
```bash
pip install psycopg2-binary
```

2. Set environment variable:
```bash
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
```

3. Run migrations:
```bash
alembic upgrade head
```

4. Load data:
```bash
python -m app.database.load_data
```

## Data Sources

### Primary Data
- **URL**: https://raw.githubusercontent.com/adeline-pepela/Dissertation/main/data/dataset.csv
- **Records**: 8,453 business customers
- **Period**: 24-month behavioral data
- **Features**: 14 columns (PID, segments, revenue, subscribers, churn)

### Engineered Features
The system automatically generates:
- Revenue_Ratio, ARPU_per_Sub, Active_Rate
- Risk_Score, Revenue_Active_Interaction
- Log transformations

## Model Information

- **Algorithm**: EasyEnsembleClassifier
- **Sampling**: SVMSMOTE
- **Features**: 22 (3 categorical + 19 numerical)
- **Performance**: F1=0.1286, Recall=0.3818, Precision=0.0773
- **File**: models/best_model.pkl (896KB)

## Maintenance

### Backup Database
```bash
sqlite3 churn_prediction.db ".backup backup.db"
```

### Clear Predictions
```python
db.query(Prediction).delete()
db.commit()
```

### Update Model Metrics
```python
metrics = db.query(ModelMetrics).filter_by(is_active=True).first()
metrics.f1_score = 0.15
db.commit()
```

## Troubleshooting

### Database locked
- Close other connections
- Use WAL mode: `PRAGMA journal_mode=WAL;`

### Missing data
- Run `load_data.py` again
- Check CSV URL accessibility

### Slow queries
- Add indexes: `CREATE INDEX idx_churn_prob ON predictions(churn_probability);`
- Use query optimization

## Next Steps

1. **Load your data**: Run `python -m database.load_data`
2. **Generate predictions**: Use `/api/prediction/batch` endpoint
3. **Track interventions**: Create retention campaigns
4. **Monitor performance**: Check `/api/monitoring/metrics`

## Support

For issues or questions:
- Check database logs
- Verify CSV data format
- Ensure all dependencies installed
- Review API documentation at `/docs`
