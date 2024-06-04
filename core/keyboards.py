from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


project_info = InlineKeyboardBuilder([
    [InlineKeyboardButton(text='Github проекта', url=r'https://github.com/devnsko/ai-bee')]
])