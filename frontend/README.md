# CryptoTracker Frontend

React + TypeScript + Vite + Tailwind CSS frontend for CryptoTracker.

## Установка

```bash
npm install
```

## Запуск

```bash
npm run dev
```

Приложение будет доступно по адресу: http://localhost:5173

## Сборка

```bash
npm run build
```

## Структура

```
src/
├── components/     # Переиспользуемые компоненты
├── contexts/      # React контексты (Auth)
├── hooks/         # Custom hooks (useWebSocket)
├── lib/           # Утилиты (API клиент)
├── pages/         # Страницы приложения
└── App.tsx        # Главный компонент
```

## Переменные окружения

Создайте `.env` файл:
```
VITE_API_URL=http://localhost:8000
```



