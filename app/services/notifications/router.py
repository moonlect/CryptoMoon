"""Notification Service API routes."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.signal import Notification
from pydantic import BaseModel
from datetime import datetime


class NotificationResponse(BaseModel):
    """Notification response schema."""

    id: int
    signal_type: str | None
    signal_id: int | None
    title: str | None
    body: str | None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Notification list response schema."""

    data: List[NotificationResponse]
    pagination: dict


router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    unread_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get user notifications."""
    query = select(Notification).where(Notification.user_id == user.id)

    if unread_only:
        query = query.where(Notification.is_read == False)

    # Sort by created_at DESC
    query = query.order_by(desc(Notification.created_at))

    # Count total
    from sqlalchemy import func
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Pagination
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    notifications = result.scalars().all()

    return NotificationListResponse(
        data=[
            NotificationResponse(
                id=n.id,
                signal_type=n.signal_type,
                signal_id=n.signal_id,
                title=n.title,
                body=n.body,
                is_read=n.is_read,
                created_at=n.created_at,
            )
            for n in notifications
        ],
        pagination={"total": total, "limit": limit, "offset": offset},
    )


@router.put("/{notification_id}/read", status_code=204)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Mark notification as read."""
    result = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, Notification.user_id == user.id
        )
    )
    notification = result.scalar_one_or_none()

    if not notification:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
        )

    notification.is_read = True
    notification.read_at = datetime.utcnow()
    await db.commit()


@router.put("/read-all", status_code=204)
async def mark_all_notifications_read(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Mark all user notifications as read."""
    from sqlalchemy import update

    await db.execute(
        update(Notification)
        .where(Notification.user_id == user.id, Notification.is_read == False)
        .values(is_read=True, read_at=datetime.utcnow())
    )
    await db.commit()


@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get count of unread notifications."""
    from sqlalchemy import func

    result = await db.execute(
        select(func.count(Notification.id)).where(
            Notification.user_id == user.id, Notification.is_read == False
        )
    )
    count = result.scalar() or 0

    return {"unread_count": count}



