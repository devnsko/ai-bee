from aiogram.types import KeyboardButton, InlineKeyboardButton as IBtn
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from core.settings import settings

#Cancel button
cancel_button = KeyboardButton(text='Отмена')

# Reply keyboard with button "Cancel" for canceling the current operation
async def edit_context_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(cancel_button)
    keyboard.resize_keyboard = True
    return keyboard.as_markup()


async def menu_buttons(context: str = None):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(IBtn(text=settings.project.link_text, url=settings.project.link))
    if not context or not context.strip():    
        keyboard.add(IBtn(text='Add your context', callback_data='edit_context'))
    else:   
        keyboard.add(IBtn(text='Show Context', callback_data='context'))
        keyboard.add(IBtn(text='Edit Context', callback_data='edit_context'))
    keyboard.resize_keyboard = True
    return keyboard.adjust(1,2).as_markup()
