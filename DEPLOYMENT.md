# 🚀 Wiki Quiz Generator - Deployment Guide

Complete guide for deploying to production.

## Overview

This guide covers deploying Wiki Quiz Generator to:
- Backend: Render, Heroku, or AWS
- Frontend: Vercel, Netlify, or AWS S3 + CloudFront
- Database: AWS RDS or managed PostgreSQL

---

## Prerequisites

- Frontend built (`npm run build`)
- Backend ready for production
- PostgreSQL database set up
- Gemini API key with production limits verified
- Domain name (optional)
- SSL certificate (auto-provisioned by most platforms)

---

## Option 1: Deploy to Render (Easiest)

### Backend Deployment

1. **Push code to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Create Render account**: https://render.com

3. **Create Backend Service**:
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Name**: wiki-quiz-backend
     - **Runtime**: Python 3.11
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && python main.py`
     - **Instance Type**: Free (or Starter+)

4. **Add Environment Variables**:
   - `DATABASE_URL`: PostgreSQL connection string (Render PostgreSQL)
   - `GEMINI_API_KEY`: Your Gemini API key
   - `DEBUG`: False

5. **Create PostgreSQL Database** (in Render):
   - Click "New +"
   - Select "PostgreSQL"
   - Configure:
     - **Name**: wiki-quiz-db
     - **Version**: 15
     - **Instance Type**: Free (or Starter+)
   - Copy connection string to backend `DATABASE_URL`

6. **Deploy**: Click "Deploy" (automatic)

**Rendered Backend URL**: `https://wiki-quiz-backend.onrender.com`

### Frontend Deployment

1. **Build Production Bundle**:
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel**:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Configure:
     - **Framework**: Create React App
     - **Root Directory**: frontend
     - **Build Command**: `npm run build`
     - **Output Directory**: build
   - Add Environment Variables:
     - `REACT_APP_API_URL`: https://wiki-quiz-backend.onrender.com

3. **Deploy**: Click "Deploy"

**Vercel Frontend URL**: `https://wiki-quiz.vercel.app`

---

## Option 2: Deploy to Heroku

### Prerequisite: Procfile

Create `Procfile` in backend directory:
```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Backend Deployment

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create wiki-quiz-backend

# Add Postgres
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Heroku Backend URL**: `https://wiki-quiz-backend.herokuapp.com`

### Frontend Deployment (Netlify)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
cd frontend
npm run build

# Deploy
netlify deploy --prod --dir build --site-id your_site_id
```

---

## Option 3: AWS Deployment

### Backend (Elastic Beanstalk)

```bash
# Install AWS CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 wiki-quiz

# Create environment
eb create wiki-quiz-prod

# Set environment variables
eb setenv GEMINI_API_KEY=xxx DATABASE_URL=xxx

# Deploy
eb deploy

# View logs
eb logs
```

### Frontend (S3 + CloudFront)

```bash
# Build
npm run build

# Create S3 bucket
aws s3 mb s3://wiki-quiz-frontend

# Upload files
aws s3 sync build/ s3://wiki-quiz-frontend --delete

# CloudFront distribution (use AWS Console)
```

### Database (RDS)

1. Create RDS PostgreSQL instance
2. Configure security groups for Elastic Beanstalk
3. Update `DATABASE_URL` in Elastic Beanstalk

---

## Environment Variables for Production

### Backend

```bash
# Production settings
DATABASE_URL=postgresql://user:password@host:5432/wiki_quiz_db
GEMINI_API_KEY=your_production_key
DEBUG=False
ALLOWED_ORIGINS=https://wiki-quiz.vercel.app

# Optional
MAX_WORKERS=4
LOG_LEVEL=info
CACHE_TTL=86400
```

### Frontend

```bash
REACT_APP_API_URL=https://api.yourproduction.com
REACT_APP_ENVIRONMENT=production
```

---

## SSL/HTTPS Setup

Most platforms provide automatic SSL:
- **Render**: Automatic
- **Vercel**: Automatic
- **Heroku**: Automatic (needs paid dyno)
- **AWS**: Certificate Manager (free)

---

## Database Backup Strategy

### Automated Backups

```bash
# Render: Automatic daily backups (free tier: 7 days)
# Heroku: PG Backups add-on
# AWS RDS: Automated snapshots (configurable retention)

# Manual backup
pg_dump wiki_quiz_db > backup_$(date +%Y%m%d).sql

# Restore
psql wiki_quiz_db < backup_20260131.sql
```

### Backup Script

```bash
#!/bin/bash
# Save as backup.sh

DATABASE_URL=your_connection_string
BACKUP_DIR=./backups

# Create backup
pg_dump "$DATABASE_URL" > "$BACKUP_DIR/wiki_quiz_$(date +%Y%m%d_%H%M%S).sql"

# Upload to S3
aws s3 cp "$BACKUP_DIR" s3://wiki-quiz-backups/ --recursive

# Cleanup old local backups (keep last 7)
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete
```

---

## Monitoring & Logging

### Monitoring Setup

```bash
# Render: Built-in metrics
# Heroku: Papertrail or New Relic
# AWS: CloudWatch

# Add to backend for better logging
pip install python-json-logger

# Use in code
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
```

### Error Tracking

```bash
# Install Sentry
pip install sentry-sdk

# In main.py
import sentry_sdk
sentry_sdk.init("https://examplePublicKey@o0.ingest.sentry.io/0")
```

---

## Performance Optimization

### Backend

```python
# Add caching headers
from fastapi import Response

@app.get("/api/quiz/{quiz_id}")
async def get_quiz(quiz_id: int, response: Response):
    response.headers["Cache-Control"] = "max-age=3600"  # 1 hour
    return quiz

