# Customer Churn Prediction System for Telecommunication Industry

**Author**: Adeline Makokha  
**Adm No**: 191199  
**Course**: DSA 8502 Predictive and Optimization Analytics  
**Institution**: Strathmore University

---

## 📋 Project Overview

A complete machine learning system for predicting customer churn in the telecommunication industry. This project includes:

- **Machine Learning Model**: EasyEnsembleClassifier trained on 8,436 real customers
- **Web Dashboard**: Interactive 7-page application with real-time predictions
- **REST API**: FastAPI backend with 15+ endpoints
- **Database**: SQLite with customer data, predictions, and model metrics
- **Bulk Prediction**: CSV upload for batch processing

### Key Metrics
- **F1 Score**: 0.1286
- **Recall**: 38.18%
- **Precision**: 7.73%
- **ROC-AUC**: 0.5510
- **Customers**: 8,436
- **Features**: 22 (3 categorical + 19 numerical)

---

## 🚀 Quick Start

### Option 1: Docker (Recommended - Easiest)

**One command deployment:**

```bash
cd deployment
./scripts/deploy.sh          # Linux/Mac
# OR
scripts\deploy.bat           # Windows
```

Access: **http://localhost:8000**

**Prerequisites:** Docker & Docker Compose installed  
**Time:** 5-10 minutes (first time)  
**See:** [deployment/docs/DOCKER_README.md](deployment/docs/DOCKER_README.md)

---

### Option 2: Manual Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd Churn-main

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r deployment/requirements.txt

# 5. Setup database
cd deployment/backend
python -c "from app.database.database import engine, Base; from app.database.models import *; Base.metadata.create_all(bind=engine)"
python -m app.database.load_data
python -m app.database.generate_predictions
python -m app.database.save_model_comparison
python -m app.database.save_feature_importance

# 6. Start the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Prerequisites for Manual Setup
- Python 3.8+
- pip
- Git

### Access the Dashboard
Open browser: **http://localhost:8000**

---

## 📁 Project Structure

```
Churn-main/
├── modeling_3.ipynb              # Main research notebook
├── models/
│   └── best_model.pkl            # Trained EasyEnsembleClassifier (896KB)
├── data/
│   └── dataset.csv               # Customer dataset (8,453 records)
├── deployment/                   # Production deployment system
│   ├── backend/
│   │   ├── main.py              # FastAPI application
│   │   ├── churn_prediction.db  # SQLite database
│   │   ├── app/
│   │   │   ├── api/             # API endpoints
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── prediction.py
│   │   │   │   ├── interventions.py
│   │   │   │   └── evaluation.py
│   │   │   ├── database/        # Database models & scripts
│   │   │   │   ├── models.py
│   │   │   │   ├── load_data.py
│   │   │   │   ├── generate_predictions.py
│   │   │   │   ├── save_model_comparison.py
│   │   │   │   └── save_feature_importance.py
│   │   │   └── services/
│   │   │       └── predictor.py # ML model wrapper
│   │   └── models/
│   │       └── best_model.pkl   # Symlink to main model
│   ├── frontend/
│   │   ├── templates/
│   │   │   └── index.html       # Single-page application
│   │   └── static/
│   │       ├── css/styles.css
│   │       └── js/app.js
│   ├── requirements.txt         # Python dependencies
│   ├── bulk_prediction_template.csv
│   ├── DEPLOYMENT_GUIDE.md
│   └── BULK_PREDICTION_FORMAT.md
├── visuals/                     # Research visualizations
└── README.md
```

---

## 🔧 Detailed Setup Instructions

### Step 1: Environment Setup

#### Create Virtual Environment
```bash
# Navigate to project root
cd Churn-main

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation (should show venv path)
which python  # Linux/Mac
where python  # Windows
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r deployment/requirements.txt
```

**Key Dependencies:**
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pandas==2.1.3
- scikit-learn==1.3.2
- imbalanced-learn==0.12.0
- joblib==1.3.2

