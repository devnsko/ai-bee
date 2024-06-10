from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from core.database import requests as rq
from core.utils.text import Text
from core import keyboards as kb
from core.settings import settings

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    menu_text = f'Я пчёлка — личный AI помощник программиста (личный). ' \
                f'\nПока я только умею прокидывать твой вопрос в ChatGPT и присылать тебе ответ. ' \
                f'\nУ меня пока-что даже памяти нету' \
                f'\n\nЧтобы спросить что-то введи /ai запрос или/и сделать reply другого сообщения'
    is_new_user = not await rq.add_user(message.from_user.id, message.from_user.username or message.from_user.full_name)
    if is_new_user:
        menu_text = f'Добро пожаловать, {message.from_user.username or message.from_user.full_name}!\n' + menu_text
        await rq.add_bee_system(tg_id=message.from_user.id, name=settings.basic.bot_name, content=settings.basic.bot_content)
    else:
        menu_text = f'С возвращением, {message.from_user.username or message.from_user.full_name}!\n' + menu_text
    await rq.del_bee_history(message.from_user.id)
    await message.answer(text=menu_text, reply_markup=kb.project_info.as_markup())