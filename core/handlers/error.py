import traceback
from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ErrorEvent, CallbackQuery
from core import keyboards as kb
from core.settings import settings
from core.handlers.gpt import generate_solution

error = Router()

# TODO: Fix errors
# @error.error()
# async def cmd_start(event: ErrorEvent, bot: Bot):
#     _traceback = traceback.format_exc()
#     error_text = f'Произошла ошибка: \n[Error]\n<pre language="python">{event.exception}</pre>\n[\Error]\n{_traceback}'
#     i = 0
#     if len(error_text) < 4096:
#         await bot.send_message(chat_id=settings.bots.admin_id, text=error_text, reply_markup=kb.error_keyboard, parse_mode=ParseMode.HTML)
#         return
#     else:
#         await bot.send_message(chat_id=settings.bots.admin_id, text=f'{error_text[:4092]}...', reply_markup=kb.error_keyboard, parse_mode=ParseMode.HTML)
#         # Check the content of error_text for unsupported HTML tags
#         # Ensure it does not contain any tags like <class> or any other unsupported tags

@error.callback_query(F.data == 'error_solve')
async def cmd_error_solve(callback: CallbackQuery, bot: Bot):
    solution = "Решение:\n" + await generate_solution(tg_id=callback.from_user.id, problem=callback.message.text)
    await bot.send_message(chat_id=callback.from_user.id, text=solution, parse_mode=ParseMode.HTML)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.answer()
    return
