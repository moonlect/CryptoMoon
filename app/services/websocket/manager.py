"""WebSocket connection manager."""
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from app.core.security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, Subscription


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        # Map user_id -> set of websocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # Map websocket -> user_id
        self.websocket_to_user: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Register WebSocket connection (accept should be called before this)."""
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.websocket_to_user[websocket] = user_id

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection."""
        user_id = self.websocket_to_user.get(websocket)
        if user_id and user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        if websocket in self.websocket_to_user:
            del self.websocket_to_user[websocket]

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific WebSocket connection."""
        try:
            await websocket.send_json(message)
        except Exception:
            self.disconnect(websocket)

    async def broadcast_to_user(self, user_id: int, message: dict):
        """Broadcast message to all connections of a specific user."""
        if user_id in self.active_connections:
            disconnected = set()
            for websocket in self.active_connections[user_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    disconnected.add(websocket)
            
            # Remove disconnected websockets
            for ws in disconnected:
                self.disconnect(ws)

    async def send_notification(self, user_id: int, notification: dict):
        """Send notification to specific user via WebSocket."""
        message = {
            "type": "notification",
            "data": notification,
        }
        await self.broadcast_to_user(user_id, message)

    async def broadcast_to_vip_users(self, message: dict, db: AsyncSession):
        """Broadcast message to all VIP users."""
        # Get all VIP user IDs
        result = await db.execute(
            select(Subscription.user_id).where(Subscription.plan == "vip", Subscription.status == "active")
        )
        vip_user_ids = [row[0] for row in result.all()]

        # Broadcast to all VIP users (only those currently connected)
        for user_id in vip_user_ids:
            if user_id in self.active_connections:
                await self.broadcast_to_user(user_id, message)

    async def get_user_from_token(self, token: str, db: AsyncSession) -> User | None:
        """Get user from JWT token."""
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            return None

        return user


# Global connection manager instance
manager = ConnectionManager()

