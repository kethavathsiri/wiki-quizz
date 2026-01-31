# 📚 Wiki Quiz Generator - Complete Documentation Index

Welcome to the Wiki Quiz Generator! This document indexes all available resources.

---

## 🚀 Getting Started (Pick One)

### For First-Time Users
Start here → **[QUICK_START.md](./QUICK_START.md)** (5 minutes)
- Docker setup (easiest)
- Manual setup
- Quick test

### For Complete Overview
Read → **[README.md](./README.md)** (comprehensive)
- Full feature list
- Architecture overview
- All setup options
- Troubleshooting

### For Developers
See → **[DEVELOPMENT.md](./DEVELOPMENT.md)**
- Development workflow
- Code structure
- Debugging tips
- Testing setup

---

## 📖 Documentation by Topic

### Setup & Deployment

| Document | Purpose | When to Use |
|----------|---------|------------|
| [QUICK_START.md](./QUICK_START.md) | Get running in 5 min | First time |
| [DEVELOPMENT.md](./DEVELOPMENT.md) | Development workflow | During dev |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Production deployment | Ready to deploy |
| [TESTING.md](./TESTING.md) | Test procedures | QA phase |

### Technical Reference

| Document | Purpose | When to Use |
|----------|---------|------------|
| [API.md](./API.md) | REST endpoints | Building integrations |
| [PROMPT_TEMPLATES.md](./PROMPT_TEMPLATES.md) | LLM prompts | Customizing quiz gen |
| [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) | Project overview | Understanding scope |

### Code Files

| File | Purpose | Location |
|------|---------|----------|
| Backend code | FastAPI application | `/backend/` |
| Frontend code | React app | `/frontend/src/` |
| Sample data | Example outputs | `/sample_data/` |

---

## ✅ Quick Navigation

### I want to...

**Get the app running**
→ [QUICK_START.md](./QUICK_START.md)

**Understand the features**
→ [README.md](./README.md)

**Test the application**
→ [TESTING.md](./TESTING.md)

**Deploy to production**
→ [DEPLOYMENT.md](./DEPLOYMENT.md)

**Learn about the API**
→ [API.md](./API.md)

**Customize quiz generation**
→ [PROMPT_TEMPLATES.md](./PROMPT_TEMPLATES.md)

**Develop new features**
→ [DEVELOPMENT.md](./DEVELOPMENT.md)

**See project details**
→ [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)

---

## 📂 Directory Structure

```
wiki-quiz/
├── 📄 README.md                 ← Start here for overview
├── 📄 QUICK_START.md            ← Get running in 5 min
├── 📄 DEVELOPMENT.md            ← Development guide
├── 📄 TESTING.md                ← Test procedures
├── 📄 DEPLOYMENT.md             ← Production guide
├── 📄 API.md                    ← API reference
├── 📄 PROMPT_TEMPLATES.md       ← LLM prompt design
├── 📄 PROJECT_SUMMARY.md        ← Project overview
├── 📄 INDEX.md                  ← This file
│
├── 🐳 docker-compose.yml
├── 📄 setup.sh
├── 📄 .gitignore
│
├── 📂 backend/                  ← Python/FastAPI
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
│
├── 📂 frontend/                 ← React
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── ...
│
└── 📂 sample_data/              ← Example outputs
    ├── alan_turing_quiz.json
    ├── python_quiz.json
    └── example_urls.txt
```

---

## 🎯 Common Tasks

### Task: Set Up Local Development

1. Read: [QUICK_START.md](./QUICK_START.md)
2. Run setup script: `chmod +x setup.sh && ./setup.sh`
3. Start backend & frontend
4. Visit http://localhost:3000

### Task: Add New Feature

1. Read: [DEVELOPMENT.md](./DEVELOPMENT.md)
2. Modify backend: `/backend/main.py`
3. Update frontend: `/frontend/src/`
4. Test with [TESTING.md](./TESTING.md) procedures

### Task: Deploy to Production

