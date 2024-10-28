import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.handlers.user import user
from core.handlers.admin import admin
from core.database.models import async_main
from core.settings import settings

# Temporary solution: "Google Cloud Run" need to pass Health Check
# So we will add single healthcheck endpoint and will figure out more interesting solution later
from aiohttp import web

# Health check route handler
async def health(request):
    return web.Response(text="Bot is running!")

# Function to set up and start the aiohttp web server
async def start_aiohttp_server():
    app = web.Application()
    app.router.add_get('/health', health)  # Add the health check route
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    await async_main()
    bot = Bot(token=settings.bots.bot_token, defaults=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ))
    dp = Dispatcher()
    dp.include_routers(user, admin)
    
    # Start both the bot polling and aiohttp server concurrently
    await asyncio.gather(
        start_aiohttp_server(),  # Start aiohttp server for health checks
        dp.start_polling(bot)    # Start bot polling
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
