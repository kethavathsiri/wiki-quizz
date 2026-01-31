# 📡 Wiki Quiz Generator - API Documentation

Complete REST API reference for the Wiki Quiz backend.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for current implementation.

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response** (200 OK):
```json
{
  "message": "Wiki Quiz API",
  "version": "1.0.0",
  "endpoints": {
    "generate_quiz": "POST /api/quiz/generate",
    "get_quiz": "GET /api/quiz/{quiz_id}",
    "list_quizzes": "GET /api/quiz/list",
    "delete_quiz": "DELETE /api/quiz/{quiz_id}"
  }
}
```

---

### 2. Generate Quiz

**POST** `/api/quiz/generate`

Generate a new quiz from a Wikipedia article.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Mathison Turing was an English mathematician and computer scientist...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church", "David Hilbert"],
    "organizations": ["University of Cambridge", "Bletchley Park"],
    "locations": ["United Kingdom", "Manchester", "Princeton"]
  },
  "sections": ["Early life", "Mathematical logic", "World War II", "Manchester years"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": [
        "Harvard University",
        "Cambridge University",
        "Oxford University",
        "Princeton University"
      ],
      "answer": "Cambridge University",
      "difficulty": "easy",
      "explanation": "Mentioned in the 'Early life' section."
    }
  ],
  "related_topics": ["Turing Machine", "Enigma Machine", "Computer science"],
  "created_at": "2026-01-31T10:00:00",
  "is_cached": false
}
```

**Error Responses**:

**400 Bad Request** - Invalid URL:
```json
{
  "detail": "Invalid Wikipedia URL"
}
```

**500 Internal Server Error** - LLM service error:
```json
{
  "detail": "Error processing Wikipedia article: LLM service not initialized"
}
```

**Query Parameters**:
- None

**Notes**:
- Processing takes 5-15 seconds for new articles
- Returns immediately (<1 second) if URL already in database (cached)
- Automatically detects and returns existing entries

---

### 3. Get Quiz by ID

**GET** `/api/quiz/{quiz_id}`

Retrieve a specific quiz by ID.

**Path Parameters**:
- `quiz_id` (integer, required): ID of the quiz

**Response** (200 OK):
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "...",
  "key_entities": {...},
  "sections": [...],
  "quiz": [...],
  "related_topics": [...],
  "created_at": "2026-01-31T10:00:00",
  "is_cached": false
}
```

**Error Responses**:

**404 Not Found**:
```json
{
  "detail": "Quiz not found"
}
```

**Example Request**:
```bash
curl http://localhost:8000/api/quiz/1
```

---

### 4. List All Quizzes

**GET** `/api/quiz/list`

List all stored quizzes with pagination.

**Query Parameters**:
- `skip` (integer, optional, default=0): Number of records to skip
- `limit` (integer, optional, default=100): Maximum records to return

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "url": "https://en.wikipedia.org/wiki/Alan_Turing",
    "title": "Alan Turing",
    "created_at": "2026-01-31T10:00:00",
    "is_cached": false
  },
  {
    "id": 2,
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "title": "Python (programming language)",
    "created_at": "2026-01-31T11:00:00",
    "is_cached": true
  }
]
```

**Example Requests**:
```bash
# Get first 10 quizzes
curl http://localhost:8000/api/quiz/list?skip=0&limit=10

# Get quizzes 20-30
curl http://localhost:8000/api/quiz/list?skip=20&limit=10

# Get all (default)
curl http://localhost:8000/api/quiz/list
```

**Notes**:
- Returns list representation only (no full quiz data)
- Use `/api/quiz/{id}` to get full quiz details

---

### 5. Delete Quiz

**DELETE** `/api/quiz/{quiz_id}`

Delete a quiz from the database.

**Path Parameters**:
- `quiz_id` (integer, required): ID of the quiz to delete

**Response** (200 OK):
```json
{
  "message": "Quiz deleted successfully"
}
```

**Error Responses**:

**404 Not Found**:
```json
{
  "detail": "Quiz not found"
}
```

**Example Request**:
```bash
curl -X DELETE http://localhost:8000/api/quiz/1
```

**Notes**:
- Deletes quiz and all associated data from database
- Cannot be undone (implement soft delete if needed)

---

### 6. Health Check

**GET** `/api/health`

Check API health and LLM service status.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "llm_initialized": true
}
```

**Response** (200 OK) - LLM not available:
```json
{
  "status": "healthy",
  "llm_initialized": false
}
```

**Example Request**:
```bash
curl http://localhost:8000/api/health
```

---

## Data Models

### WikiQuiz

```json
{
  "id": 1,
  "url": "string (unique, required)",
  "title": "string",
  "summary": "string (0-500 chars)",
  "key_entities": {
    "people": ["string"],
    "organizations": ["string"],
    "locations": ["string"]
  },
  "sections": ["string"],
  "quiz": [
    {
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer": "string (must be in options)",
      "difficulty": "easy | medium | hard",
      "explanation": "string"
    }
  ],
  "related_topics": ["string"],
  "created_at": "ISO 8601 timestamp",
  "is_cached": "boolean"
}
```

