from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class WikiQuiz(Base):
    """Model for storing Wikipedia article quizzes"""
    __tablename__ = "wiki_quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    summary = Column(Text)
    key_entities = Column(JSON)  # {people, organizations, locations}
    sections = Column(JSON)  # Array of section titles
    quiz = Column(JSON)  # Array of quiz questions
    related_topics = Column(JSON)  # Array of related topics
    raw_html = Column(Text, nullable=True)  # Optional: Store raw HTML
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_cached = Column(Boolean, default=False)


class User(Base):
    """User model for authentication and per-user history"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    histories = relationship("QuizHistory", back_populates="user")


class QuizHistory(Base):
    """Link quizzes to users for per-user history"""
    __tablename__ = "quiz_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("wiki_quizzes.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="histories")
    quiz = relationship("WikiQuiz")

    class Config:
        from_attributes = True
