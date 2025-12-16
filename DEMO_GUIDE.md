# Руководство по запуску MVP для демонстрации

## Быстрый старт

### Вариант 1: Автоматический запуск (рекомендуется)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Вариант 2: Ручной запуск

#### 1. Настройка окружения

Создайте файл `.env` из `.env.example`:
```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите:
```env
SECRET_KEY=your-secret-key-here-min-32-chars
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cryptotracker
DATABASE_URL_SYNC=postgresql://postgres:postgres@localhost:5432/cryptotracker
REDIS_URL=redis://localhost:6379/0

# Опционально (для полной функциональности):
COINMARKETCAP_API_KEY=your-api-key
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### 2. Запуск Docker сервисов

```bash
docker-compose up -d postgres redis
```

#### 3. Применение миграций

```bash
alembic upgrade head
```

#### 4. Установка зависимостей

**Backend:**
```bash
pip install -e ".[dev]"
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

#### 5. Запуск приложений

**Backend (в отдельном терминале):**
```bash
uvicorn app.main:app --reload
```

**Frontend (в отдельном терминале):**
```bash
cd frontend
npm run dev
```

## Доступ к приложению

После запуска:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Документация:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Демонстрация функциональности

### 1. Регистрация и вход

1. Откройте http://localhost:5173
2. Нажмите "Sign Up"
3. Создайте аккаунт (email + пароль)
4. Автоматически войдете в систему

### 2. Просмотр Market Data (Free план)

1. После входа перейдите в "Market Data"
2. Увидите таблицу с криптовалютами
3. Можете сортировать, искать, переключать страницы

### 3. Обновление до VIP

1. Перейдите в "Pricing"
2. Нажмите "Upgrade to VIP"
3. Подтвердите активацию
4. Теперь доступны все страницы сигналов

### 4. Просмотр сигналов (VIP)

После обновления до VIP доступны:
- **MEXC Spot & Futures** - арбитражные возможности
- **Funding Rate Spread** - дифференциалы funding rate
- **MEXC & DEX** - спреды между централизованными и децентрализованными биржами

### 5. Real-time обновления

1. Откройте любую страницу сигналов
2. WebSocket автоматически подключится
3. При появлении новых сигналов они появятся в реальном времени

### 6. Настройки уведомлений

1. Перейдите в "Profile"
2. Настройте уведомления для каждого типа сигналов
3. Установите фильтры (минимальный спред, прибыль)

## Тестовые данные

### Создание тестового сигнала через API

```bash
# Получите токен после входа
TOKEN="your-access-token"

# Создайте MEXC Spot & Futures сигнал
curl -X POST "http://localhost:8000/api/v1/signals/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "signal_type": "mexc_spot_futures",
    "coin_name": "BTC",
    "position": "SHORT",
    "spread": 5.5,
    "mexc_spot_price": 50000,
    "mexc_futures_price": 52750
  }'
```

## Структура для демонстрации

### Что работает без дополнительной настройки:

✅ Регистрация и вход
✅ Просмотр Market Data (если есть данные в БД)
✅ Обновление подписки
✅ Профиль и настройки
✅ Все страницы интерфейса

### Что требует настройки:

⚠️ **CoinMarketCap API** - для реальных данных котировок
⚠️ **Telegram Bot** - для автоматического создания сигналов
⚠️ **SMTP** - для email уведомлений

## Troubleshooting

### Проблема: База данных не подключается

```bash
# Проверьте статус контейнеров
docker-compose ps

# Проверьте логи
docker-compose logs postgres

# Пересоздайте контейнеры
docker-compose down
docker-compose up -d postgres redis
```

### Проблема: Миграции не применяются

```bash
# Проверьте подключение к БД
alembic current

# Примените миграции вручную
alembic upgrade head
```

### Проблема: Frontend не подключается к API

1. Проверьте, что backend запущен на порту 8000
2. Проверьте `frontend/.env` - должен быть `VITE_API_URL=http://localhost:8000`
3. Перезапустите frontend после изменения .env

### Проблема: WebSocket не работает

1. Убедитесь, что у пользователя VIP подписка
2. Проверьте токен в localStorage
3. Откройте консоль браузера для отладки

## Остановка сервисов

```bash
# Остановить все
docker-compose down

# Остановить и удалить volumes
docker-compose down -v
```

## Готово к демонстрации!

Все основные функции работают. Для полной функциональности настройте внешние сервисы (CoinMarketCap, Telegram, SMTP).



