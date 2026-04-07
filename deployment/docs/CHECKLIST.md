# 📋 Deployment Checklist

## Pre-Deployment

### Environment Setup
- [ ] Python 3.8+ installed
- [ ] pip package manager available
- [ ] Virtual environment created
- [ ] All dependencies installed from requirements.txt
- [ ] Model file (best_model.pkl) copied to correct location

### Configuration
- [ ] .env file created from .env.example
- [ ] Model path configured correctly
- [ ] Feature names match training data
- [ ] API host and port configured
- [ ] CORS origins set appropriately

### Testing
- [ ] Health check endpoint works (`/health`)
- [ ] Dashboard loads successfully
- [ ] Single prediction works
- [ ] Batch prediction works
- [ ] All charts render correctly
- [ ] Filters function properly
- [ ] Modal windows open/close
- [ ] API documentation accessible (`/docs`)

## Production Deployment

### Security
- [ ] Authentication implemented
- [ ] API keys configured
- [ ] HTTPS enabled
- [ ] CORS restricted to specific origins
- [ ] Rate limiting added
- [ ] Input validation in place
- [ ] SQL injection prevention
- [ ] XSS protection enabled

### Performance
- [ ] Database connection pooling
- [ ] Caching strategy implemented
- [ ] Static files served efficiently
- [ ] Gzip compression enabled
- [ ] CDN configured for static assets
- [ ] Load balancer set up (if needed)
- [ ] Auto-scaling configured

### Monitoring
- [ ] Application logging configured
- [ ] Error tracking set up (e.g., Sentry)
- [ ] Performance monitoring (e.g., New Relic)
- [ ] Uptime monitoring
- [ ] Alert notifications configured
- [ ] Dashboard analytics tracking

### Backup & Recovery
- [ ] Database backup strategy
- [ ] Model versioning system
- [ ] Disaster recovery plan
- [ ] Rollback procedure documented

### Documentation
- [ ] API documentation complete
- [ ] User guide created
- [ ] Admin guide written
- [ ] Troubleshooting guide available
- [ ] Architecture diagram created

## Post-Deployment

### Validation
- [ ] All features tested in production
- [ ] Performance benchmarks met
- [ ] Security scan completed
- [ ] Load testing performed
- [ ] User acceptance testing done

### Maintenance
- [ ] Monitoring dashboards reviewed daily
- [ ] Logs checked regularly
- [ ] Model performance tracked
- [ ] User feedback collected
- [ ] Regular updates scheduled

## Quick Reference

### Start Application
```bash
cd deployment
./start.sh
```

### Stop Application
```bash
# Press Ctrl+C in terminal
# Or kill process:
lsof -ti:8000 | xargs kill -9
```

### View Logs
```bash
tail -f logs/app.log
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Restart Service
```bash
systemctl restart churn-prediction  # If using systemd
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

#### Model Not Loading
- Check model path in predictor.py
- Verify model file exists
- Check file permissions

#### API Not Responding
- Check if server is running
- Verify firewall settings
- Check CORS configuration

#### Charts Not Displaying
- Check browser console for errors
- Verify Chart.js is loaded
- Check API responses

## Support Contacts

- **Technical Lead**: [Name]
- **DevOps**: [Name]
- **Data Science**: [Name]
- **Product Owner**: [Name]

## Version History

- **v1.0.0** (2024-01-15): Initial deployment
  - Executive dashboard
  - Risk segmentation
  - Real-time prediction
  - Model monitoring

---

**Last Updated**: 2024-01-15  
**Next Review**: 2024-02-15
