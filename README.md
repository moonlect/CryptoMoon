# CryptoTracker 🚀

Веб-платформа для анализа криптовалют с агрегацией данных о котировках, спрединге между биржами и финансовых показателях.

## ✅ MVP полностью готов к демонстрации!

**Backend:** FastAPI + PostgreSQL + Redis  
**Frontend:** React + TypeScript + Tailwind CSS  
**Все 9 страниц из ТЗ реализованы!**

## Технологический стек

- **Backend:** FastAPI, Python 3.11+
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7+
- **ORM:** SQLAlchemy 2.0
- **Миграции:** Alembic
- **WebSocket:** WebSockets (Python)
- **Background Jobs:** Celery

## Структура проекта

```
cryptotracker/
├── app/
│   ├── core/              # Общие компоненты (config, security, database)
│   ├── services/           # Микросервисы
│   │   ├── auth/          # Auth Service
│   │   ├── user/           # User Service
│   │   ├── market/         # Market Data Service
│   │   ├── signals/        # Signals Service
│   │   └── notifications/ # Notification Service
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   └── main.py            # Точка входа FastAPI
├── alembic/               # Миграции БД
├── tests/                 # Тесты
├── docker-compose.yml     # Docker Compose для разработки
└── pyproject.toml         # Зависимости
```

## 🚀 Быстрый запуск для демонстрации

### Автоматический запуск (рекомендуется)

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Ручной запуск

1. **Настройте окружение:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env, укажите SECRET_KEY
   ```

2. **Запустите Docker сервисы:**
   ```bash
   docker-compose up -d postgres redis
   ```

3. **Примените миграции:**
   ```bash
   alembic upgrade head
   ```

4. **Установите зависимости:**
   ```bash
   # Backend
   pip install -e ".[dev]"
   
   # Frontend
   cd frontend
   npm install
   cd ..
   ```

5. **Запустите приложения:**
   ```bash
   # Терминал 1 - Backend
   uvicorn app.main:app --reload
   
   # Терминал 2 - Frontend
   cd frontend
   npm run dev
   ```

### Доступ к приложению

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Документация:** http://localhost:8000/docs

## Разработка

### Запуск тестов
```bash
pytest
```

### Форматирование кода
```bash
black .
```

### Проверка типов
```bash
mypy app
```

### Линтинг
```bash
flake8 app
```

## Лицензия

MIT

