from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from core.database import requests as rq
from core.utils.text import Text
from core import keyboards as kb

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    menu_text = f'Привет, {message.from_user.username or message.from_user.full_name}! ' \
                f'\nЯ пчёлка — личный AI помощник программиста (личный). ' \
                f'\nПока я только умею прокидывать твой вопрос в ChatGPT и присылать тебе ответ. ' \
                f'\nУ меня пока-что даже памяти нету' \
                f'\n\nЧтобы спросить что-то введи /ai запрос или/и сделать reply другого сообщения'
    await rq.add_user(message.from_user.id, message.from_user.username or message.from_user.full_name)
    await message.answer(text=menu_text, reply_markup=kb.project_info.as_markup())