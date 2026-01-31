# 📚 Wiki Quiz Generator

A full-stack web application that automatically generates interactive quizzes from Wikipedia articles using AI/LLM technology.

## Overview

Wiki Quiz Generator combines web scraping, AI/LLM integration, and a modern web interface to create an engaging learning experience. Users provide Wikipedia article URLs, and the system automatically:

1. Scrapes and extracts article content
2. Identifies key entities, sections, and summary
3. Generates relevant quiz questions using Google Gemini API
4. Suggests related topics for further reading
5. Stores everything in a PostgreSQL database for historical access

## Features

### ✅ Core Features

- **Tab 1 - Generate Quiz**: Input Wikipedia URLs and receive structured quiz output
- **Tab 2 - History**: Browse previously generated quizzes with delete capability
- **Quiz Display**: 
  - Article summary, key entities, and sections
  - 5-8 multiple-choice questions (easy/medium/hard difficulty)
  - Explanations for correct answers
  - Related Wikipedia topics for further reading
- **Quiz Mode**: 
  - Take-quiz interface with hidden answers
  - Score calculation upon submission
  - Visual feedback for correct/incorrect answers
  - Retry functionality

### 🚀 Bonus Features Implemented

- ✅ URL validation before processing
- ✅ Caching to prevent duplicate scraping
- ✅ Raw HTML storage for reference
- ✅ Take Quiz mode with user scoring
- ✅ Section-wise content display
- ✅ Comprehensive error handling

## Project Structure

```
wiki-quiz/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── database.py             # Database setup
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── scraper.py              # Wikipedia scraping logic
│   ├── llm_service.py          # LLM/LangChain integration
│   ├── crud.py                 # Database operations
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment template
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js              # Main app component
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── GenerateQuiz.js   # Quiz generation tab
│   │       ├── GenerateQuiz.css
│   │       ├── QuizDisplay.js    # Quiz display & quiz mode
│   │       ├── QuizDisplay.css
│   │       ├── QuizHistory.js    # History tab
│   │       ├── QuizHistory.css
│   │       ├── QuizModal.js      # Details modal
│   │       └── QuizModal.css
│   └── package.json
├── sample_data/
│   ├── alan_turing_quiz.json
│   └── python_quiz.json
├── PROMPT_TEMPLATES.md         # LangChain prompt documentation
└── README.md                   # This file
```

## Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Web Scraping**: BeautifulSoup4
- **AI/LLM**: Google Generative AI (Gemini) via LangChain
- **API Format**: RESTful JSON

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Styling**: CSS3 (no external UI frameworks)
- **Build Tool**: Create React App

### Database
- **Engine**: PostgreSQL
- **Tables**: `wiki_quizzes` (stores all quiz data with caching support)

## Setup & Installation

### Prerequisites

- Python 3.8+ (backend)
- Node.js 14+ (frontend)
- PostgreSQL 12+ (database)
- Google Gemini API Key (free tier available)

### Backend Setup

1. **Clone the repository and navigate to backend**:
```bash
cd backend
```

2. **Create Python virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```
DATABASE_URL=postgresql://username:password@localhost:5432/wiki_quiz_db
GEMINI_API_KEY=your_api_key_from_google
DEBUG=True
```

5. **Create PostgreSQL database**:
```bash
createdb wiki_quiz_db
```

6. **Run backend server**:
```bash
python main.py
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Create `.env` file** (optional, for custom API URL):
```
REACT_APP_API_URL=http://localhost:8000
```

4. **Start development server**:
```bash
npm start
```

Frontend will open at `http://localhost:3000`

## API Endpoints

### Generate Quiz
**POST** `/api/quiz/generate`
- **Request**:
  ```json
  {
    "url": "https://en.wikipedia.org/wiki/Alan_Turing"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "id": 1,
    "url": "...",
    "title": "...",
    "summary": "...",
    "key_entities": {...},
    "sections": [...],
    "quiz": [...],
    "related_topics": [...],
    "created_at": "...",
    "is_cached": false
  }
  ```

### Get Quiz Details
**GET** `/api/quiz/{quiz_id}`
- Returns full quiz details with all metadata

### List All Quizzes
**GET** `/api/quiz/list?skip=0&limit=100`
- Returns paginated list of quizzes

### Delete Quiz
**DELETE** `/api/quiz/{quiz_id}`
- Removes quiz from database

### Health Check
**GET** `/api/health`
- Returns server status and LLM initialization status

## Auth & Per-user History

This project now supports user registration and login with email/password. Generated quizzes are tied to authenticated users so each user sees only their own history.

Backend env vars in `backend/.env` (or copy `backend/.env.example`):

