# ⚡ Quick Start Guide - Wiki Quiz Generator

Get the Wiki Quiz app running in 5 minutes!

## Option 1: Using Docker (Easiest)

### Prerequisites
- Docker and Docker Compose installed
- Gemini API key (get free at https://makersuite.google.com/app/apikey)

### Steps

```bash
# 1. Clone and navigate
cd /home/user/wiki\ quizz

# 2. Create .env file
cat > backend/.env << EOF
DATABASE_URL=postgresql://user:password@postgres:5432/wiki_quiz_db
GEMINI_API_KEY=your_api_key_here
DEBUG=True
EOF

# 3. Start all services
docker-compose up

# 4. Open browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

That's it! 🎉

---

## Option 2: Manual Setup (5-10 min)

### Step 1: Get Gemini API Key
- Visit https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key

### Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `backend/.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/wiki_quiz_db
GEMINI_API_KEY=paste_your_api_key_here
DEBUG=True
```

### Step 3: Setup Database

```bash
# Create database
createdb wiki_quiz_db

# Verify
psql wiki_quiz_db -c "SELECT 1;"
```

### Step 4: Start Backend

```bash
cd backend
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 5: Setup Frontend

In a **new terminal**:

```bash
cd frontend
npm install
npm start
```

Frontend will open at http://localhost:3000

---

## Quick Test

### 1. Generate a Quiz

1. Open http://localhost:3000
2. Enter URL: `https://en.wikipedia.org/wiki/Alan_Turing`
3. Click "Generate Quiz"
4. Wait 10-15 seconds...
5. Quiz appears! 🎉

### 2. Take the Quiz

- Select answer for each question
- Click "Submit Answers"
- See your score!

### 3. Check History

- Click "History" tab
- See all generated quizzes
- Click "Details" to view any quiz

---

## Troubleshooting

### Backend won't start - "Address already in use"
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
python main.py
```

### Database connection error
```bash
# Check PostgreSQL is running
psql -U user -d wiki_quiz_db

# Create database if missing
createdb wiki_quiz_db
```

### Gemini API errors
- Verify API key is correct
- Check it starts with `AIzaSy...`
- Create new key if unsure

### Frontend can't reach backend
- Verify backend is running on port 8000
- Check REACT_APP_API_URL in frontend/.env
- Clear browser cache (Ctrl+Shift+Delete)

### Quiz won't generate
- Check internet connection
- Verify Wikipedia URL is valid
- Check backend logs for errors

---

## Next Steps

1. **Explore the code**:
   - Backend: `backend/main.py`
   - Frontend: `frontend/src/App.js`

2. **Read full documentation**:
   - README.md - Complete overview
   - DEVELOPMENT.md - Dev guide
   - TESTING.md - Test procedures

3. **Customize**:
   - Edit prompts in `backend/llm_service.py`
   - Style in `frontend/src/components/*.css`
   - Add features to `backend/main.py`

4. **Deploy**:
   - See README.md for deployment steps

---

## Useful Commands

```bash
# Backend
python main.py                          # Start server
curl http://localhost:8000/api/health  # Health check
psql wiki_quiz_db                       # Access database

# Frontend
npm start                               # Dev server
npm run build                           # Production build
npm test                                # Run tests

# Database
psql -U user -d wiki_quiz_db            # Connect
SELECT * FROM wiki_quizzes LIMIT 5;     # View quizzes
DELETE FROM wiki_quizzes WHERE id = 1;  # Delete quiz
```

---

## File Structure

```
📁 wiki-quiz/
├── 📄 README.md              ← Full documentation
├── 📄 QUICK_START.md         ← This file
├── 📄 DEVELOPMENT.md         ← Dev guide
├── 📄 TESTING.md             ← Test procedures
├── 📄 PROMPT_TEMPLATES.md    ← LLM prompts
├── 🐳 docker-compose.yml     ← Docker setup
│
├── 📂 backend/
│   ├── main.py               ← FastAPI app
│   ├── llm_service.py        ← LLM integration
│   ├── scraper.py            ← Web scraping
│   ├── requirements.txt       ← Dependencies
│   └── .env.example          ← Config template
│
├── 📂 frontend/
│   ├── src/App.js            ← Main component
│   ├── package.json          ← Dependencies
│   └── public/index.html     ← Entry point
│
└── 📂 sample_data/
    ├── alan_turing_quiz.json ← Example output
    └── python_quiz.json      ← Example output
```

---

## Performance Tips

- ⚡ First quiz generation: 5-15 seconds (Gemini API)
- ⚡ Cached quiz: <1 second
- ⚡ History load: <500ms
- 💾 Database: PostgreSQL (fast queries)

---

## Support

**Stuck?** Check:
1. Backend logs for errors
2. Browser DevTools console (F12)
3. README.md troubleshooting section
4. TESTING.md for expected behavior

---

**Ready to go!** 🚀

Next: Open http://localhost:3000 and start generating quizzes!
