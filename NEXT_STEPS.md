# Следующие шаги разработки

## Приоритет 1: Критичные функции MVP

### 1. Парсинг Telegram сообщений
**Цель:** Автоматическое создание сигналов из Telegram группы

**Задачи:**
- [ ] Создать Telegram бота для мониторинга группы
- [ ] Реализовать парсеры для трех типов сигналов:
  - [ ] MEXC Spot & Futures (формат из ТЗ)
  - [ ] Funding Rate Spread (формат из ТЗ)
  - [ ] MEXC & DEX Price Spread (формат из ТЗ)
- [ ] Интегрировать с `app/services/signals/service.py` для создания сигналов
- [ ] Настроить фоновую задачу (Celery или asyncio task)

**Файлы для создания:**
- `app/services/telegram/__init__.py`
- `app/services/telegram/bot.py`
- `app/services/telegram/parsers.py`
- `app/tasks/telegram_parser.py`

### 2. Notification Service
**Цель:** Система уведомлений для пользователей

**Задачи:**
- [ ] Создать сервис для отправки уведомлений
- [ ] Реализовать браузерные уведомления (Web Push API)
- [ ] Реализовать звуковые уведомления (клиентская часть)
- [ ] Реализовать email уведомления (SMTP)
- [ ] Интегрировать с настройками пользователя
- [ ] Фильтрация по настройкам (min_spread, min_profit и т.д.)

**Файлы для создания:**
- `app/services/notifications/__init__.py`
- `app/services/notifications/service.py`
- `app/services/notifications/router.py`
- `app/services/notifications/schemas.py`

### 3. Фоновая синхронизация CoinMarketCap
**Цель:** Автоматическое обновление котировок каждые 5 минут

**Задачи:**
- [ ] Настроить Celery или asyncio background task
- [ ] Реализовать периодическую задачу синхронизации
- [ ] Обработка ошибок и retry logic
- [ ] Логирование результатов

**Файлы для обновления:**
- `app/tasks/market_data.py` (уже создан, нужно доработать)
- Настроить Celery worker или asyncio scheduler

## Приоритет 2: Улучшения и оптимизация

### 4. Тестирование
**Задачи:**
- [ ] Unit тесты для всех сервисов (≥80% coverage)
- [ ] Интеграционные тесты для API эндпоинтов
- [ ] E2E тесты для критичных user flows
- [ ] Тесты WebSocket соединений

**Файлы для создания:**
- `tests/test_auth.py`
- `tests/test_user.py`
- `tests/test_market.py`
- `tests/test_signals.py`
- `tests/test_websocket.py`

### 5. Логирование и мониторинг
**Задачи:**
- [ ] Настроить structlog для структурированного логирования
- [ ] Добавить Prometheus метрики
- [ ] Настроить Grafana дашборды
- [ ] Интеграция с Sentry для отслеживания ошибок

### 6. Оптимизация производительности
**Задачи:**
- [ ] Оптимизация SQL запросов (индексы, N+1 проблемы)
- [ ] Кеширование в Redis для часто запрашиваемых данных
- [ ] Оптимизация WebSocket соединений
- [ ] Load testing и оптимизация

## Приоритет 3: Дополнительные функции

### 7. История сигналов и аналитика
**Задачи:**
- [ ] Эндпоинт для истории сигналов
- [ ] Статистика по сигналам
- [ ] Графики и визуализация (для фронтенда)

### 8. Улучшение безопасности
**Задачи:**
- [ ] CSRF защита
- [ ] Rate limiting по IP и пользователю (улучшить текущий)
- [ ] Audit logging для критичных операций
- [ ] Security headers (CSP, HSTS и т.д.)

### 9. API документация
**Задачи:**
- [ ] Улучшить OpenAPI документацию
- [ ] Добавить примеры запросов
- [ ] Создать Postman коллекцию

## Инструкции по реализации

### Настройка Telegram бота

1. Создать бота через @BotFather
2. Получить токен и добавить в `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```
3. Добавить бота в группу с правами на чтение сообщений

### Настройка Celery (опционально)

1. Установить зависимости:
   ```bash
   pip install celery[redis]
   ```
2. Создать `app/celery_app.py`
3. Настроить worker:
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

### Настройка Email (SMTP)

1. Добавить SMTP настройки в `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_password
   ```
2. Для Gmail использовать App Password

## Полезные команды

```bash
# Запуск приложения
uvicorn app.main:app --reload

# Применение миграций
alembic upgrade head

# Создание новой миграции
alembic revision --autogenerate -m "Description"

# Запуск тестов
pytest

# Форматирование кода
black app

# Проверка типов
mypy app

# Линтинг
flake8 app
```

## Полезные ссылки

- [FastAPI WebSocket](https://fastapi.tiangolo.com/advanced/websockets/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Celery Documentation](https://docs.celeryq.dev/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)



