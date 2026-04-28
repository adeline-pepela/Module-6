# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│                     (http://localhost:8000)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    FASTAPI SERVER                            │
│                   (Backend - Port 8000)                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API ROUTES                               │  │
│  │  • /api/dashboard/*    (5 endpoints)                 │  │
│  │  • /api/prediction/*   (3 endpoints)                 │  │
│  │  • /api/monitoring/*   (5 endpoints)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │           BUSINESS LOGIC LAYER                        │  │
│  │  • Request Validation (Pydantic)                      │  │
│  │  • Data Processing                                    │  │
│  │  • Response Formatting                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │           ML SERVICE LAYER                            │  │
│  │  • Model Loading                                      │  │
│  │  • Feature Engineering                                │  │
│  │  • Prediction                                         │  │
│  │  • Feature Importance                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼────────────────────────────────┐  │
│  │           TRAINED ML MODEL                            │  │
│  │  • EasyEnsembleClassifier                            │  │
│  │  • 22 Features                                        │  │
│  │  • SVMSMOTE Sampling                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ Serves
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    FRONTEND (SPA)                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              HTML TEMPLATES                           │  │
│  │  • index.html (Main Dashboard)                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              CSS STYLING                              │  │
│  │  • styles.css (500+ lines)                           │  │
│  │  • Responsive Design                                  │  │
│  │  • Modern Gradients                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              JAVASCRIPT LOGIC                         │  │
│  │  • app.js (400+ lines)                               │  │
│  │  • Axios (API calls)                                  │  │
│  │  • Chart.js (Visualizations)                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Single Prediction Flow
```
User Input → Form Validation → API Request → Preprocessing → 
Model Prediction → Feature Importance → Response Formatting → 
Display Results
```

### 2. Batch Prediction Flow
```
CSV Upload → File Parsing → Batch Processing → 
Multiple Predictions → Results Aggregation → 
CSV Download
```

### 3. Dashboard Data Flow
```
Page Load → API Calls (Parallel) → Data Fetching → 
Chart Rendering → Display Metrics
```

## Component Breakdown

### Backend Components

#### 1. API Layer (`app/api/`)
```
dashboard.py
├── get_dashboard_metrics()
├── get_churn_trend()
├── get_risk_distribution()
├── get_segment_analysis()
├── get_at_risk_customers()
└── get_customer_detail()

prediction.py
├── predict_churn()
├── predict_batch()
└── get_risk_score()

monitoring.py
├── get_model_metrics()
├── get_performance_trend()
├── get_drift_alerts()
├── log_retention_action()
└── get_campaign_performance()
```

#### 2. Service Layer (`app/services/`)
```
predictor.py
├── ChurnPredictor
│   ├── __init__()
│   ├── _load_model()
│   ├── _get_feature_names()
│   ├── preprocess_input()
│   ├── predict()
│   ├── get_feature_importance()
│   └── get_recommended_action()
```

#### 3. Model Layer (`app/models/`)
```
schemas.py
├── RiskLevel (Enum)
├── CustomerSegment (Enum)
├── CustomerInput
├── PredictionResponse
├── DashboardMetrics
├── CustomerDetail
├── RetentionAction
└── ModelMetrics
```

### Frontend Components

#### 1. Sections
```
index.html
├── Navigation Bar
├── Dashboard Section
│   ├── KPI Cards (6)
│   └── Charts (3)
├── Risk Analysis Section
│   ├── Filters
│   └── Customer Table
├── Prediction Section
│   ├── Single Form
│   ├── Result Display
│   └── Batch Upload
└── Monitoring Section
    ├── Model Info
    ├── Performance Metrics
    └── Trend Chart
```

#### 2. JavaScript Functions
```
app.js
├── Navigation
│   └── showSection()
├── Dashboard
│   ├── loadDashboardMetrics()
│   ├── loadChurnTrend()
│   ├── loadRiskDistribution()
│   └── loadSegmentAnalysis()
├── Risk Analysis
│   ├── loadAtRiskCustomers()
│   ├── filterCustomers()
│   └── showCustomerDetail()
├── Prediction
│   ├── predictChurn()
│   ├── batchPredict()
│   └── displayPredictionResult()
└── Monitoring
    ├── loadModelMetrics()
    └── loadPerformanceTrend()
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic 2.5.0
- **ML**: scikit-learn, imbalanced-learn
- **Data**: pandas, numpy

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling, gradients, animations
- **JavaScript**: ES6+, async/await
- **Libraries**: 
  - Chart.js (visualizations)
  - Axios (HTTP client)

### ML Model
- **Algorithm**: EasyEnsembleClassifier
- **Sampling**: SVMSMOTE
- **Features**: 22
- **Performance**: F1=0.42, Recall=0.38

## Security Layers

```
┌─────────────────────────────────────┐
│     Input Validation (Pydantic)     │
├─────────────────────────────────────┤
│     CORS Middleware                 │
├─────────────────────────────────────┤
│     Rate Limiting (TODO)            │
├─────────────────────────────────────┤
│     Authentication (TODO)           │
├─────────────────────────────────────┤
│     HTTPS/TLS (Production)          │
└─────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
    ├── FastAPI Instance 1
    ├── FastAPI Instance 2
    ├── FastAPI Instance 3
    └── FastAPI Instance N
```

### Caching Strategy
```
Request → Cache Check → Cache Hit? 
    ├── Yes → Return Cached
    └── No → Process → Cache → Return
```

### Database Integration (Future)
```
API Layer → ORM (SQLAlchemy) → Database
    ├── Customer Data
    ├── Predictions History
    ├── Retention Actions
    └── Model Metrics
```

## Deployment Architecture

### Development
```
Local Machine → uvicorn --reload → http://localhost:8000
```

### Production
```
Cloud Platform → Docker Container → 
Load Balancer → Multiple Instances → 
Database → Monitoring
```

## Monitoring & Observability

```
Application
    ├── Logs → Log Aggregation
    ├── Metrics → Prometheus/Grafana
    ├── Traces → Jaeger/Zipkin
    └── Alerts → PagerDuty/Slack
```

---

**Architecture Version**: 1.0.0  
**Last Updated**: 2026-01-15  
**Maintained By**: Adeline Makokha
