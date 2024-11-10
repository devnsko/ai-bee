import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError

from core.handlers.user import user
from core.handlers.admin import admin
from core.database.models import async_main
from core.settings import settings

def setup_logging():
    """Set up logging for the bot with detailed output format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

def create_bot() -> Bot:
    """Initialize and return the Bot instance."""
    return Bot(
        token=settings.bots.bot_token,
        defaults=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

def create_dispatcher() -> Dispatcher:
    """Initialize and return the Dispatcher instance, including routers."""
    dp = Dispatcher()
    dp.include_routers(user, admin)
    return dp

async def main():
    setup_logging()
    logging.info("Starting the bot...")

    await async_main()  # Initialize database or any async startup tasks
    bot = create_bot()
    dp = create_dispatcher()

    try:
        await dp.start_polling(bot)
    except TelegramAPIError as e:
        logging.error(f"Telegram API Error: {e}")
    except Exception as e:
        logging.exception("Unexpected error occurred during bot polling.")
    finally:
        await bot.session.close()
        logging.info("Bot stopped and session closed.")
        
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")