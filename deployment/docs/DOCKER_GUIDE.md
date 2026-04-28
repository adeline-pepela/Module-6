# Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)

### One-Command Deployment

```bash
cd deployment
docker-compose up -d
```

Access: **http://localhost:8000**

---

## What Gets Built

The Docker container includes:
- Python 3.11 slim base image
- FastAPI application
- SQLite database with 8,436 customers
- Trained ML model (896KB)
- All dependencies pre-installed
- Auto-initialization on first run

---

## Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Option 2: Docker CLI

```bash
# Build image
docker build -t churn-prediction:latest .

# Run container
docker run -d \
  --name churn-prediction \
  -p 8000:8000 \
  -v $(pwd)/backend/churn_prediction.db:/app/backend/churn_prediction.db \
  churn-prediction:latest

# View logs
docker logs -f churn-prediction

# Stop container
docker stop churn-prediction
docker rm churn-prediction
```

---

## Configuration

### Environment Variables

Create `.env` file:
```env
DATABASE_URL=sqlite:///./churn_prediction.db
MODEL_PATH=../models/best_model.pkl
PORT=8000
```

Update `docker-compose.yml`:
```yaml
services:
  churn-prediction:
    env_file:
      - .env
```

### Custom Port

```bash
# Change port in docker-compose.yml
ports:
  - "9000:8000"  # Host:Container
```

---

## Database Persistence

Database is persisted via volume mount:
```yaml
volumes:
  - ./backend/churn_prediction.db:/app/backend/churn_prediction.db
```

To reset database:
```bash
docker-compose down
rm backend/churn_prediction.db
docker-compose up -d
```

---

## Monitoring

### Health Check

```bash
# Check container health
docker ps

# Manual health check
curl http://localhost:8000/api/dashboard/metrics
```

### View Logs

```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### Container Stats

```bash
docker stats churn-prediction-app
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Issues

```bash
# Access container shell
docker exec -it churn-prediction-app bash

# Check database
cd /app/backend
python -c "from app.database.database import SessionLocal; db = SessionLocal(); print('OK'); db.close()"
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
```

---

## Updates & Maintenance

### Update Application Code

```bash
git pull
cd deployment
docker-compose up -d --build
```

### Backup Database

```bash
# Copy from container
docker cp churn-prediction-app:/app/backend/churn_prediction.db ./backup.db

# Or use volume mount (already backed up locally)
cp backend/churn_prediction.db backup/churn_prediction_$(date +%Y%m%d).db
```

### Restore Database

```bash
docker-compose down
cp backup.db backend/churn_prediction.db
docker-compose up -d
```

---

## Production Deployment

### AWS ECS

```bash
# Build for ARM64 (Graviton)
docker buildx build --platform linux/arm64 -t churn-prediction:latest .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag churn-prediction:latest <account>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/churn-prediction:latest
```

### Azure Container Instances

```bash
# Login to Azure
az login

# Create container
az container create \
  --resource-group churn-rg \
  --name churn-prediction \
  --image churn-prediction:latest \
  --ports 8000 \
  --dns-name-label churn-prediction
```

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/churn-prediction

# Deploy
gcloud run deploy churn-prediction \
  --image gcr.io/PROJECT_ID/churn-prediction \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Scaling

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml churn

# Scale service
docker service scale churn_churn-prediction=3
```

### Kubernetes

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: churn-prediction
spec:
  replicas: 3
  selector:
    matchLabels:
      app: churn-prediction
  template:
    metadata:
      labels:
        app: churn-prediction
    spec:
      containers:
      - name: churn-prediction
        image: churn-prediction:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: churn-prediction
spec:
  selector:
    app: churn-prediction
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## Security Best Practices

### 1. Use Non-Root User

Add to Dockerfile:
```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 2. Scan for Vulnerabilities

```bash
docker scan churn-prediction:latest
```

### 3. Use Secrets

```bash
docker secret create db_password ./db_password.txt
```

### 4. Enable HTTPS

Use reverse proxy (nginx):
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
```

---

## Performance Optimization

### Multi-Stage Build

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
```

### Resource Limits

```yaml
services:
  churn-prediction:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## Verification

After deployment, verify:

```bash
# Container running
docker ps | grep churn-prediction

# Health check
curl http://localhost:8000/api/dashboard/metrics

# Database loaded
curl http://localhost:8000/api/dashboard/customers | jq '.total'
# Should return: 8436

# Model loaded
docker exec churn-prediction-app ls -lh /app/models/best_model.pkl
# Should show: 896K
```

---

## Docker Commands Cheat Sheet

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Shell access
docker exec -it churn-prediction-app bash

# Remove all
docker-compose down -v --rmi all

# Prune system
docker system prune -a
```

---

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify health: `docker ps`
3. Test API: `curl http://localhost:8000/api/dashboard/metrics`
4. Access shell: `docker exec -it churn-prediction-app bash`

---

**Author**: Adeline Makokha | Adm No: 191199

**Container Size**: ~800MB  
**Startup Time**: ~30 seconds (first run with DB init)  
**Memory Usage**: ~500MB  
**CPU Usage**: <10% idle