```
JWT_SECRET_KEY=change-me-to-a-secure-random-value
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Frontend env example (copy `frontend/.env.example`):

```
REACT_APP_API_URL=http://localhost:8000
```

Quick setup (backend):

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py   # or use .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

**Note**: The backend will create DB tables on startup. Use `DATABASE_URL` in `.env` to point to your PostgreSQL instance. The `GET /api/history` endpoint returns the authenticated user's quiz history and requires a bearer token from `/api/auth/login`.


## LangChain Prompt Templates

See [PROMPT_TEMPLATES.md](./PROMPT_TEMPLATES.md) for detailed documentation on:
- Quiz generation prompt design
- Related topics suggestion template
- Hallucination mitigation strategies
- Response validation logic
- Token efficiency considerations

### Key Prompts Used

**Quiz Generation**:
- Instructs LLM to generate 5-8 questions grounded in article content
- Enforces 4 multiple-choice options per question
- Requires difficulty levels (easy/medium/hard)
- Demands JSON-only output for parsing

**Related Topics**:
- Generates diverse, real Wikipedia topics
- Validates suggestions are relevant to article
- Returns JSON array format

## Database Schema

### `wiki_quizzes` Table

```sql
CREATE TABLE wiki_quizzes (
  id SERIAL PRIMARY KEY,
  url VARCHAR UNIQUE NOT NULL,
  title VARCHAR NOT NULL,
  summary TEXT,
  key_entities JSON,
  sections JSON,
  quiz JSON NOT NULL,
  related_topics JSON,
  raw_html TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  is_cached BOOLEAN DEFAULT FALSE
);
```

**Fields**:
- `id`: Auto-incremented primary key
- `url`: Unique Wikipedia URL (prevents duplicate processing)
- `title`, `summary`: Article metadata
- `key_entities`: Extracted people, organizations, locations (JSON)
- `sections`: Article sections list (JSON)
- `quiz`: Generated quiz questions (JSON array)
- `related_topics`: Suggested topics (JSON array)
- `raw_html`: Original page HTML (for reference)
- `created_at`, `updated_at`: Timestamps
- `is_cached`: Indicates if result is from cache

## Sample Data

Two example quiz outputs are provided in `sample_data/`:

1. **alan_turing_quiz.json** - Demonstrates quiz from Alan Turing Wikipedia page
2. **python_quiz.json** - Demonstrates quiz from Python programming language page

These show:
- Correctly structured JSON responses
- Quiz questions grounded in article content
- Proper difficulty distribution
- Relevant related topics
- Entity extraction accuracy

## Testing

### Manual Testing Steps

1. **Start both backend and frontend**

2. **Test Quiz Generation (Tab 1)**:
   - Enter valid Wikipedia URL: `https://en.wikipedia.org/wiki/Climate_change`
   - Click "Generate Quiz"
   - Verify quiz generates with 5-8 questions
   - Verify article metadata displays correctly
   - Test "Take Quiz" mode:
     - Select answers
     - Click "Submit Answers"
     - Verify score calculation
     - Try alternate answers

3. **Test History (Tab 2)**:
   - Click "History" tab
   - Verify previously generated quizzes appear
   - Click "Details" button
   - Verify quiz displays in modal correctly
   - Test "Delete" button
   - Verify quiz removed from list

4. **Error Handling**:
   - Test invalid URL: `https://example.com`
   - Verify error message displays
   - Test network error by stopping backend
   - Verify graceful error handling

### Testing URLs

Recommended Wikipedia pages for testing:
- `https://en.wikipedia.org/wiki/Alan_Turing`
- `https://en.wikipedia.org/wiki/Python_(programming_language)`
- `https://en.wikipedia.org/wiki/Climate_change`
- `https://en.wikipedia.org/wiki/Artificial_intelligence`
- `https://en.wikipedia.org/wiki/Quantum_computing`

## Error Handling

The application handles:

✅ **Invalid Wikipedia URLs** - Validates domain and /wiki/ path
✅ **Network Failures** - Try-catch blocks around all API calls
✅ **Parsing Errors** - JSON validation for LLM responses
✅ **Missing Sections** - Graceful degradation if sections not found
✅ **Database Errors** - Rollback transactions on failure
✅ **LLM Errors** - Detailed error messages to frontend
✅ **Cache Validation** - Checks for existing URLs before reprocessing

## Deployment

### Backend Deployment (Heroku/Render)

```bash
# Create Procfile
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app" > Procfile

# Deploy to Render/Heroku
git push heroku main
```

### Frontend Deployment (Vercel/Netlify)

```bash
npm run build
# Deploy the build/ folder to Vercel or Netlify
```

## Environment Variables

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@host:port/database
GEMINI_API_KEY=your_google_gemini_api_key
DEBUG=True
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:8000
# Or for production:
REACT_APP_API_URL=https://api.yourproduction.com
```

## Troubleshooting

### Backend Issues

**PostgreSQL Connection Error**:
```
ERROR: could not translate host name
```
Solution: Verify PostgreSQL is running and DATABASE_URL is correct

**GEMINI_API_KEY not set**:
```
Error initializing QuizGenerator
```
Solution: Add valid Gemini API key to .env file

**Port 8000 already in use**:
```
Address already in use
```
Solution: Change port in main.py or kill process on port 8000

### Frontend Issues

**CORS Error**:
```
Access to XMLHttpRequest blocked by CORS
```
Solution: Verify backend CORS configuration allows frontend origin

**API connection timeout**:
```
Network error
```
Solution: Verify backend is running at correct URL in .env

## Performance Optimization

- **Caching**: Same URL returns cached result instead of re-scraping
- **Text Truncation**: Article content limited to 5000 chars for LLM efficiency
- **Pagination**: History view supports limit/offset for scalability
- **Token Efficiency**: ~2500 tokens per quiz generation (well within free tier)

## Future Enhancements

- [ ] Multi-language Wikipedia support
- [ ] Advanced search for finding Wikipedia articles
- [ ] User authentication and personal quiz history
- [ ] Leaderboard with quiz scores
- [ ] Custom difficulty filtering
- [ ] Export quizzes (PDF, CSV)
- [ ] Collaborative quiz creation
- [ ] Mobile app (React Native)
- [ ] WebSocket support for real-time updates

## Security Considerations

- ✅ SQL injection prevention (SQLAlchemy parameterized queries)
- ✅ CORS configured appropriately
- ✅ Input validation on all endpoints
- ✅ API key stored in environment variables (never in code)
- ✅ HTTPS recommended for production

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review [PROMPT_TEMPLATES.md](./PROMPT_TEMPLATES.md) for LLM details
3. Check sample data in `sample_data/` folder
4. Review API response format in sample outputs

## Contributors

Created as a demonstration of modern full-stack development with AI integration.

---

**Last Updated**: January 31, 2026
**Status**: Ready for Production
