from aiogram import Router, F, Bot
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import Filter, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from core.utils.commands import set_commands
from core.settings import settings
from core.handlers.gpt import generate
from core.database.models import SystemData, User
from core.database import requests as rq
from core import keyboards as kb

admin = Router()


class AdminProtect(Filter):
    """
    Фильтр для проверки пользователя на админа
    """
    def __init__(self):
        self.admins = [settings.bots.admin_id]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


class NewBotState(StatesGroup):
    add_name = State()
    add_content = State()

class BotStates(StatesGroup):
    edit_name = State()
    edit_content = State()

class WaitState(StatesGroup):
    wait_changed = State()


@admin.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started!', disable_notification=True)


@admin.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped', disable_notification=True)


@admin.message(Command('ai'))
async def ai_request(message: Message, command: CommandObject, bot: Bot):
    reply_msg = message.reply_to_message
    reply_text = reply_msg.text if reply_msg and reply_msg.text else None
    reply_sticker = reply_msg.sticker.emoji if reply_msg and reply_msg.sticker else None
    command_text = command.args if command.args else None

    prompt = " \n".join([f"{t}" for t in [reply_text, reply_sticker, command_text] if t is not None])

    if prompt.strip() == "":
        await message.reply(text='Something wrong:(\nYou didn`t type any question')
        return

    answer = await generate(tg_id=message.from_user.id, user_message=prompt)
    await message.reply(text=answer)


