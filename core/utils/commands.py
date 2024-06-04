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
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
