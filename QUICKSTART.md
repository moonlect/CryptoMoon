# Быстрый старт CryptoTracker

## Предварительные требования

- Python 3.11 или выше
- Docker и Docker Compose (для PostgreSQL и Redis)
- Git

## Шаги установки

### 1. Установите зависимости

```bash
pip install -e ".[dev]"
```

### 2. Настройте переменные окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите:
- `SECRET_KEY` - случайная строка для JWT токенов
- `DATABASE_URL` - URL базы данных (по умолчанию для Docker Compose)
- `REDIS_URL` - URL Redis (по умолчанию для Docker Compose)

### 3. Запустите PostgreSQL и Redis

```bash
docker-compose up -d
```

Или используйте Makefile:
```bash
make up
```

### 4. Примените миграции базы данных

```bash
alembic upgrade head
```

Или через Makefile:
```bash
make upgrade
```

### 5. Запустите приложение

```bash
uvicorn app.main:app --reload
```

Или через Makefile:
```bash
make dev
```

### 6. Проверьте работу API

Откройте в браузере:
- API документация: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Тестирование API

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

### Вход в систему

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

Ответ содержит `access_token` и `refresh_token`.

### Использование токена

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Полезные команды

- `make install` - Установить зависимости
- `make dev` - Запустить dev сервер
- `make test` - Запустить тесты
- `make lint` - Проверить код линтерами
- `make format` - Форматировать код
- `make migrate msg="description"` - Создать новую миграцию
- `make upgrade` - Применить миграции
- `make up` - Запустить Docker сервисы
- `make down` - Остановить Docker сервисы

## Структура проекта

```
cryptotracker/
├── app/
│   ├── core/              # Общие компоненты
│   │   ├── config.py      # Конфигурация
│   │   ├── database.py    # База данных
│   │   ├── security.py    # JWT и пароли
│   │   ├── redis_client.py # Redis клиент
│   │   ├── dependencies.py # FastAPI зависимости
│   │   └── exceptions.py  # Обработка ошибок
│   ├── models/            # SQLAlchemy модели
│   ├── schemas/           # Pydantic схемы
│   ├── services/          # Микросервисы
│   │   └── auth/          # Auth Service
│   └── main.py            # Точка входа
├── alembic/               # Миграции БД
├── docker-compose.yml     # Docker Compose
└── pyproject.toml         # Зависимости
```

## Следующие шаги

1. Реализовать остальные сервисы (User, Market, Signals, Notifications)
2. Добавить WebSocket для real-time обновлений
3. Интегрировать CoinMarketCap API
4. Настроить парсинг Telegram сигналов
5. Создать фронтенд приложение

## Проблемы?

- Убедитесь, что PostgreSQL и Redis запущены: `docker-compose ps`
- Проверьте логи: `docker-compose logs postgres redis`
- Убедитесь, что миграции применены: `alembic current`
- Проверьте переменные окружения в `.env`



