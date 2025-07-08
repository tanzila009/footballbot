from aiogram.types import BotCommand
from aiogram import Bot

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать регистрацию"),
        BotCommand(command="remind", description="Напомнить игрокам"),
        BotCommand(command="players", description="Игроки")
        ,  # ✅ English command
    ]
    await bot.set_my_commands(commands)
