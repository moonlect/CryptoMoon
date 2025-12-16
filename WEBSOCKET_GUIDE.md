# WebSocket Guide - Real-time Signal Updates

## Обзор

WebSocket эндпоинт предоставляет real-time обновления сигналов для VIP пользователей. При появлении нового сигнала все подключенные VIP пользователи получают уведомление через WebSocket соединение.

## Подключение

### URL
```
ws://localhost:8000/ws/signals?token=YOUR_ACCESS_TOKEN
```

### Требования
- Действительный JWT access token
- VIP подписка (активная)

### Пример подключения (JavaScript)

```javascript
const token = "your_access_token_here";
const ws = new WebSocket(`ws://localhost:8000/ws/signals?token=${token}`);

ws.onopen = () => {
    console.log("Connected to CryptoTracker WebSocket");
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log("Received:", message);
    
    switch (message.type) {
        case "connected":
            console.log("Successfully connected");
            break;
        case "new_signal":
            handleNewSignal(message);
            break;
        case "signal_update":
            handleSignalUpdate(message);
            break;
        case "pong":
            // Response to ping
            break;
    }
};

ws.onerror = (error) => {
    console.error("WebSocket error:", error);
};

ws.onclose = (event) => {
    console.log("WebSocket closed:", event.code, event.reason);
};

// Send ping to keep connection alive
setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "ping" }));
    }
}, 30000); // Every 30 seconds
```

## Формат сообщений

### Входящие сообщения (от сервера)

#### 1. Connected
```json
{
    "type": "connected",
    "message": "Connected to CryptoTracker real-time signals",
    "user_id": 123
}
```

#### 2. New Signal
```json
{
    "type": "new_signal",
    "signal_type": "mexc_spot_futures",
    "data": {
        "id": 1,
        "coin_name": "NB",
        "position": "SHORT",
        "spread": 8.84,
        "created_at": "2025-12-14T12:00:00Z"
    }
}
```

Возможные значения `signal_type`:
- `mexc_spot_futures`
- `funding_rate`
- `mexc_dex`

#### 3. Signal Update
```json
{
    "type": "signal_update",
    "signal_type": "mexc_spot_futures",
    "signal_id": 1,
    "data": {
        "spread": 9.12,
        "mexc_spot_price": 0.00670000
    }
}
```

#### 4. Pong (ответ на ping)
```json
{
    "type": "pong"
}
```

### Исходящие сообщения (от клиента)

#### Ping (для keepalive)
```json
{
    "type": "ping"
}
```

#### Pong (ответ на ping от сервера)
```json
{
    "type": "pong"
}
```

## Обработка ошибок

### Коды закрытия WebSocket

- `1008` - Unauthorized (неверный токен или нет VIP подписки)
- `1000` - Normal closure (нормальное закрытие)

### Пример обработки

```javascript
ws.onclose = (event) => {
    if (event.code === 1008) {
        if (event.reason === "Unauthorized") {
            console.error("Invalid token. Please login again.");
        } else if (event.reason === "VIP subscription required") {
            console.error("VIP subscription required for real-time signals");
        }
    }
    
    // Reconnect logic
    setTimeout(() => {
        connectWebSocket();
    }, 5000);
};
```

## Best Practices

1. **Keepalive**: Отправляйте ping каждые 30 секунд для поддержания соединения
2. **Reconnection**: Реализуйте автоматическое переподключение при разрыве соединения
3. **Error Handling**: Обрабатывайте все типы ошибок и сообщений
4. **Token Refresh**: Обновляйте токен перед истечением срока действия
5. **Rate Limiting**: Не отправляйте слишком много сообщений на сервер

## Пример полной реализации (React)

```javascript
import { useEffect, useRef, useState } from 'react';

function useWebSocketSignals(token) {
    const [signals, setSignals] = useState([]);
    const wsRef = useRef(null);
    const reconnectTimeoutRef = useRef(null);

    useEffect(() => {
        if (!token) return;

        const connect = () => {
            const ws = new WebSocket(`ws://localhost:8000/ws/signals?token=${token}`);
            
            ws.onopen = () => {
                console.log('WebSocket connected');
                if (reconnectTimeoutRef.current) {
                    clearTimeout(reconnectTimeoutRef.current);
                }
            };

            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                
                if (message.type === 'new_signal') {
                    setSignals(prev => [message.data, ...prev]);
                } else if (message.type === 'signal_update') {
                    setSignals(prev => 
                        prev.map(signal => 
                            signal.id === message.signal_id 
                                ? { ...signal, ...message.data }
                                : signal
                        )
                    );
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            ws.onclose = (event) => {
                console.log('WebSocket closed:', event.code);
                // Reconnect after 5 seconds
                reconnectTimeoutRef.current = setTimeout(connect, 5000);
            };

            wsRef.current = ws;

            // Keepalive
            const pingInterval = setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'ping' }));
                }
            }, 30000);

            return () => {
                clearInterval(pingInterval);
                ws.close();
            };
        };

        connect();

        return () => {
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [token]);

    return signals;
}
```

## Тестирование

### Использование wscat (Node.js)

```bash
npm install -g wscat
wscat -c "ws://localhost:8000/ws/signals?token=YOUR_TOKEN"
```

### Использование Python

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/signals?token=YOUR_TOKEN"
    async with websockets.connect(uri) as websocket:
        # Send ping
        await websocket.send(json.dumps({"type": "ping"}))
        
        # Listen for messages
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(test_websocket())
```



