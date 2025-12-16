"""WebSocket routes for real-time signal updates."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.core.database import AsyncSessionLocal
from app.services.websocket.manager import manager
import json

router = APIRouter()


@router.websocket("/ws/signals")
async def websocket_signals(
    websocket: WebSocket,
    token: str = Query(...),
):
    """WebSocket endpoint for real-time signal updates."""
    user = None
    try:
        # Accept connection first (required by FastAPI)
        await websocket.accept()
        
        # Authenticate user AFTER accepting connection
        async with AsyncSessionLocal() as db:
            # Authenticate user
            user = await manager.get_user_from_token(token, db)
            if not user:
                # Close connection if unauthorized
                await websocket.close(code=1008, reason="Unauthorized")
                return

            # Check if user has VIP subscription
            from app.models.user import Subscription
            from sqlalchemy import select

            result = await db.execute(
                select(Subscription).where(Subscription.user_id == user.id)
            )
            subscription = result.scalar_one_or_none()
            plan = subscription.plan if subscription else "free"

            if plan != "vip":
                await websocket.close(code=1008, reason="VIP subscription required")
                return

        # Register connection in manager (this doesn't call accept again)
        await manager.connect(websocket, user.id)

        # Send welcome message
        await manager.send_personal_message(
            {
                "type": "connected",
                "message": "Connected to CryptoTracker real-time signals",
                "user_id": user.id,
            },
            websocket,
        )

        # Keep connection alive and handle ping/pong
        while True:
            try:
                # Wait for message from client (ping/pong or other)
                data = await websocket.receive_text()
                message = json.loads(data)

                if message.get("type") == "pong":
                    # Respond to ping
                    await manager.send_personal_message(
                        {"type": "pong"}, websocket
                    )
                elif message.get("type") == "ping":
                    # Client sent ping, respond with pong
                    await manager.send_personal_message(
                        {"type": "pong"}, websocket
                    )

            except WebSocketDisconnect:
                # Client closed the connection - exit loop and clean up
                break
            except json.JSONDecodeError:
                # Invalid JSON, ignore
                continue
            except Exception as e:
                # Any other runtime error (e.g., connection already closed) - log and exit
                print(f"WebSocket error: {e}")
                try:
                    await websocket.close(code=1011, reason="WebSocket error")
                except Exception:
                    pass
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        # Log error but don't crash
        print(f"WebSocket connection error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal error")
        except:
            pass
    finally:
        # Always disconnect, even if user is None
        manager.disconnect(websocket)


async def broadcast_new_signal(signal_type: str, signal_data: dict):
    """Broadcast new signal to all connected VIP users."""
    from app.core.database import AsyncSessionLocal

    try:
        async with AsyncSessionLocal() as db:
            message = {
                "type": "new_signal",
                "signal_type": signal_type,
                "data": signal_data,
            }
            await manager.broadcast_to_vip_users(message, db)
    except Exception as e:
        # Log error but don't crash the application
        print(f"Error broadcasting new signal: {e}")


async def broadcast_signal_update(signal_type: str, signal_id: int, updates: dict):
    """Broadcast signal update to all connected VIP users."""
    from app.core.database import AsyncSessionLocal

    try:
        async with AsyncSessionLocal() as db:
            message = {
                "type": "signal_update",
                "signal_type": signal_type,
                "signal_id": signal_id,
                "data": updates,
            }
            await manager.broadcast_to_vip_users(message, db)
    except Exception as e:
        # Log error but don't crash the application
        print(f"Error broadcasting signal update: {e}")