# Database query optimization
db.query(WikiQuiz).filter(...).options(
    selectinload(WikiQuiz.quiz_questions)
).all()
```

### Frontend

```bash
# Production build optimization
npm run build

# Enable gzip compression (most platforms do this)
# Vercel/Netlify: Automatic
# AWS: Use CloudFront with gzip enabled

# Code splitting
React.lazy(() => import('./components/GenerateQuiz'))
```

### Database

```sql
-- Create indexes for faster queries
CREATE INDEX idx_wiki_quizzes_url ON wiki_quizzes(url);
CREATE INDEX idx_wiki_quizzes_created ON wiki_quizzes(created_at);

-- Connection pooling
-- Render/AWS RDS: Built-in
-- Heroku: PgBouncer add-on
```

---

## Cost Optimization

### Free Tier Options

**Render**:
- Free backend tier: limited resources
- Free PostgreSQL: 90 days, 256MB storage
- Free SSL/HTTPS

**Vercel**:
- Free frontend hosting
- Free SSL/HTTPS
- 50GB/month bandwidth

**GitHub**:
- Free code hosting
- Free CI/CD with Actions

**Total Free Cost**: $0/month (with limitations)

### Recommended Paid Plan

```
Render Backend (Starter): $7/month
Render Database (Starter): $15/month
Vercel Frontend: $20/month (optional, free works)
Domain Name: $12/month
CDN: Included

Total: ~$54/month
```

---

## Security Checklist

- [ ] Remove DEBUG=True in production
- [ ] Use strong database passwords
- [ ] Set CORS to specific origin only
- [ ] Enable HTTPS/SSL everywhere
- [ ] Store secrets in environment variables
- [ ] Use managed database (not self-hosted)
- [ ] Enable database backups
- [ ] Monitor API usage
- [ ] Set rate limiting (optional but recommended)
- [ ] Regular security updates

---

## Rollback Procedure

### Render

```bash
# Go to service dashboard
# Click "Timeline"
# Select previous deployment
# Click "Redeploy"
```

### Vercel

```bash
# Go to project dashboard
# Click "Deployments"
# Click "..."  on previous deployment
# Click "Promote to Production"
```

### Git-based (General)

```bash
# Revert to previous commit
git revert <commit_hash>
git push

# Or reset (use carefully)
git reset --hard <commit_hash>
git push --force
```

---

## Monitoring in Production

### Key Metrics to Track

1. **API Response Time**
   - Target: <1 second (cached), <15 seconds (new)
   - Alert if: >20 seconds

2. **Error Rate**
   - Target: <1%
   - Alert if: >5%

3. **Database Performance**
   - Connection count
   - Query latency
   - Backup completion

4. **Frontend Performance**
   - Page load time
   - Core Web Vitals
   - Error tracking

### Using Render Dashboard

```
Service → Metrics tab shows:
- CPU Usage
- Memory Usage
- Network I/O
- Restarts
```

---

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy-render:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy backend
        run: |
          curl -X POST https://api.render.com/deploy/srv-xxx
          # Use Render deploy hook
        env:
          RENDER_DEPLOY_HOOK: ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## Domain Setup

### Using Custom Domain with Vercel

1. Purchase domain (GoDaddy, Namecheap, etc.)
2. In Vercel: Settings → Domains
3. Add domain
4. Update nameservers at registrar
5. DNS automatically configured

### Using Custom Domain with Render

1. Purchase domain
2. In Render: Service → Settings → Custom Domain
3. Add domain
4. Update nameservers
5. Auto SSL provisioned

---

## Troubleshooting Production Issues

### API returns 500 errors

```bash
# Check logs
heroku logs --tail  # Heroku
render logs         # Render

# Common causes:
# - Gemini API key invalid
# - Database connection failed
# - Out of memory

# Fix:
# 1. Verify environment variables
# 2. Restart service
# 3. Scale up resources if needed
```

### Frontend won't load

```bash
# Check:
# 1. Vercel deployment logs
# 2. Browser DevTools → Network tab
# 3. Console errors
# 4. API_URL is correct

# Common causes:
# - Backend URL incorrect
# - CORS misconfigured
# - Build failed
```

### Slow quiz generation

```bash
# Check:
# 1. Gemini API quota
# 2. Database query performance
# 3. Network latency

# Optimize:
# - Enable caching
# - Increase database connections
# - Use CDN for assets
```

---

## Scaling for Growth

### When to Scale

- **Backend**: CPU >80%, Memory >85%
- **Database**: Connections maxed, queries slow
- **Frontend**: Not needed (static files)

### Scaling Options

```bash
# Render: Increase instance type (paid)
# Heroku: Increase dyno size
# AWS: Auto-scaling groups

# Database: Read replicas, connection pooling
# CDN: Already included in most platforms
```

---

## Disaster Recovery Plan

1. **Database**: Automated daily backups (verify working)
2. **Code**: GitHub as source of truth
3. **Secrets**: Stored separately (env variables)
4. **Monitoring**: Alerts for failures
5. **Runbook**: This document

**Recovery Time Objective (RTO)**: <1 hour
**Recovery Point Objective (RPO)**: <24 hours

---

## Maintenance Tasks

### Weekly
- [ ] Check error logs
- [ ] Monitor API usage
- [ ] Verify backups completed

### Monthly
- [ ] Security updates
- [ ] Performance review
- [ ] Cost optimization

### Quarterly
- [ ] Full backup test/restore
- [ ] Disaster recovery drill
- [ ] Capacity planning

---

**Last Updated**: January 31, 2026
**Version**: 1.0.0
