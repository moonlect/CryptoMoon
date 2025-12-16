#!/bin/bash

# Start script for CryptoTracker MVP

echo "🚀 Starting CryptoTracker MVP..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration"
    echo "   Required: SECRET_KEY, DATABASE_URL, REDIS_URL"
    exit 1
fi

# Start Docker services
echo "🐳 Starting Docker services (PostgreSQL, Redis)..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if migrations need to be run
echo "📊 Checking database migrations..."
alembic upgrade head

# Start backend
echo "🔧 Starting backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ CryptoTracker MVP is running!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 Frontend: http://localhost:5173"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT
wait



