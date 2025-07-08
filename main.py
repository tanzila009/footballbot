import os
import asyncio

# ✅ Configure Django BEFORE importing anything Django-related
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FootballBot.settings")
import django
django.setup()

# ✅ Safe to import everything now
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import user_registration
from bot.set_commands import set_bot_commands


BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        user_registration.router,
    )
    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
