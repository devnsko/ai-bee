from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.database import requests as rq
from core.database.models import User, Bot

#Cancel button
cancel_button = KeyboardButton(text='Отмена')

project_info = InlineKeyboardBuilder([
    [InlineKeyboardButton(text='Github проекта', url=r'https://github.com/devnsko/ai-bee')],
])

# Reply keyboard with button "Cancel" for canceling the current operation
cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[cancel_button]],
    resize_keyboard=True, one_time_keyboard=True)

async def menu_buttons(tg_id):
    user: User = await rq.get_user(tg_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Project on GitHub', url=r'https://github.com/devnsko/ai-bee'))
    if user.bot:
        keyboard.add(InlineKeyboardButton(text='Your current Bot', callback_data='current_bot'))
    else:
        keyboard.add(InlineKeyboardButton(text='Create First Bot', callback_data='new_bot'))
    keyboard.resize_keyboard = True
    return keyboard.adjust(1).as_markup()

# Inline keyboard with settings of user's bot
async def bot_info_buttons(tg_id):
    system: Bot = await rq.get_bee_system(tg_id=tg_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=f'Edit name', callback_data=f'bot_edit_name'))
    keyboard.add(InlineKeyboardButton(text=f'Edit Setting', callback_data=f'bot_edit_setting'))
    keyboard.add(InlineKeyboardButton(text=f'Full Setting', callback_data=f'bot_show_setting'))
    keyboard.add(InlineKeyboardButton(text=f'PUBLIC: {"ON✅" if system.is_public else "OFF"}', callback_data=f'bot_is_public'))
    keyboard.resize_keyboard = True
    return keyboard.adjust(2).as_markup()


# Inline keyboard with list of bots
async def get_bot_list(systems: list[Bot]):
    keyboard = InlineKeyboardBuilder()
    print(" BTN")
    if not systems:
        print("No systems")
        return None
    for system in systems:
        keyboard.add(InlineKeyboardButton(text=f'{system.bot_name}', callback_data=f'bot_info_{system.id}'))
    keyboard.resize_keyboard = True
    return keyboard.adjust(2).as_markup()


# Inline keyboard with bot settings from list
async def get_bot_settings(user: User, system: Bot):
    keyboard = InlineKeyboardBuilder()
    if system.id != user.system_id:
        keyboard.add(InlineKeyboardButton(text=f'Подключить бота', callback_data=f'bot_connect_{system.id}'))
    keyboard.add(InlineKeyboardButton(text=f'Назад в список', callback_data=f'bot_list'))
    keyboard.add(InlineKeyboardButton(text=f'Глянуть настройку', callback_data=f'bot_show_setting_{system.id}'))
    keyboard.resize_keyboard = True
    return keyboard.adjust(2).as_markup()


# Inline keyboard for error
error_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Решить', callback_data='error_solve')],
], resize_keyboard=True)