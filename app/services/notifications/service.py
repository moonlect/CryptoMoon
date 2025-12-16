"""Notification Service for sending notifications to users."""
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserPreferences, Subscription
from app.models.signal import Notification
from datetime import datetime


class NotificationService:
    """Service for managing and sending notifications."""

    async def should_send_notification(
        self,
        db: AsyncSession,
        user_id: int,
        signal_type: str,
        signal_data: Dict[str, Any],
    ) -> bool:
        """Check if notification should be sent based on user preferences."""
        # Get user preferences
        result = await db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        preferences = result.scalar_one_or_none()
        if not preferences:
            return False

        # Check if notifications are enabled globally
        if not preferences.notifications_enabled:
            return False

        # Check signal type specific settings
        if signal_type == 'mexc_spot_futures':
            if not preferences.mexc_spot_futures_enabled:
                return False
            # Check min spread filter
            min_spread = float(preferences.mexc_spot_futures_min_spread or 0)
            signal_spread = signal_data.get('spread')
            if signal_spread and float(signal_spread) < min_spread:
                return False

        elif signal_type == 'funding_rate':
            if not preferences.funding_rate_enabled:
                return False
            # Check min profit filter
            min_profit = float(preferences.funding_rate_min_profit or 0)
            signal_profit = signal_data.get('hourly_profit')
            if signal_profit and float(signal_profit) < min_profit:
                return False

        elif signal_type == 'mexc_dex':
            if not preferences.mexc_dex_enabled:
                return False
            # Check min spread filter
            min_spread = float(preferences.mexc_dex_min_spread or 0)
            signal_spread = signal_data.get('spread_percent')
            if signal_spread and float(signal_spread) < min_spread:
                return False

        return True

    async def create_notification(
        self,
        db: AsyncSession,
        user_id: int,
        signal_type: str,
        signal_id: int,
        title: str,
        body: str,
    ) -> Notification:
        """Create a notification record in database."""
        notification = Notification(
            user_id=user_id,
            signal_type=signal_type,
            signal_id=signal_id,
            title=title,
            body=body,
            is_read=False,
        )
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    async def send_browser_notification(
        self,
        db: AsyncSession,
        user_id: int,
        title: str,
        body: str,
        signal_data: Optional[Dict[str, Any]] = None,
    ):
        """Send browser notification via WebSocket."""
        from app.services.websocket.manager import manager
        
        notification = {
            "title": title,
            "body": body,
            "data": signal_data or {},
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        await manager.send_notification(user_id, notification)

    async def send_sound_notification(
        self,
        db: AsyncSession,
        user_id: int,
        signal_type: str,
    ):
        """Trigger sound notification via WebSocket."""
        from app.services.websocket.manager import manager
        
        notification = {
            "type": "sound",
            "signal_type": signal_type,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        await manager.send_notification(user_id, notification)

    async def send_email_notification(
        self,
        user: User,
        title: str,
        body: str,
        signal_data: Optional[Dict[str, Any]] = None,
    ):
        """Send email notification."""
        from app.services.notifications.email import email_service

        if not signal_data:
            signal_data = {}

        signal_type = signal_data.get("signal_type", "")
        coin_name = signal_data.get("coin_name", "Unknown")

        # Generate email content
        subject, html_body, text_body = email_service.generate_signal_email_html(
            signal_type, coin_name, signal_data
        )

        # Send email
        await email_service.send_email(
            to_email=user.email,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )

    async def notify_users_about_signal(
        self,
        db: AsyncSession,
        signal_type: str,
        signal_id: int,
        signal_data: Dict[str, Any],
    ):
        """Notify all users who should receive notification about new signal."""
        # Get all VIP users
        result = await db.execute(
            select(User.id, User.email, Subscription.user_id)
            .join(Subscription, User.id == Subscription.user_id)
            .where(Subscription.plan == 'vip', Subscription.status == 'active')
        )
        vip_users = result.all()

        # Generate notification title and body
        coin_name = signal_data.get('coin_name', 'Unknown')
        title = f"New {signal_type.replace('_', ' ').title()} Signal: {coin_name}"
        
        if signal_type == 'mexc_spot_futures':
            spread = signal_data.get('spread')
            position = signal_data.get('position', '')
            body = f"Spread: {spread}% | Position: {position}"
        elif signal_type == 'funding_rate':
            profit = signal_data.get('hourly_profit')
            body = f"Hourly Profit: {profit}%"
        elif signal_type == 'mexc_dex':
            spread = signal_data.get('spread_percent')
            body = f"Spread: {spread}%"
        else:
            body = "New signal available"

        for user_id, email, _ in vip_users:
            # Check if user should receive notification
            should_send = await self.should_send_notification(
                db, user_id, signal_type, signal_data
            )

            if not should_send:
                continue

            # Get user preferences for notification types
            pref_result = await db.execute(
                select(UserPreferences).where(UserPreferences.user_id == user_id)
            )
            preferences = pref_result.scalar_one_or_none()

            if not preferences:
                continue

            # Create notification record
            await self.create_notification(db, user_id, signal_type, signal_id, title, body)

            # Send browser notification if enabled
            if signal_type == 'mexc_spot_futures' and preferences.mexc_spot_futures_browser_notif:
                await self.send_browser_notification(db, user_id, title, body, signal_data)
            elif signal_type == 'funding_rate' and preferences.funding_rate_browser_notif:
                await self.send_browser_notification(db, user_id, title, body, signal_data)
            elif signal_type == 'mexc_dex' and preferences.mexc_dex_browser_notif:
                await self.send_browser_notification(db, user_id, title, body, signal_data)

            # Send sound notification if enabled
            if signal_type == 'mexc_spot_futures' and preferences.mexc_spot_futures_sound:
                await self.send_sound_notification(db, user_id, signal_type)
            elif signal_type == 'funding_rate' and preferences.funding_rate_sound:
                await self.send_sound_notification(db, user_id, signal_type)
            elif signal_type == 'mexc_dex' and preferences.mexc_dex_sound:
                await self.send_sound_notification(db, user_id, signal_type)

            # Send email notification if enabled
            user_result = await db.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()
            
            if user:
                if signal_type == 'mexc_spot_futures' and preferences.mexc_spot_futures_email_notif:
                    await self.send_email_notification(user, title, body, signal_data)
                elif signal_type == 'funding_rate' and preferences.funding_rate_email_notif:
                    await self.send_email_notification(user, title, body, signal_data)
                elif signal_type == 'mexc_dex' and preferences.mexc_dex_email_notif:
                    await self.send_email_notification(user, title, body, signal_data)


# Global service instance
notification_service = NotificationService()

