# Quick Start Guide

## For Anyone Cloning This Repository

### Method 1: Docker (Easiest - Recommended)

```bash
# Clone repository
git clone https://github.com/adeline-pepela/Module-6.git
cd "Module-6/deployment"

# Deploy (choose your OS)
./scripts/deploy.sh          # Linux/Mac
# OR
scripts\deploy.bat           # Windows
```

**That's it!** Access: http://localhost:8000

**Prerequisites:**
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually included with Docker)

**Time:** 5-10 minutes first run, 30 seconds after that

---

### Method 2: Manual Setup (Advanced)

### 1️. Clone & Navigate
```bash
git clone https://github.com/adeline-pepela/Module-6.git

```

### 2️. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### 3️. Install Dependencies
```bash
pip install --upgrade pip
pip install -r deployment/requirements.txt
```

### 4️. Setup Database
```bash
cd deployment/backend

# Create tables
python -c "from app.database.database import engine, Base; from app.database.models import *; Base.metadata.create_all(bind=engine)"

# Load data
python -m app.database.load_data
python -m app.database.generate_predictions
python -m app.database.save_model_comparison
python -m app.database.save_feature_importance
```

### 5️. Start Application
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6️⃣ Access Dashboard
Open: **http://localhost:8000**

---

## ✅ Verify Installation

```bash
# Check Python version (should be 3.8+)
python --version

# Check virtual environment is activated
which python  # Should show path with 'venv'

# Test database
python -c "from app.database.database import SessionLocal; db = SessionLocal(); print('✓ Database OK'); db.close()"

# Test API
curl http://localhost:8000/api/dashboard/metrics
```

---

## 📦 What's Included

- ✅ Trained ML model (896KB)
- ✅ 8,436 real customer records
- ✅ FastAPI backend with 15+ endpoints
- ✅ Interactive web dashboard (7 pages)
- ✅ Bulk prediction system
- ✅ Complete documentation

---

## 🆘 Need Help?

See full documentation in:
- `README.md` - Complete setup guide
- `deployment/DEPLOYMENT_GUIDE.md` - Detailed deployment instructions
- `deployment/BULK_PREDICTION_FORMAT.md` - CSV format guide

---

## 📊 Expected Results

After setup:
- Total Customers: 8,436
- Predictions Generated: 8,436
- High Risk Customers: 7
- Medium Risk: 255
- Low Risk: 8,174
- Models Compared: 11
- Features Tracked: 22

---

**Time to Complete**: ~10 minutes

**Author**: Adeline Makokha | Adm No: 191199
