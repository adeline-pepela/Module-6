# Docker Deployment - Quick Start

## One-Command Deployment

### For Linux/Mac Users
```bash
cd deployment
./deploy.sh
```

### For Windows Users
```cmd
cd deployment
deploy.bat
```

That's it! Your application will be running at **http://localhost:8000**

---

## What Happens Automatically

1. Checks Docker installation
2. Builds Docker image (~5-10 minutes first time)
3. Creates database with 8,436 customers
4. Loads trained ML model
5. Starts web application
6. Initializes all API endpoints

---

## Manual Deployment (Alternative)

If you prefer manual control:

```bash
cd deployment

# Build
docker-compose build

# Start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## Prerequisites

### Install Docker

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Mac:**
Download from: https://docs.docker.com/desktop/install/mac-install/

**Windows:**
Download from: https://docs.docker.com/desktop/install/windows-install/

### Install Docker Compose

Usually included with Docker Desktop. Verify:
```bash
docker-compose --version
```

---

## Verification

After deployment, test these URLs:

### Web Dashboard
```
http://localhost:8000
```

### API Health Check
```bash
curl http://localhost:8000/api/dashboard/metrics
```

Expected response:
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

### API Documentation
```
http://localhost:8000/docs
```

---

## Common Commands

### View Logs
```bash
docker-compose logs -f
```

### Stop Application
```bash
docker-compose down
```

### Restart Application
```bash
docker-compose restart
```

### Rebuild After Changes
```bash
docker-compose up -d --build
```

### Check Container Status
```bash
docker ps
```

### Access Container Shell
```bash
docker exec -it churn-prediction-app bash
```

---

## Troubleshooting

### Port 8000 Already in Use

**Option 1: Stop existing service**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Option 2: Change port**

Edit `docker-compose.yml`:
```yaml
ports:
  - "9000:8000"  # Use port 9000 instead
```

### Docker Daemon Not Running

**Linux:**
```bash
sudo systemctl start docker
```

**Mac/Windows:**
Start Docker Desktop application

### Build Fails

```bash
# Clean everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

### Application Not Responding

```bash
# Check logs
docker-compose logs

# Wait longer (first startup takes 30-60 seconds)
sleep 30
curl http://localhost:8000/api/dashboard/metrics
```

---

## System Requirements

### Minimum
- 2 GB RAM
- 2 GB disk space
- Docker 20.10+
- Docker Compose 2.0+

### Recommended
- 4 GB RAM
- 5 GB disk space
- Docker 24.0+
- Docker Compose 2.20+

---

## What's Included

- FastAPI backend
- SQLite database (8,436 customers)
- Trained ML model (EasyEnsembleClassifier)
- Interactive web dashboard (7 pages)
- 15+ API endpoints
- Automatic database initialization
- Health checks
- Logging

---

## Performance

| Metric | Value |
|--------|-------|
| Container Size | ~800 MB |
| Memory Usage | ~150 MB |
| CPU Usage | <1% |
| Startup Time | 15-30 seconds |
| API Response | <100ms |

---

## Sharing Your Deployment

### Save Image
```bash
docker save deployment_churn-prediction:latest | gzip > churn-prediction.tar.gz
```

### Load on Another Machine
```bash
docker load < churn-prediction.tar.gz
cd deployment
docker-compose up -d
```

---

## Cloud Deployment

### AWS ECS
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag deployment_churn-prediction:latest <account>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:latest
```

### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/churn-prediction
gcloud run deploy churn-prediction --image gcr.io/PROJECT_ID/churn-prediction --platform managed --allow-unauthenticated
```

### Azure Container Instances
```bash
az container create --resource-group churn-rg --name churn-prediction --image deployment_churn-prediction:latest --ports 8000 --dns-name-label churn-prediction
```

---

## Stopping & Cleanup

### Stop Application
```bash
docker-compose down
```

### Remove Everything (including data)
```bash
docker-compose down -v
docker rmi deployment_churn-prediction:latest
```

### Clean Docker System
```bash
docker system prune -a
```

---

## Support

### Check Logs
```bash
docker-compose logs -f
```

### Verify Container
```bash
docker ps -a
docker inspect churn-prediction-app
```

### Test API
```bash
curl -v http://localhost:8000/api/dashboard/metrics
```

---

## Next Steps

1. Deploy with `./deploy.sh` or `deploy.bat`
2. Access http://localhost:8000
3. Explore the 7 dashboard pages
4. Test bulk prediction with CSV upload
5. Review API documentation at /docs
6. Check model evaluation metrics

---

## Files

- `Dockerfile` - Container definition
- `docker-compose.yml` - Orchestration config
- `docker-entrypoint.sh` - Initialization script
- `deploy.sh` - Linux/Mac deployment script
- `deploy.bat` - Windows deployment script
- `.dockerignore` - Build optimization
- `DOCKER_GUIDE.md` - Detailed documentation

---

**Author**: Adeline Makokha  
**Adm No**: 191199  
**Course**: Dissertation

---

## Ready to Deploy!

Run `./deploy.sh` (Linux/Mac) or `deploy.bat` (Windows) and you're done!
