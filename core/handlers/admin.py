from aiogram import Router, F, Bot
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import Filter
from aiogram.types import Message
from core.utils.commands import set_commands
from core.settings import settings
from core.handlers.gpt import generate
admin = Router()


class AdminProtect(Filter):
    """
    Фильтр для проверки пользователя на админа
    """
    def __init__(self):
        self.admins = [settings.bots.admin_id]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started!', disable_notification=True)


@admin.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped', disable_notification=True)


@admin.message(Command('ai'))
async def ai_request(message: Message, command: CommandObject, bot: Bot):
    reply = message.reply_to_message
    prompt = reply.text if reply else ''
    prompt += ('\n' + command.args) if command.args else ''

    if prompt.strip() == "":
        await message.answer(text='Something wrong:(\nYou didn`t type any question')
        return

    answer = await generate(prompt)
    await message.answer(text=answer)