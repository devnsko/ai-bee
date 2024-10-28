from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from core.database import requests as rq
from core import keyboards as kb
from core.settings import settings
from core.handlers.gpt import generate
from core.database.models import User
from core.database import requests as rq
from core import keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import Filter, StateFilter
from aiogram.enums.chat_type import ChatType
import asyncio

user = Router()

class FreeChatFilter(Filter):
    def __init__(self) -> None:
        self.freeChat = [ChatType.PRIVATE]

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in (
            self.freeChat
        )

class Editing(StatesGroup):
    context = State()

class Wait(StatesGroup):
    answering = State()

@user.message(CommandStart())
async def cmd_start(message: Message):
    menu_text = "I'm AI bot"
    if not await rq.check_user(message.from_user.id):
        menu_text = f'Welcome, {message.from_user.username or message.from_user.full_name}!\n' + menu_text
    else:
        menu_text = f'Hello again, {message.from_user.username or message.from_user.full_name}!\n' + menu_text
    menu_text += '\n\nWrite your question and I will answer you'
    user = await rq.get_user(message.from_user.id)
    await message.answer(text=menu_text, reply_markup=await kb.menu_buttons(user.context))

@user.callback_query(F.data == 'edit_context')
async def bot_edit_setting(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user = await rq.get_user(callback.from_user.id)
    await state.set_state(Editing.context)
    await callback.message.answer(text=f'Please write the new context for your bot:', reply_markup=await kb.edit_context_keyboard())
    callback.answer()

# Get new bot content after bot_edit_setting in state BotStates.edit_content
@user.message(F.text, Editing.context)
async def get_new_bot_context(message: Message, state: FSMContext):
    context: str = message.text
    await rq.edit_context(tg_id=message.from_user.id, new_context=context)
    await message.reply(text=f'Great! Your new context is: {context}')
    await state.clear()

@user.callback_query(F.data == 'context')
async def bot_context(callback: CallbackQuery, bot: Bot):
    user = await rq.get_user(callback.from_user.id)
    await callback.message.answer(text=f'Your context is: \n\n{user.context}')
    callback.answer()

@user.message(F.text, Wait.answering)
async def nothing(message: Message):
    pass

# AI chat
@user.message(F.text, FreeChatFilter())
async def ai_request(message: Message, bot: Bot, state: FSMContext):
    reply_msg = message.reply_to_message
    reply_text = reply_msg.text if reply_msg and reply_msg.text else None
    reply_sticker = reply_msg.sticker.emoji if reply_msg and reply_msg.sticker else None
    msg_text = message.text

    prompt = " \n".join([f"{t}" for t in [reply_text, reply_sticker, msg_text] if t is not None])

    bot_msg = await message.reply(text='Wait a second...', parse_mode=ParseMode.HTML)
    await state.set_state(Wait.answering)
    answer = await generate(tg_id=message.from_user.id, user_message=prompt)
    print("[ANSWER:]\n\n"+answer+'\n\n')
    # If answer longer than 4095 then split and add ... then recursively send second message
    await send_chunk(message, answer)
    await bot_msg.delete()
    await state.clear()
    # await message.reply(text=answer, parse_mode=ParseMode.HTML)

async def send_chunk(message: Message, text: str):
    if len(text) > 4095:
        message.reply(text=text[:4090]+'...', parse_mode=ParseMode.HTML)
        print(text[:4090])
        await asyncio.sleep(1)
        await send_chunk(message, '...'+text[4090:])
    else:
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    return True




# @user.message(Command('ai'), States.chat_mode)
# async def ai_close_dialogue(message: Message, state: FSMContext):
#     await message.reply(text='Конец диалога')
#     await state.clear()
#     await rq.del_chat_history(message.from_user.id)


# @user.message(Command('ai'))
# async def ai_request(message: Message, command: CommandObject, bot: Bot, state: FSMContext):
#     reply_msg = message.reply_to_message
#     reply_text = reply_msg.text if reply_msg and reply_msg.text else None
#     reply_sticker = reply_msg.sticker.emoji if reply_msg and reply_msg.sticker else None
#     command_text = command.args if command.args else None

#     prompt = " \n".join([f"{t}" for t in [reply_text, reply_sticker, command_text] if t is not None])

#     if prompt.strip() == "":
#         await message.reply(text='Задавайте вопросы, я вас слушаю')
#         await state.set_state(States.chat_mode)
#         return

#     answer = await generate(tg_id=message.from_user.id, user_message=prompt)
#     await message.reply(text=answer, parse_mode=ParseMode.HTML)
