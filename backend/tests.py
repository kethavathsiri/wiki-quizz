"""
Tests for Wiki Quiz Backend

Run with: pytest
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAPI:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "version" in response.json()

    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert "status" in response.json()

    def test_list_quizzes_empty(self):
        response = client.get("/api/quiz/list")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_nonexistent_quiz(self):
        response = client.get("/api/quiz/999")
        assert response.status_code == 404

    def test_invalid_url(self):
        response = client.post("/api/quiz/generate", json={"url": "https://example.com"})
        assert response.status_code == 400

    def test_generate_quiz_valid_url(self):
        """Test would require actual scraping and LLM - skip in CI"""
        pass

# Run tests with: pytest backend/tests.py -v
