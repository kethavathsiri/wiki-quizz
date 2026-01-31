# Wiki Quiz Generator - Development Guide

## Quick Start for Development

### 1. Initial Setup (One Time)

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Gemini API key
```

#### Frontend Setup
```bash
cd frontend
npm install
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb wiki_quiz_db

# Optional: Connect to verify
psql wiki_quiz_db
```

### 3. Running the Application

#### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
python main.py
```
Backend runs on: http://localhost:8000

#### Terminal 2 - Frontend:
```bash
cd frontend
npm start
```
Frontend runs on: http://localhost:3000

### 4. Get Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Create new API key
3. Add to `backend/.env`: `GEMINI_API_KEY=your_key_here`

## Development Workflow

### Testing Quiz Generation

1. Open http://localhost:3000
2. Enter Wikipedia URL: `https://en.wikipedia.org/wiki/Alan_Turing`
3. Click "Generate Quiz"
4. Verify quiz appears with questions, options, and related topics

### Testing Quiz Mode

1. After quiz generates, try selecting answers
2. Click "Submit Answers" to see score
3. Review explanations for each question

### Testing History

1. Generate multiple quizzes with different URLs
2. Switch to "History" tab
3. Click "Details" to view previous quizzes in modal
4. Test "Delete" functionality

## API Testing

### Using cURL or Postman

Generate Quiz:
```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}'
```

List Quizzes:
```bash
curl http://localhost:8000/api/quiz/list
```

Get Specific Quiz:
```bash
curl http://localhost:8000/api/quiz/1
```

Health Check:
```bash
curl http://localhost:8000/api/health
```

## Code Structure

### Backend Modules

- **main.py**: FastAPI app, route handlers, error handling
- **config.py**: Environment and configuration management
- **database.py**: SQLAlchemy setup, session management
- **models.py**: Database ORM models
- **schemas.py**: Pydantic request/response schemas
- **scraper.py**: Wikipedia scraping and text extraction
- **llm_service.py**: LangChain LLM integration
- **crud.py**: Database CRUD operations

### Frontend Components

- **App.js**: Main app with tab navigation
- **GenerateQuiz.js**: Tab 1 - input and form
- **QuizDisplay.js**: Quiz rendering and quiz mode
- **QuizHistory.js**: Tab 2 - history table
- **QuizModal.js**: Modal wrapper for details view

## Common Issues & Fixes

### Backend won't start
```
Address already in use
```
Kill process: `lsof -ti:8000 | xargs kill -9`

### PostgreSQL not found
Install PostgreSQL from https://www.postgresql.org/download/

### Gemini API errors
Check API key is valid and set in .env
Visit https://makersuite.google.com/app/apikey

### CORS errors
Verify CORS is enabled in main.py (already configured)

### Frontend can't reach backend
Check REACT_APP_API_URL in frontend/.env
Verify backend is running on port 8000

## Production Build

### Frontend
```bash
cd frontend
npm run build
# Outputs to frontend/build/
# Deploy to Vercel, Netlify, or static hosting
```

### Backend
```bash
# Add gunicorn to requirements.txt
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## Debugging

### Backend Logs
FastAPI server shows request logs and errors by default

### Frontend Console
Open DevTools (F12) to see console.log() calls and errors

### Database Inspection
```bash
psql wiki_quiz_db
SELECT COUNT(*) FROM wiki_quizzes;
SELECT * FROM wiki_quizzes LIMIT 5;
```

## Performance Tips

- Cache responses to avoid re-scraping same URL
- Limit history pagination to 50 items per page
- Use browser DevTools Network tab to monitor requests
- Check LLM response time - may take 5-10 seconds

## Next Steps

1. Test with various Wikipedia articles
2. Monitor token usage for Gemini API
3. Collect user feedback on question quality
4. Add user authentication for personal histories
5. Deploy to production hosting
