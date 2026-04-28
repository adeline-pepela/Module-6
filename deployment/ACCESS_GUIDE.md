# Access Your Running Docker Application

## Container Status: RUNNING

Your Docker container is already running and healthy!

---

## Access the Application

### Web Dashboard
Open your browser and go to:
```
http://localhost:8000
```

### Alternative URLs
```
http://127.0.0.1:8000
http://0.0.0.0:8000
```

---

## Test the API

### Using Browser
Open any of these URLs in your browser:

**Dashboard Metrics:**
```
http://localhost:8000/api/dashboard/metrics
```

**Customer List:**
```
http://localhost:8000/api/dashboard/customers
```

**Model Comparison:**
```
http://localhost:8000/api/evaluation/model-comparison
```

**API Documentation (Interactive):**
```
http://localhost:8000/docs
```

### Using Command Line

```bash
# Test API
curl http://localhost:8000/api/dashboard/metrics

# Pretty print with jq
curl -s http://localhost:8000/api/dashboard/metrics | jq .

# Test web interface
curl -I http://localhost:8000
```

---

## What You'll See

### Dashboard (http://localhost:8000)
- 6 KPI cards (Total Customers, Churn Rate, etc.)
- 4 Risk buckets (Ultra High, High, Medium, Low)
- 4 Interactive charts
- 7 Navigation pages:
  1. Overview
  2. Customers
  3. Risk Analysis
  4. Predict
  5. Interventions
  6. Model Governance
  7. Model Evaluation

### API Response Example
```json
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

## 🔍 Container Information

### Check Status
```bash
docker ps
```

### View Logs
```bash
docker logs -f churn-prediction-app
```

### Container Stats
```bash
docker stats churn-prediction-app
```

### Stop Container
```bash
docker-compose down
```

### Restart Container
```bash
docker-compose restart
```

---

## Access from Other Devices (Same Network)

### Find Your IP Address

**Linux/Mac:**
```bash
hostname -I | awk '{print $1}'
# OR
ip addr show | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```cmd
ipconfig
```

### Access from Another Device
Replace `YOUR_IP` with your machine's IP address:
```
http://YOUR_IP:8000
```

Example:
```
http://192.168.1.100:8000
```

---

## Features to Try

### 1. Dashboard Overview
- View all KPIs
- See risk distribution
- Check charts with hover tooltips

### 2. Customer Search
- Navigate to "Customers" page
- Search by PID or name
- Filter by segment or risk level
- Export to CSV

### 3. Single Prediction
- Go to "Predict" page
- Fill in customer details
- Get churn probability and risk level
- See top 3 churn drivers

### 4. Bulk Prediction
- Download template: `bulk_prediction_template.csv`
- Fill with customer data
- Upload via "Predict" page
- Download results

### 5. Model Evaluation
- Navigate to "Model Evaluation"
- View 11 model comparison
- See feature importance (22 features)
- Check confusion matrix
- View ROC and PR curves

---

## Useful Commands

### Quick Access
```bash
# Open in default browser (Linux)
xdg-open http://localhost:8000

# Open in default browser (Mac)
open http://localhost:8000

# Open in default browser (Windows)
start http://localhost:8000
```

### Container Management
```bash
# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Rebuild
docker-compose up -d --build

# Check health
docker inspect churn-prediction-app | grep -A 5 Health
```

---

## Screenshots to Take

For your dissertation:
1. Dashboard overview with all KPIs
2. Customer list with filters
3. Risk distribution chart
4. Single prediction result
5. Bulk prediction upload
6. Model comparison table
7. Feature importance chart
8. Confusion matrix
9. ROC curve
10. PR curve

---

## Troubleshooting

### Can't Access http://localhost:8000

**Check if container is running:**
```bash
docker ps | grep churn-prediction
```

**Check logs for errors:**
```bash
docker logs churn-prediction-app
```

**Restart container:**
```bash
docker-compose restart
```

### Port 8000 Already in Use

**Find what's using the port:**
```bash
lsof -i :8000
```

**Kill the process:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Or change port in docker-compose.yml:**
```yaml
ports:
  - "9000:8000"  # Use port 9000 instead
```

---



Your application is running at:
**http://localhost:8000**


