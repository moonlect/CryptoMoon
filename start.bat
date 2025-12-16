@echo off
REM Start script for CryptoTracker MVP (Windows)

echo 🚀 Starting CryptoTracker MVP...

REM Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file with your configuration
    echo    Required: SECRET_KEY, DATABASE_URL, REDIS_URL
    pause
    exit /b 1
)

REM Start Docker services
echo 🐳 Starting Docker services (PostgreSQL, Redis)...
docker-compose up -d postgres redis

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 5 /nobreak >nul

REM Check if migrations need to be run
echo 📊 Checking database migrations...
alembic upgrade head

REM Start backend
echo 🔧 Starting backend server...
start "CryptoTracker Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🎨 Starting frontend server...
cd frontend
call npm install
start "CryptoTracker Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ✅ CryptoTracker MVP is running!
echo.
echo 📍 Backend API: http://localhost:8000
echo 📍 Frontend: http://localhost:5173
echo 📍 API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop services...
pause >nul

REM Stop services
docker-compose down



