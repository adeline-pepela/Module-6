# 🚀 Churn Prediction System - Deployment

Complete deployment package for the Customer Churn Prediction System.

---

## 📦 Quick Start

### One-Command Deployment

**Linux/Mac:**
```bash
./scripts/deploy.sh
```

**Windows:**
```cmd
scripts\deploy.bat
```

**Access:** http://localhost:8000

---

## 📁 Folder Structure

```
deployment/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── database/          # Database models & scripts
│   │   ├── models/            # Pydantic schemas
│   │   └── services/          # ML model service
│   ├── main.py                # Application entry point
│   └── churn_prediction.db    # SQLite database
│
├── frontend/                   # Web interface
│   ├── static/
│   │   ├── css/               # Stylesheets
│   │   └── js/                # JavaScript
│   └── templates/
│       └── index.html         # Main dashboard
│
├── models/                     # ML models
│   └── best_model.pkl         # Trained model (896KB)
│
├── data/                       # Sample data
│   └── sample_batch.csv       # Example CSV
│
├── docs/                       # Documentation
│   ├── DOCKER_README.md       # Docker quick start
│   ├── DOCKER_GUIDE.md        # Comprehensive Docker guide
│   ├── DEPLOYMENT_GUIDE.md    # Detailed deployment
│   ├── BULK_PREDICTION_FORMAT.md  # CSV format
│   ├── DATABASE_GUIDE.md      # Database schema
│   ├── ARCHITECTURE.md        # System architecture
│   ├── REPLICATION_VERIFIED.md    # Test results
│   └── ...                    # More documentation
│
├── scripts/                    # Deployment scripts
│   ├── deploy.sh              # Linux/Mac deployment
│   ├── deploy.bat             # Windows deployment
│   ├── test-docker.sh         # Docker validation
│   ├── create_sample_csv.py   # Generate sample data
│   ├── setup_database.py      # Database setup
│   └── ...                    # More scripts
│
├── Dockerfile                  # Docker container definition
├── docker-compose.yml          # Docker orchestration
├── docker-entrypoint.sh        # Container initialization
├── .dockerignore              # Docker build exclusions
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── bulk_prediction_template.csv   # Sample CSV with real data
└── README.md                  # This file
```

---

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Deploy
```bash
cd deployment
./scripts/deploy.sh
```

### Verify
```bash
curl http://localhost:8000/api/dashboard/metrics
```

### Documentation
See [docs/DOCKER_README.md](docs/DOCKER_README.md)

---

## 🔧 Manual Deployment

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
cd backend
python -m app.database.load_data
python -m app.database.generate_predictions
python -m app.database.save_model_comparison
python -m app.database.save_feature_importance

# Start application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Documentation
See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [DOCKER_README.md](docs/DOCKER_README.md) | Docker quick start guide |
| [DOCKER_GUIDE.md](docs/DOCKER_GUIDE.md) | Comprehensive Docker documentation |
| [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Detailed deployment instructions |
| [BULK_PREDICTION_FORMAT.md](docs/BULK_PREDICTION_FORMAT.md) | CSV format specification |
| [DATABASE_GUIDE.md](docs/DATABASE_GUIDE.md) | Database schema & setup |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture overview |
| [REPLICATION_VERIFIED.md](docs/REPLICATION_VERIFIED.md) | Deployment test results |

---

## 🛠️ Scripts

| Script | Purpose |
|--------|---------|
| `scripts/deploy.sh` | One-command deployment (Linux/Mac) |
| `scripts/deploy.bat` | One-command deployment (Windows) |
| `scripts/test-docker.sh` | Validate Docker setup |
| `scripts/create_sample_csv.py` | Generate sample CSV |
| `scripts/setup_database.py` | Initialize database |

---

## 🎯 What's Included

### Application
- ✅ FastAPI backend with 15+ endpoints
- ✅ Interactive web dashboard (7 pages)
- ✅ SQLite database with 8,436 customers
- ✅ Trained ML model (EasyEnsembleClassifier)
- ✅ Real-time predictions
- ✅ Bulk CSV processing

### Data
- ✅ 8,436 customer records
- ✅ 8,436 predictions
- ✅ 11 model comparisons
- ✅ 22 feature importance scores
- ✅ Confusion matrix data
- ✅ ROC/PR curve data

### Features
- ✅ Dashboard with KPIs
- ✅ Customer search & filter
- ✅ Risk analysis
- ✅ Single prediction
- ✅ Bulk prediction (CSV)
- ✅ Model evaluation
- ✅ Intervention tracking
- ✅ CSV export

---

## 🔍 Verification

After deployment, verify:

```bash
# Container status (Docker)
docker ps | grep churn-prediction

# API test
curl http://localhost:8000/api/dashboard/metrics

# Expected response
{
  "total_customers": 8436,
  "current_churn_rate": 0.0646,
  "predicted_at_risk": 7,
  "revenue_at_risk": 1224.34,
  "prevention_rate": 0.3818,
  "campaign_efficiency": 0.0773
}
```

---

## 📊 System Requirements

### Minimum
- 2 GB RAM
- 2 GB disk space
- Docker 20.10+ (for Docker deployment)
- Python 3.8+ (for manual deployment)

### Recommended
- 4 GB RAM
- 5 GB disk space
- Docker 24.0+
- Python 3.11+

---

## 🆘 Troubleshooting

### Port 8000 in use
```bash
# Change port in docker-compose.yml
ports:
  - "9000:8000"
```

### Docker not running
```bash
# Linux
sudo systemctl start docker

# Mac/Windows
# Start Docker Desktop
```

### Build fails
```bash
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
```

---

## 📞 Support

For issues:
1. Check [docs/DOCKER_GUIDE.md](docs/DOCKER_GUIDE.md)
2. View logs: `docker-compose logs -f`
3. Test API: `curl http://localhost:8000/api/dashboard/metrics`

---

## 🎓 For Dissertation

This deployment demonstrates:
- ✅ Production-ready ML system
- ✅ Containerized deployment
- ✅ Easy replication (one command)
- ✅ Complete documentation
- ✅ Real data integration
- ✅ Interactive visualization

---

**Author**: Adeline Makokha  
**Adm No**: 191199  
**Course**: DSA 8502 Predictive and Optimization Analytics  
**Institution**: Strathmore University

---

## 🚀 Get Started

```bash
cd deployment
./scripts/deploy.sh
```

Open: http://localhost:8000
