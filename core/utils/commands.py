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
            description='talk to AI Bee'
        ),
        BotCommand(
            command='newbot',
            description='Add new bot'
        ),
        BotCommand(
            command='mybots',
            description='List of your bots'
        ),
        BotCommand(
            command='botinfo',
            description='Info about your bot'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
