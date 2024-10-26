import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.handlers.user import user
from core.handlers.admin import admin
from core.handlers.error import error
from core.database.models import async_main
from core.settings import settings
# from core.utils.exception import BeeException


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    await async_main()
    bot = Bot(token=settings.bots.bot_token, defaults=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ))
    # bee = BeeException(bot)
    dp = Dispatcher()
    dp.include_routers(user, admin, error)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
