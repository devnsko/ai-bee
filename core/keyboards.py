from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.database import requests as rq
from core.database.models import SystemData, User

#Cancel button
cancel_button = KeyboardButton(text='Отмена')

project_info = InlineKeyboardBuilder([
    [InlineKeyboardButton(text='Github проекта', url=r'https://github.com/devnsko/ai-bee')]
])

bot_settings = InlineKeyboardBuilder([

])

# Reply keyboard with button "Cancel" for canceling the current operation
cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[cancel_button]],
    resize_keyboard=True, one_time_keyboard=True)


# Inline keyboard with settings of user's bot
async def bot_info_buttons(tg_id):
    system: SystemData = await rq.get_bee_system(tg_id=tg_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=f'Edit name', callback_data=f'bot_edit_name'))
    keyboard.add(InlineKeyboardButton(text=f'Edit Setting', callback_data=f'bot_edit_setting'))
    keyboard.add(InlineKeyboardButton(text=f'Full Setting', callback_data=f'bot_show_setting'))
    keyboard.add(InlineKeyboardButton(text=f'PUBLIC: {"ON✅" if system.is_public else "OFF"}', callback_data=f'bot_is_public'))
    return keyboard.adjust(2).as_markup()


# Inline keyboard with list of bots
async def get_bot_list(systems: list[SystemData]):
    keyboard = InlineKeyboardBuilder()
    print(" BTN")
    if not systems:
        print("No systems")
        return None
    for system in systems:
        keyboard.add(InlineKeyboardButton(text=f'{system.bot_name}', callback_data=f'bot_info_{system.id}'))
    return keyboard.adjust(2).as_markup()


# Inline keyboard with bot settings from list
async def get_bot_settings(user: User, system: SystemData):
    keyboard = InlineKeyboardBuilder()
    if system.id != user.system_id:
        keyboard.add(InlineKeyboardButton(text=f'Подключить бота', callback_data=f'bot_connect_{system.id}'))
    keyboard.add(InlineKeyboardButton(text=f'Назад в список', callback_data=f'bot_list'))
    keyboard.add(InlineKeyboardButton(text=f'Глянуть настройку', callback_data=f'bot_show_setting_{system.id}'))
    return keyboard.adjust(2).as_markup()