### Quiz Question

```json
{
  "question": "What was X?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Option B",
  "difficulty": "medium",
  "explanation": "Explanation of why Option B is correct."
}
```

### Key Entities

```json
{
  "people": ["Person Name", ...],
  "organizations": ["Organization Name", ...],
  "locations": ["Location Name", ...]
}
```

---

## HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Quiz retrieved successfully |
| 400 | Bad Request | Invalid Wikipedia URL |
| 404 | Not Found | Quiz ID doesn't exist |
| 500 | Internal Server Error | LLM service crashed |

---

## Usage Examples

### Python (Requests)

```python
import requests

# Generate quiz
response = requests.post(
    'http://localhost:8000/api/quiz/generate',
    json={'url': 'https://en.wikipedia.org/wiki/Alan_Turing'}
)
quiz = response.json()
print(f"Generated {len(quiz['quiz'])} questions")

# List all quizzes
quizzes = requests.get('http://localhost:8000/api/quiz/list').json()
print(f"Total quizzes: {len(quizzes)}")

# Get specific quiz
quiz = requests.get(f'http://localhost:8000/api/quiz/{quiz["id"]}').json()
print(f"Title: {quiz['title']}")

# Delete quiz
requests.delete(f'http://localhost:8000/api/quiz/{quiz["id"]}')
```

### cURL

```bash
# Generate quiz
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}'

# List quizzes
curl http://localhost:8000/api/quiz/list

# Get specific quiz
curl http://localhost:8000/api/quiz/1

# Delete quiz
curl -X DELETE http://localhost:8000/api/quiz/1

# Health check
curl http://localhost:8000/api/health
```

### JavaScript (Fetch)

```javascript
// Generate quiz
const response = await fetch('http://localhost:8000/api/quiz/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://en.wikipedia.org/wiki/Alan_Turing' })
});
const quiz = await response.json();

// List quizzes
const quizzes = await fetch('http://localhost:8000/api/quiz/list').then(r => r.json());

// Get quiz details
const fullQuiz = await fetch(`http://localhost:8000/api/quiz/${quiz.id}`).then(r => r.json());

// Delete quiz
await fetch(`http://localhost:8000/api/quiz/${quiz.id}`, { method: 'DELETE' });
```

---

## Rate Limiting

Currently no rate limiting implemented.

Recommended for production:
- 100 requests/minute per IP
- 10 quiz generations/minute per IP

---

## Pagination

For `/api/quiz/list`, use skip/limit:

```bash
# Page 1 (0-49)
curl 'http://localhost:8000/api/quiz/list?skip=0&limit=50'

# Page 2 (50-99)
curl 'http://localhost:8000/api/quiz/list?skip=50&limit=50'

# Get all (default limit 100)
curl 'http://localhost:8000/api/quiz/list'
```

---

## CORS

Frontend requests from different origin are allowed.

CORS headers included:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

---

## Timeout Behavior

- Quiz generation: ~10 seconds timeout (processing 5-15s)
- Other endpoints: ~30 seconds timeout
- WebSocket: N/A (REST only)

---

## Versioning

Current API version: **1.0.0**

To maintain backward compatibility, consider:
- Adding `/v1/` prefix in future: `/v1/api/quiz/generate`
- Deprecating old endpoints gradually
- Supporting multiple versions simultaneously

---

## Error Handling

All errors return JSON with `detail` field:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Examples:
- Invalid URL → 400 Bad Request
- Scraping failed → 500 Internal Server Error
- LLM error → 500 Internal Server Error
- DB error → 500 Internal Server Error

---

## Performance Metrics

**Average Response Times**:
- Generate Quiz (cold): 10-15 seconds
- Generate Quiz (cached): <100ms
- List Quizzes: 50-200ms
- Get Quiz: 20-50ms
- Delete Quiz: 10-30ms
- Health Check: <10ms

**Limits**:
- Max questions per quiz: 8
- Max related topics: 8
- Max entities per type: 10
- Max sections: 15

---

## Testing the API

### Using Postman

1. Import collection from `/postman/wiki-quiz-collection.json`
2. Set `{{BASE_URL}}` to `http://localhost:8000`
3. Run requests

### Using API Documentation

Visit http://localhost:8000/docs (auto-generated by FastAPI)

---

## Future Endpoints

Planned for v2.0:

- `POST /api/quiz/batch` - Generate multiple quizzes
- `GET /api/quiz/search?q=topic` - Search quizzes
- `POST /api/quiz/{id}/submit` - Submit user answers
- `GET /api/stats` - Usage statistics
- `GET /api/suggestions?url=...` - Topic suggestions before generating

---

**Last Updated**: January 31, 2026
**API Version**: 1.0.0