1. Read: [DEPLOYMENT.md](./DEPLOYMENT.md)
2. Choose platform (Render, Heroku, AWS)
3. Follow step-by-step guide
4. Set environment variables

### Task: Customize Quiz Generation

1. Read: [PROMPT_TEMPLATES.md](./PROMPT_TEMPLATES.md)
2. Edit: `/backend/llm_service.py`
3. Update prompt templates
4. Test with new URLs

### Task: Integrate with External System

1. Read: [API.md](./API.md)
2. Use endpoint: `POST /api/quiz/generate`
3. Handle response JSON
4. Store quiz data as needed

---

## 📊 Feature Overview

### Frontend Features
- ✅ Tab 1: Generate quizzes from Wikipedia URLs
- ✅ Tab 2: View history of generated quizzes
- ✅ Quiz mode with answer selection
- ✅ Score calculation
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Modal details view

### Backend Features
- ✅ Wikipedia URL scraping
- ✅ Content extraction (entities, sections, summary)
- ✅ LLM-powered quiz generation
- ✅ Related topics suggestion
- ✅ Database caching
- ✅ REST API with error handling

### Database Features
- ✅ PostgreSQL storage
- ✅ URL uniqueness for caching
- ✅ JSON fields for structured data
- ✅ Timestamp tracking
- ✅ Efficient indexing

---

## 🔍 Find Documentation By Section

