from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from core.database import requests as rq
from core import keyboards as kb
from core.settings import settings

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    menu_text = "I'm your AI bot"
    if not await rq.check_user(message.from_user.id):
        await rq.get_user(message.from_user.id)
        menu_text = f'Welcome, {message.from_user.username or message.from_user.full_name}!\n' + menu_text
    else:
        menu_text = f'Hello again, {message.from_user.username or message.from_user.full_name}!\n' + menu_text
    await message.answer(text=menu_text, reply_markup=kb.menu_buttons())
