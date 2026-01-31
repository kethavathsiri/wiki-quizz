"""
FastAPI backend for Wiki Quiz Application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db, engine, Base
from models import WikiQuiz
from schemas import WikiQuizCreate, WikiQuizResponse, WikiQuizListResponse
from schemas import UserCreate, UserResponse, Token, LoginRequest, QuizHistoryItem
import auth
from auth import create_access_token, get_password_hash
from scraper import scrape_wikipedia_article, validate_wikipedia_url
from llm_service import QuizGenerator
import crud

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Wiki Quiz API",
    description="Generate quizzes from Wikipedia articles using LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize quiz generator
try:
    quiz_generator = QuizGenerator()
except Exception as e:
    logger.error(f"Failed to initialize QuizGenerator: {e}")
    quiz_generator = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Wiki Quiz API",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "POST /api/quiz/generate",
            "get_quiz": "GET /api/quiz/{quiz_id}",
            "list_quizzes": "GET /api/quiz/list",
            "delete_quiz": "DELETE /api/quiz/{quiz_id}"
        }
    }

@app.post("/api/quiz/generate", response_model=WikiQuizResponse)
async def generate_quiz(request: WikiQuizCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user_optional)):
    """
    Generate a quiz from a Wikipedia article URL
    
    - **url**: Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)
    """
    
    # Validate URL
    if not validate_wikipedia_url(request.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Wikipedia URL"
        )
    
    # Check if quiz already exists (caching) and has content
    existing_quiz = crud.get_quiz_by_url(db, request.url)
    if existing_quiz and getattr(existing_quiz, 'quiz', None):
        try:
            # Ensure stored quiz is non-empty list
            if isinstance(existing_quiz.quiz, list) and len(existing_quiz.quiz) > 0:
                return existing_quiz
        except Exception:
            # Fall back to regenerating if stored data is malformed
            pass
    
    try:
        # Step 1: Scrape Wikipedia article
        logger.info(f"Scraping article from {request.url}")
        scraped_data = scrape_wikipedia_article(request.url)
        
        # Step 2: Generate quiz using LLM
        if quiz_generator is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM service not initialized"
            )
        
        logger.info("Generating quiz with LLM")
        quiz = quiz_generator.generate_quiz(
            scraped_data["title"],
            scraped_data["full_text"]
        )

        # If LLM returned insufficient questions (need at least 5), fail fast
        if not quiz or (isinstance(quiz, list) and len(quiz) < 5):
            logger.error("LLM returned fewer than 5 questions for URL: %s (got %d)", request.url, len(quiz) if quiz else 0)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to generate enough quiz questions. Please try again."
            )
        
        # Step 3: Generate related topics
        logger.info("Generating related topics")
        related_topics = quiz_generator.generate_related_topics(
            scraped_data["title"],
            scraped_data["full_text"]
        )
        
        # Step 4: Store in database
        logger.info("Storing quiz in database")
        db_quiz = crud.create_quiz(
            db=db,
            url=request.url,
            title=scraped_data["title"],
            summary=scraped_data["summary"],
            key_entities=scraped_data["key_entities"],
            sections=scraped_data["sections"],
            quiz=quiz,
            related_topics=related_topics,
            raw_html=scraped_data["raw_html"]
        )

        # If a user is authenticated, create a history entry linking the user and quiz
        try:
            if current_user is not None:
                try:
                    crud.create_history(db, user_id=current_user.id, quiz_id=db_quiz.id)
                except Exception:
                    logger.exception("Failed to create history entry")
        except Exception:
            # safe guard: ignore history creation errors
            pass
        
        return db_quiz
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing Wikipedia article: {str(e)}"
        )

@app.get("/api/quiz/{quiz_id}", response_model=WikiQuizResponse)
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get a specific quiz by ID"""
    quiz = crud.get_quiz_by_id(db, quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz

@app.get("/api/quiz/list", response_model=List[WikiQuizListResponse])
async def list_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all quizzes with pagination"""
    quizzes = crud.get_all_quizzes(db, skip=skip, limit=limit)
    return quizzes


@app.get("/api/history", response_model=List[QuizHistoryItem])
async def get_my_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    """Return the authenticated user's quiz history"""
    histories = crud.get_history_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

    # map history items to include quiz metadata
    results = []
    for h in histories:
        results.append(QuizHistoryItem(
            id=h.id,
            quiz_id=h.quiz_id,
            created_at=h.created_at,
            title=getattr(h.quiz, 'title', None),
            url=getattr(h.quiz, 'url', None)
        ))
    return results


# ------------------
# Authentication
# ------------------
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account (email + password)"""
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = auth.get_password_hash(user.password)
    try:
        u = crud.create_user(db, user_in=user, hashed_password=hashed)
        return u
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/login", response_model=Token)
async def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}




@app.delete("/api/quiz/{quiz_id}")
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Delete a quiz"""
    success = crud.delete_quiz(db, quiz_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return {"message": "Quiz deleted successfully"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_initialized": quiz_generator is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
