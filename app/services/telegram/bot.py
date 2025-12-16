"""Telegram bot for monitoring group messages and parsing signals."""
import asyncio
from typing import Optional
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.core.logging_config import get_logger
from app.services.telegram.parsers import (
    detect_signal_type,
    MEXCSpotFuturesParser,
    FundingRateParser,
    MEXCDEXParser,
)
from app.services.signals.service import (
    create_mexc_spot_futures_signal,
    create_funding_rate_signal,
    create_mexc_dex_signal,
)

logger = get_logger(__name__)


class TelegramBot:
    """Telegram bot for signal parsing."""

    def __init__(self):
        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
        
        self.application = Application.builder().token(settings.telegram_bot_token).build()
        self.chat_id = settings.telegram_chat_id

    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process incoming message and create signal if valid."""
        if not update.message or not update.message.text:
            return

        message_text = update.message.text
        chat_id = str(update.message.chat_id)

        # Only process messages from configured chat
        if self.chat_id and chat_id != self.chat_id:
            return

        # Detect signal type
        signal_type = detect_signal_type(message_text)
        if not signal_type:
            return

        # Parse signal based on type
        parsed_data = None
        async with AsyncSessionLocal() as db:
            try:
                if signal_type == 'mexc_spot_futures':
                    parser = MEXCSpotFuturesParser()
                    parsed_data = parser.parse(message_text)
                    if parsed_data:
                        await create_mexc_spot_futures_signal(db, **parsed_data)
                        logger.info(
                            "Created MEXC Spot & Futures signal",
                            coin_name=parsed_data.get('coin_name'),
                            spread=parsed_data.get('spread'),
                        )

                elif signal_type == 'funding_rate':
                    parser = FundingRateParser()
                    parsed_data = parser.parse(message_text)
                    if parsed_data:
                        await create_funding_rate_signal(db, **parsed_data)
                        logger.info(
                            "Created Funding Rate signal",
                            coin_name=parsed_data.get('coin_name'),
                            hourly_profit=parsed_data.get('hourly_profit'),
                        )

                elif signal_type == 'mexc_dex':
                    parser = MEXCDEXParser()
                    parsed_data = parser.parse(message_text)
                    if parsed_data:
                        await create_mexc_dex_signal(db, **parsed_data)
                        logger.info(
                            "Created MEXC & DEX signal",
                            coin_name=parsed_data.get('coin_name'),
                            spread_percent=parsed_data.get('spread_percent'),
                        )

            except Exception as e:
                logger.error(
                    "Error processing Telegram message",
                    error=str(e),
                    signal_type=signal_type,
                    exc_info=True,
                )
                # Log error but don't crash

    def setup_handlers(self):
        """Setup message handlers."""
        # Handle text messages
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.process_message
        )
        self.application.add_handler(message_handler)

    async def start(self):
        """Start the bot."""
        self.setup_handlers()
        logger.info("Telegram bot started and listening for messages", chat_id=self.chat_id)
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        """Stop the bot."""
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()


# Global bot instance
_telegram_bot: Optional[TelegramBot] = None


async def start_telegram_bot():
    """Start Telegram bot in background."""
    global _telegram_bot
    if not settings.telegram_bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN not set, skipping Telegram bot")
        return

    try:
        _telegram_bot = TelegramBot()
        await _telegram_bot.start()
    except Exception as e:
        logger.error("Error starting Telegram bot", error=str(e), exc_info=True)


async def stop_telegram_bot():
    """Stop Telegram bot."""
    global _telegram_bot
    if _telegram_bot:
        await _telegram_bot.stop()

