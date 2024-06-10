from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Start work'
        ),
        BotCommand(
            command='ai',
            description='Издеваемся над OpenAI'
        ),
        BotCommand(
            command='restart',
            description='обновить чат'
        ),
        BotCommand(
            command='newbot',
            description='добавить нового бота'
        ),
        BotCommand(
            command='mybots',
            description='список всех ботов'
        ),
        BotCommand(
            command='botinfo',
            description='инфо про текущего бота'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