### Step 2: Database Setup

```bash
cd deployment/backend

# Create database tables
python -c "from app.database.database import engine, Base; from app.database.models import *; Base.metadata.create_all(bind=engine); print('✓ Tables created')"

# Load customer data (8,436 customers)
python -m app.database.load_data

# Generate predictions for all customers
python -m app.database.generate_predictions

# Save model comparison data (11 models)
python -m app.database.save_model_comparison

# Save feature importance (22 features)
python -m app.database.save_feature_importance
```

**Expected Output:**
- ✓ Tables created
- ✓ Loaded 8,436 customers
- ✓ Generated 8,436 predictions
- ✓ Saved 11 model comparisons
- ✓ Saved 22 feature importances

### Step 3: Verify Model File

```bash
# Check model exists
ls -lh ../../models/best_model.pkl

# Should show: 896KB file
```

### Step 4: Start Application

```bash
# From deployment/backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 5: Test API

```bash
# In new terminal
curl http://localhost:8000/api/dashboard/metrics

# Expected: JSON with 6 KPIs
```

---

## 📊 Dashboard Features

### 1. Overview Page
- 6 KPI cards (Total Customers, Churn Rate, At-Risk, Revenue at Risk, Prevention Rate, Campaign Efficiency)
- 4 risk buckets (Ultra High, High, Medium, Low)
- 4 interactive charts (Churn Trends, Risk Distribution, Revenue Impact, Top Features)

### 2. Customers Page
- Searchable table with 8,436 customers
- Filters by segment, risk level, region
- Export to CSV

### 3. Risk Analysis Page
- Risk distribution by segment
- Risk distribution by region
- Detailed customer lists per risk level

### 4. Predict Page
- Single customer prediction form
- Bulk CSV upload (max 10,000 rows)
- Download results with recommendations

### 5. Interventions Page
- Create retention campaigns
- Track intervention outcomes
- Assign account managers

### 6. Model Governance Page
- Model version tracking
- Performance monitoring
- Training history

### 7. Model Evaluation Page
- Model comparison table (11 models)
- Feature importance chart (22 features)
- Confusion matrix visualization
- ROC curve (AUC: 0.5510)
- Precision-Recall curve (AUC: 0.0786)

---

## 🔌 API Endpoints

### Dashboard
```
GET  /api/dashboard/metrics              # 6 KPIs
GET  /api/dashboard/trends               # Monthly trends
GET  /api/dashboard/risk-distribution    # Risk buckets
GET  /api/dashboard/customers            # Customer list
GET  /api/dashboard/customer/{pid}       # Customer details
```

### Predictions
```
POST /api/predict                        # Single prediction
POST /api/predict/bulk                   # Bulk CSV upload
```

### Interventions
```
POST /api/interventions                  # Create campaign
GET  /api/interventions                  # List campaigns
```

### Model Evaluation
```
GET  /api/evaluation/model-comparison    # 11 models
GET  /api/evaluation/feature-importance  # 22 features
GET  /api/evaluation/confusion-matrix    # TP/FP/TN/FN
GET  /api/evaluation/roc-curve           # ROC data
GET  /api/evaluation/pr-curve            # PR data
```

---

## 📤 Bulk Prediction Format

### Required CSV Columns (12)
```csv
PID,CRM_PID_Value_Segment,EffectiveSegment,Billing_ZIP,KA_name,Active_subscribers,Not_Active_subscribers,Suspended_subscribers,Total_Subscribers,Average_Mobile_Revenue,Average_Fix_Revenue,ARPU
```

### Sample Template
See `deployment/bulk_prediction_template.csv` - contains 10 real customers

### Output Columns (7 additional)
- Churn_Probability
- Risk_Level
- Top_Driver_1, Top_Driver_2, Top_Driver_3
- Recommended_Action
- Prediction_Date

---

## 🧪 Testing

### Backend Tests
```bash
cd deployment/backend

