import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/wiki_quiz_db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-this")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
