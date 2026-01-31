from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from pydantic import EmailStr

class QuizQuestion(BaseModel):
    """Schema for a single quiz question"""
    question: str
    options: List[str]
    answer: str
    difficulty: str  # easy, medium, hard
    explanation: str

class KeyEntities(BaseModel):
    """Schema for key entities extracted from article"""
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []

class WikiQuizCreate(BaseModel):
    """Schema for creating a new wiki quiz"""
    url: str

class WikiQuizResponse(BaseModel):
    """Schema for returning wiki quiz data"""
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict
    sections: List[str]
    quiz: List[QuizQuestion]
    related_topics: List[str]
    created_at: datetime
    is_cached: bool

    class Config:
        from_attributes = True

class WikiQuizListResponse(BaseModel):
    """Schema for listing quizzes in history"""
    id: int
    url: str
    title: str
    created_at: datetime
    is_cached: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class QuizHistoryItem(BaseModel):
    id: int
    quiz_id: int
    created_at: datetime
    title: Optional[str] = None
    url: Optional[str] = None

    class Config:
        from_attributes = True