@admin.message(Command('botinfo'))
async def cmd_bot_info(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(WaitState.wait_changed)
    await bot_info(message=message, tg_id=message.from_user.id)
    await state.clear()


# Get bot list after command /mybots in message and in inline keyboard
@admin.message(Command('mybots'))
async def get_bots_list(message: Message, bot: Bot):
    tg_id = message.from_user.id
    systems = await rq.get_bee_system_list(tg_id=tg_id)
    if not systems:
        await message.reply(text='У вас нет ни одного бота')
        return
    text = 'Ваши боты:\n'
    for system in systems:
        text += f'{system.bot_name}\n'
    await message.reply(text=text, reply_markup=await kb.get_bot_list(systems=systems))


@admin.message(Command('restart'))
async def refresh_history(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await rq.del_bee_history(message.from_user.id)
    await message.reply(text='Bee: Новый чат')


@admin.message(Command('newbot'))
async def new_bot(message: Message, bot: Bot, state: FSMContext):
    await message.reply(text='Напишите название для бота')
    await state.clear()
    await state.set_state(NewBotState.add_name)


# Get bot info after bot_info_{system_id} in callback query
@admin.callback_query(F.data.startswith('bot_info_'))
async def bot_info_by_id(callback: CallbackQuery, bot: Bot):
    system_id = int(callback.data.split('_')[-1])
    user = await rq.get_user_by_tuid(tg_id=callback.from_user.id)
    system: SystemData = await rq.get_bee_system_by_id(system_id=system_id)
    text = await bot_text_by_classes(user=user, system=system)
    await callback.message.answer(text=text, reply_markup=await kb.get_bot_settings(user=user, system=system))
    await callback.answer()


# Set bot to user after bot_connect_{system_id} in callback query
@admin.callback_query(F.data.startswith('bot_connect_'))
async def bot_connect_by_id(callback: CallbackQuery, bot: Bot):
    system_id = int(callback.data.split('_')[-1])
    await rq.set_bee_system(tg_id=callback.from_user.id, system_id=system_id)
    await callback.answer()
    await callback.message.answer(text=f'Бот подключен')
    await bot_info(message=callback.message, tg_id=callback.from_user.id, on_edit=False)


# Get bot list after bot_list in callback query
@admin.callback_query(F.data == 'bot_list')
async def bot_list(callback: CallbackQuery, bot: Bot):
    tg_id = callback.from_user.id
    systems = await rq.get_bee_system_list(tg_id=tg_id)
    if not systems:
        await callback.message.answer(text='У вас нет ни одного бота')
        return
    text = 'Ваши боты:\n'
    for system in systems:
        text += f'{system.bot_name}\n'
    await callback.message.answer(text=text, reply_markup=await kb.get_bot_list(systems=systems))
    await callback.answer()


# Get bot setting after bot_show_setting_{system_id} in callback query
@admin.callback_query(F.data.startswith('bot_show_setting_'))
async def bot_show_setting_by_id(callback: CallbackQuery, bot: Bot):
    system_id = int(callback.data.split('_')[-1])
    system: SystemData = await rq.get_bee_system_by_id(system_id=system_id)
    await callback.message.answer(text=system.bot_content)
    await callback.answer()


# Get new bot name after bot_edit_name in state BotStates.edit_name
@admin.message(F.text, BotStates.edit_name)
async def get_new_bot_name(message: Message, state: FSMContext):
    bot_name: str = message.text
    await rq.edit_bee_system_name(tg_id=message.from_user.id, new_name=bot_name)
    await message.reply(text=f'Отлично! Теперь у вашего бота новое имя: {bot_name}')
    await bot_info(message=message, tg_id=message.from_user.id, on_edit=False)
    await state.clear()

# Get new bot content after bot_edit_setting in state BotStates.edit_content
@admin.message(F.text, BotStates.edit_content)
async def get_new_bot_content(message: Message, state: FSMContext):
    bot_content: str = message.text
    await rq.edit_bee_system_content(tg_id=message.from_user.id, new_content=bot_content)
    await message.reply(text=f'Отлично! Теперь у вашего бота новая настройка: {bot_content}')
    await bot_info(message=message, tg_id=message.from_user.id, on_edit=False)
    await state.clear()

@admin.callback_query(F.data == 'bot_edit_setting')
async def bot_edit_setting(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(BotStates.edit_content)
    await callback.message.answer(text='Введите новую настройку для бота', reply_markup=kb.cancel_keyboard)
    await state.set_state(BotStates.edit_content)
    await callback.answer()

@admin.callback_query(F.data == 'bot_edit_name')
async def bot_edit_name(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(BotStates.edit_name)
    await callback.message.answer(text='Введите новое имя для бота', reply_markup=kb.cancel_keyboard)
    await state.set_state(BotStates.edit_name)
    await callback.answer()



@admin.callback_query(F.data == 'bot_show_setting')
async def bot_show_setting(callback: CallbackQuery, bot: Bot):
    tg_id = callback.from_user.id
    system: SystemData = await rq.get_bee_system(tg_id=tg_id)
    await callback.message.answer(text=system.bot_content)
    await callback.answer()


@admin.callback_query(F.data == 'bot_is_public')
async def bot_switch_is_public(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if state.get_state() == WaitState.wait_changed:
        return
    await state.set_state(WaitState.wait_changed)
    message: Message = callback.message
    tg_id = callback.from_user.id
    await rq.switch_ispublic_bee_system(tg_id=tg_id)
    await bot_info(message=message, tg_id=tg_id, on_edit=True)
    await state.clear()
    await callback.answer()


# Get universal bot info text for all cases
async def bot_text(tg_id: int):
    user = await rq.get_user_by_tuid(tg_id=tg_id)
    system = await rq.get_bee_system(tg_id=tg_id)
    author = await rq.get_user(system.author_id)
    bot_texts = f'Bot: {system.bot_name}' \
    f'\nSetting: {system.bot_content if len(system.bot_content) < 50 else system.bot_content[0:50] + "..."} ' \
    f'\nAuthor: {"You" if author.id == user.id else author.name} \nBot is {"Public👨‍👩‍👧‍👦" if system.is_public else "Private"}'
    return bot_texts

# Get universal bot info text for all cases using system_id
async def bot_text_by_classes(user: User, system: SystemData):
    bot_texts = f'Bot: {system.bot_name}' \
    f'\nSetting: {system.bot_content if len(system.bot_content) < 50 else system.bot_content[0:50] + "..."} ' \
    f'\nAuthor: {"You" if system.author_id == user.id else (await rq.get_user(system.author_id)).name} \nBot is {"Public👨‍👩‍👧‍👦" if system.is_public else "Private"}'
    return bot_texts

async def bot_info(message: Message, tg_id: int, on_edit: bool = False):

    text = await bot_text(tg_id=tg_id)
    text = 'Ваш бот:\n' + text + '\n\nВыберите действие:'
    keyboard = await kb.bot_info_buttons(tg_id=tg_id)
    if on_edit:
        await message.edit_text(text=text, reply_markup=keyboard)
    else:
        await message.answer(text=text, reply_markup=keyboard)


@admin.message(NewBotState.add_name)
async def new_bot_name(message: Message, bot: Bot, state: FSMContext):
    bot_name = message.text
    await state.update_data(name=bot_name)
    await message.reply(text='Отлично! Теперь введите настройку для бота')
    await state.set_state(NewBotState.add_content)


@admin.message(NewBotState.add_content)
async def new_bot_content(message: Message, bot: Bot, state: FSMContext):
    await message.reply(text='Подождите...')
    bot_content = message.text
    data = await state.get_data()
    bot_name = data.get('name')
    await rq.add_bee_system(tg_id=message.from_user.id, name=bot_name, content=bot_content)
    await bot.send_message(chat_id=message.from_user.id, text=f'Ваш новый бот \nBot: {bot_name}\nSetting: {bot_content if len(bot_content) < 50 else bot_content[::50] + "..."} \nAuthor: "You" \nBot is private', reply_markup=await kb.bot_info_buttons(message.from_user.id))
