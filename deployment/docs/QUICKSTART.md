# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup
```bash
cd deployment
./start.sh
```

### Step 2: Access Dashboard
Open your browser and navigate to:
```
http://localhost:8000
```

### Step 3: Make Your First Prediction

#### Option A: Single Customer
1. Click on **Prediction** tab
2. Fill in the form:
   - Customer ID: CUST1001
   - Segment: SME
   - Active Subscribers: 50
   - Suspended Subscribers: 5
   - Total Subscribers: 55
   - ARPU: 15000
   - Mobile Revenue: 750000
   - Fix Revenue: 75000
3. Click **Predict Churn**

#### Option B: Batch Upload
1. Use the sample file: `data/sample_batch.csv`
2. Upload in the **Batch Prediction** section
3. Download results

## 📊 Dashboard Sections

### 1. Executive Dashboard
- View overall churn metrics
- Monitor trends and distributions
- Track campaign performance

### 2. Risk Analysis
- Filter customers by risk level
- View at-risk customer list
- Click on any customer for details

### 3. Prediction
- Single customer scoring
- Batch CSV processing
- Real-time results

### 4. Monitoring
- Model performance metrics
- Historical trends
- Drift detection status

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### Model Not Found
```bash
# Copy your trained model
cp path/to/your/best_model.pkl deployment/models/
```

### Dependencies Error
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📝 API Testing

### Using cURL
```bash
# Health check
curl http://localhost:8000/health

# Get dashboard metrics
curl http://localhost:8000/api/dashboard/metrics

# Make prediction
curl -X POST http://localhost:8000/api/prediction/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST1001",
    "segment": "SME",
    "active_subscribers": 50,
    "suspended_subscribers": 5,
    "total_subscribers": 55,
    "arpu": 15000,
    "average_mobile_revenue": 750000,
    "average_fix_revenue": 75000
  }'
```

### Using Python
```python
import requests

# Make prediction
response = requests.post(
    'http://localhost:8000/api/prediction/predict',
    json={
        'customer_id': 'CUST1001',
        'segment': 'SME',
        'active_subscribers': 50,
        'suspended_subscribers': 5,
        'total_subscribers': 55,
        'arpu': 15000,
        'average_mobile_revenue': 750000,
        'average_fix_revenue': 75000
    }
)

print(response.json())
```

## 🎯 Next Steps

1. **Customize**: Update model path and feature names in `predictor.py`
2. **Database**: Connect to your database for real customer data
3. **Authentication**: Add user authentication for production
4. **Deploy**: Use Docker or cloud platform for deployment
5. **Monitor**: Set up logging and alerting

## 💡 Tips

- Use filters in Risk Analysis to focus on specific segments
- Download batch results for offline analysis
- Monitor model performance regularly
- Update retention actions to track campaign effectiveness

## 📞 Need Help?

- Check the full README.md for detailed documentation
- Review API docs at http://localhost:8000/docs
- Check logs for error messages

Happy Predicting! 
