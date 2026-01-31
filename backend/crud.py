"""
CRUD operations for Wikipedia quizzes
"""
from sqlalchemy.orm import Session
from models import WikiQuiz
from schemas import WikiQuizCreate
from typing import List, Optional
import logging
from models import User, QuizHistory
from schemas import UserCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
import datetime

logger = logging.getLogger(__name__)

def get_quiz_by_url(db: Session, url: str) -> Optional[WikiQuiz]:
    """Get quiz by URL (for checking cache)"""
    try:
        return db.query(WikiQuiz).filter(WikiQuiz.url == url).first()
    except Exception as e:
        logger.error(f"Error fetching quiz by URL: {e}")
        return None

def get_quiz_by_id(db: Session, quiz_id: int) -> Optional[WikiQuiz]:
    """Get quiz by ID"""
    try:
        return db.query(WikiQuiz).filter(WikiQuiz.id == quiz_id).first()
    except Exception as e:
        logger.error(f"Error fetching quiz by ID: {e}")
        return None

def get_all_quizzes(db: Session, skip: int = 0, limit: int = 100) -> List[WikiQuiz]:
    """Get all quizzes with pagination"""
    try:
        return db.query(WikiQuiz).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error fetching all quizzes: {e}")
        return []

def create_quiz(
    db: Session,
    url: str,
    title: str,
    summary: str,
    key_entities: dict,
    sections: list,
    quiz: list,
    related_topics: list,
    raw_html: Optional[str] = None
) -> WikiQuiz:
    """Create a new quiz entry"""
    try:
        db_quiz = WikiQuiz(
            url=url,
            title=title,
            summary=summary,
            key_entities=key_entities,
            sections=sections,
            quiz=quiz,
            related_topics=related_topics,
            raw_html=raw_html,
            is_cached=False
        )
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz
    except Exception as e:
        logger.error(f"Error creating quiz: {e}")
        db.rollback()
        raise

def update_quiz_cache_flag(db: Session, quiz_id: int, is_cached: bool = True) -> Optional[WikiQuiz]:
    """Update quiz cache flag"""
    try:
        quiz = db.query(WikiQuiz).filter(WikiQuiz.id == quiz_id).first()
        if quiz:
            quiz.is_cached = is_cached
            db.commit()
            db.refresh(quiz)
        return quiz
    except Exception as e:
        logger.error(f"Error updating quiz cache flag: {e}")
        db.rollback()
        return None

def delete_quiz(db: Session, quiz_id: int) -> bool:
    """Delete a quiz"""
    try:
        quiz = db.query(WikiQuiz).filter(WikiQuiz.id == quiz_id).first()
        if quiz:
            db.delete(quiz)
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting quiz: {e}")
        db.rollback()
        return False


# -------------------------
# User CRUD
# -------------------------
def create_user(db: Session, user_in: UserCreate, hashed_password: str) -> User:
    db_user = User(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.error(f"Error fetching user by email: {e}")
        return None


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error fetching user by id: {e}")
        return None


# -------------------------
# Quiz History CRUD
# -------------------------
def create_history(db: Session, user_id: int, quiz_id: int) -> QuizHistory:
    try:
        history = QuizHistory(user_id=user_id, quiz_id=quiz_id)
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    except Exception as e:
        logger.error(f"Error creating history: {e}")
        db.rollback()
        raise


def get_history_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[QuizHistory]:
    try:
        return db.query(QuizHistory).filter(QuizHistory.user_id == user_id).order_by(QuizHistory.created_at.desc()).offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error fetching history for user {user_id}: {e}")
        return []
