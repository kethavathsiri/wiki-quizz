#!/bin/bash

# Wiki Quiz Setup Script
# This script sets up both backend and frontend for development

echo "🚀 Wiki Quiz Generator - Setup Script"
echo "======================================"

# Check Python
echo "✓ Checking Python..."
python3 --version || { echo "Python 3 not found"; exit 1; }

# Setup Backend
echo ""
echo "📦 Setting up Backend..."
cd backend || exit 1

# Create virtual environment
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "✓ Virtual environment created"
fi

# Activate venv
source venv/bin/activate || { echo "Failed to activate venv"; exit 1; }

# Install dependencies
pip install -r requirements.txt -q
echo "✓ Backend dependencies installed"

# Check .env
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "✓ Created .env file (please update with your credentials)"
  echo "  - Add GEMINI_API_KEY"
  echo "  - Update DATABASE_URL if needed"
fi

cd ..

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd frontend || exit 1

# Check Node
echo "✓ Checking Node.js..."
node --version || { echo "Node.js not found"; exit 1; }

# Install dependencies
npm install -q
echo "✓ Frontend dependencies installed"

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your Gemini API key"
echo "2. Ensure PostgreSQL is running"
echo "3. Create database: createdb wiki_quiz_db"
echo "4. Start backend: cd backend && python main.py"
echo "5. In another terminal, start frontend: cd frontend && npm start"
echo ""
echo "Happy quizzing! 📚"