### Setup & Installation
- [QUICK_START.md](./QUICK_START.md) - Fast setup
- [README.md](./README.md#setup--installation) - Detailed setup
- [DEVELOPMENT.md](./DEVELOPMENT.md#quick-start-for-development) - Dev setup
- [docker-compose.yml](./docker-compose.yml) - Docker config

### Running the App
- [QUICK_START.md](./QUICK_START.md#quick-test) - Quick test
- [DEVELOPMENT.md](./DEVELOPMENT.md#running-the-application) - Dev mode
- [README.md](./README.md#running-the-application) - Production mode

### Testing
- [TESTING.md](./TESTING.md) - Complete test guide
- [README.md](./README.md#testing) - Basic testing
- [backend/tests.py](./backend/tests.py) - Unit tests

### Deployment
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [README.md](./README.md#deployment) - Deployment basics
- [docker-compose.yml](./docker-compose.yml) - Docker deployment

### API Reference
- [API.md](./API.md) - Complete API docs
- [README.md](./README.md#api-endpoints) - Endpoint summary

### Troubleshooting
- [README.md](./README.md#troubleshooting) - Common issues
- [DEVELOPMENT.md](./DEVELOPMENT.md#common-issues--fixes) - Dev issues
- [DEPLOYMENT.md](./DEPLOYMENT.md#troubleshooting-production-issues) - Production issues

---

## 💡 Tips & Best Practices

### Before Running
- [ ] Verify PostgreSQL is installed and running
- [ ] Get Gemini API key from Google
- [ ] Clone repository or navigate to project folder
- [ ] Review [QUICK_START.md](./QUICK_START.md) once

### While Developing
- [ ] Use virtual environment (Python)
- [ ] Check backend/frontend logs for errors
- [ ] Test with sample URLs from [sample_data/](./sample_data/example_urls.txt)
- [ ] Run tests from [TESTING.md](./TESTING.md)

### Before Deploying
- [ ] Read [DEPLOYMENT.md](./DEPLOYMENT.md) completely
- [ ] Test in development environment
- [ ] Set production environment variables
- [ ] Verify database backups work
- [ ] Enable monitoring/logging

### For Production
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Set up automated backups
- [ ] Monitor API metrics
- [ ] Implement rate limiting

---

## 📞 Getting Help

### Documentation
1. Check the [README.md](./README.md) troubleshooting section
2. See [DEVELOPMENT.md](./DEVELOPMENT.md#troubleshooting) for dev issues
3. Review [DEPLOYMENT.md](./DEPLOYMENT.md#troubleshooting-production-issues) for production issues

### Code Issues
1. Check backend logs: `uvicorn main:app --reload`
2. Check frontend console: F12 in browser
3. Verify environment variables: `echo $GEMINI_API_KEY`
4. Test API directly: `curl http://localhost:8000/api/health`

### Database Issues
1. Test connection: `psql wiki_quiz_db`
2. Check tables: `\dt` in psql
3. View logs: Check PostgreSQL logs
4. Reset database: `dropdb wiki_quiz_db && createdb wiki_quiz_db`

---

## 🔗 External Resources

### Technologies Used
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Learning Resources
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Tutorial](https://react.dev/learn)
- [Web Scraping with BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [SQL Tutorials](https://www.w3schools.com/sql/)

---

## 📋 Document Checklist

### User Documentation
- ✅ README.md - Complete overview
- ✅ QUICK_START.md - Fast setup guide
- ✅ PROJECT_SUMMARY.md - Project details

### Developer Documentation
- ✅ DEVELOPMENT.md - Development workflow
- ✅ API.md - API reference
- ✅ PROMPT_TEMPLATES.md - LLM prompt design

### Operations Documentation
- ✅ TESTING.md - Test procedures
- ✅ DEPLOYMENT.md - Production deployment
- ✅ INDEX.md - This file

### Configuration Files
- ✅ .env.example - Environment template
- ✅ docker-compose.yml - Docker setup
- ✅ Dockerfile - Container definitions
- ✅ .gitignore - Git exclusions

### Sample Data
- ✅ alan_turing_quiz.json - Example quiz
- ✅ python_quiz.json - Example quiz
- ✅ example_urls.txt - Test URLs

---

## 🎓 Learning Paths

### Path 1: Just Want to Use It
1. [QUICK_START.md](./QUICK_START.md)
2. Try the app
3. Generate a few quizzes
4. Done! ✅

### Path 2: Want to Understand It
1. [README.md](./README.md)
2. [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)
3. Browse code in `/backend/` and `/frontend/`
4. Read [API.md](./API.md)

### Path 3: Want to Develop It
1. [DEVELOPMENT.md](./DEVELOPMENT.md)
2. Set up environment
3. Read code in `/backend/` and `/frontend/`
4. Follow [TESTING.md](./TESTING.md)
5. Make changes and test

### Path 4: Want to Deploy It
1. [DEPLOYMENT.md](./DEPLOYMENT.md)
2. Choose platform
3. Follow step-by-step guide
4. Configure environment
5. Deploy and monitor

---

## 📅 Document Versions

| Document | Last Updated | Version |
|----------|--------------|---------|
| README.md | Jan 31, 2026 | 1.0.0 |
| QUICK_START.md | Jan 31, 2026 | 1.0.0 |
| DEVELOPMENT.md | Jan 31, 2026 | 1.0.0 |
| TESTING.md | Jan 31, 2026 | 1.0.0 |
| DEPLOYMENT.md | Jan 31, 2026 | 1.0.0 |
| API.md | Jan 31, 2026 | 1.0.0 |
| PROMPT_TEMPLATES.md | Jan 31, 2026 | 1.0.0 |
| PROJECT_SUMMARY.md | Jan 31, 2026 | 1.0.0 |
| INDEX.md | Jan 31, 2026 | 1.0.0 |

---

## ✨ Key Takeaways

1. **Start Simple**: Use [QUICK_START.md](./QUICK_START.md) to get running
2. **Read Documentation**: Each guide covers a specific aspect
3. **Test Thoroughly**: [TESTING.md](./TESTING.md) has complete procedures
4. **Deploy Safely**: [DEPLOYMENT.md](./DEPLOYMENT.md) covers all platforms
5. **Learn as You Go**: Read relevant docs when needed

---

## 🎉 Ready to Start?

→ **Open [QUICK_START.md](./QUICK_START.md) now and get running in 5 minutes!**

---

**Project**: Wiki Quiz Generator  
**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: January 31, 2026

For the best experience, start with [QUICK_START.md](./QUICK_START.md)!