# Test database
python -c "from app.database.database import SessionLocal; db = SessionLocal(); print('✓ Connected'); db.close()"

# Test API
curl http://localhost:8000/api/dashboard/metrics
curl http://localhost:8000/api/evaluation/model-comparison
```

### Frontend Tests
- Navigate to all 7 pages
- Test search/filter functionality
- Upload bulk_prediction_template.csv
- Export customer list
- Create intervention campaign

---

## 📈 Model Performance

### Selected Model: EasyEnsembleClassifier
- **Sampling**: SVMSMOTE
- **Features**: 22 (3 categorical + 19 numerical)
- **Training Set**: 6,745 customers
- **Test Set**: 1,691 customers

### Metrics
| Metric | Value |
|--------|-------|
| F1 Score | 0.1286 |
| Recall | 0.3818 (38.18%) |
| Precision | 0.0773 (7.73%) |
| Accuracy | 0.6635 (66.35%) |
| ROC-AUC | 0.5510 |
| PR-AUC | 0.0786 |

### Confusion Matrix
| | Predicted No | Predicted Yes |
|---|---|---|
| **Actual No** | 1,080 (TN) | 501 (FP) |
| **Actual Yes** | 68 (FN) | 42 (TP) |

### Top 5 Features
1. Active_Rate: 0.014311
2. Not_Active_subscribers: 0.009344
3. Billing_ZIP: 0.005795
4. Revenue_Active_Interaction: 0.000651
5. Active_subscribers: 0.000177

---

## 🛠️ Troubleshooting

### Database Not Found
```bash
cd deployment/backend
rm -f churn_prediction.db
# Re-run Step 2: Database Setup
```

### Port Already in Use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r deployment/requirements.txt
```

### Model Loading Error
```bash
# Verify model exists and is correct size
ls -lh models/best_model.pkl
# Should show: 896KB

# Check sklearn version
python -c "import sklearn; print(sklearn.__version__)"
# Should be: 1.3.2
```

---

## 📚 Research Notebook

The main research is in `modeling_3.ipynb`:
- Data exploration & preprocessing
- Feature engineering
- Model training & comparison (11 models)
- Hyperparameter tuning
- Model evaluation
- SHAP & permutation importance

---

## 🔐 Security Notes

**For Production Deployment:**
- Add authentication (JWT tokens)
- Implement rate limiting
- Use environment variables for secrets
- Switch to PostgreSQL
- Enable HTTPS
- Add input validation
- Implement logging

---

## 📝 Citation

```bibtex
@mastersthesis{makokha2024churn,
  author  = {Adeline Makokha},
  title   = {Application of Machine Learning Techniques in Customer Churn Prediction for Telecommunication Industries},
  school  = {Strathmore University},
  year    = {2024},
  type    = {PhD Dissertation},
  course  = {DSA 8502 Predictive and Optimization Analytics}
}
```

---

## 📄 License

Academic use only - PhD Dissertation Project

---

## 🤝 Contributing

This is a dissertation project. For questions or collaboration:
- **Author**: Adeline Makokha
- **Adm No**: 191199
- **Email**: [Contact through Strathmore University]

---

## 📖 Additional Documentation

- `deployment/DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `deployment/BULK_PREDICTION_FORMAT.md` - CSV format specification
- `deployment/ARCHITECTURE.md` - System architecture details
- `deployment/DATABASE_GUIDE.md` - Database schema documentation

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Database created with 8,436 customers
- [ ] Predictions generated
- [ ] Model comparison data loaded
- [ ] Feature importance data loaded
- [ ] Server running on port 8000
- [ ] Dashboard accessible at http://localhost:8000
- [ ] All 7 pages load correctly
- [ ] Charts display data
- [ ] Bulk prediction works
- [ ] CSV export works

---

**System Status**: ✅ Production Ready

**Last Updated**: March 2024
