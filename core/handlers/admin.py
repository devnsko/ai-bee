from aiogram import Router, F, Bot
from aiogram.filters import Filter
from aiogram.types import Message
from core.utils.commands import set_commands
from core.settings import settings


admin = Router()

class AdminProtect(Filter):
    """
    Filter for checking user is admin
    """
    def __init__(self):
        self.admins = [settings.bots.admin_id]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started!', disable_notification=True)


@admin.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped', disable_notification=True)

