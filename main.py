import asyncio
import os
import django
from aiogram.client.default import DefaultBotProperties

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FootballBot.settings")
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import user_registration, game_registration
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from asgiref.sync import sync_to_async
from football_app.models import Player
from dotenv import load_dotenv

load_dotenv()

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

    await dp.start_polling(bot)


router = Router()

class RegisterState(StatesGroup):
    name = State()
    phone = State()

# @router.message(F.text == "/start")
# async def start(message: Message, state: FSMContext):
#     await message.answer("Привет! Как тебя зовут?")
#     await state.set_state(RegisterState.name)
#
# @router.message(RegisterState.name)
# async def ask_phone(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     kb = ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text="📞 Отправить номер", request_contact=True)]],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#     )
#     await message.answer("Отправь свой номер телефона, пожалуйста:", reply_markup=kb)
#     await state.set_state(RegisterState.phone)
#
# @router.message(RegisterState.phone, F.contact)
# async def register_user(message: Message, state: FSMContext):
#     data = await state.get_data()
#     name = data["name"]
#     phone = message.contact.phone_number
#     telegram_id = message.from_user.id
#
#     await sync_to_async(Player.objects.update_or_create)(
#         telegram_id=telegram_id,
#         defaults={"full_name": name, "phone": phone},
#     )
#
#     await message.answer("Спасибо! Ты зарегистрирован.", reply_markup=None)
#     await state.clear()


if __name__ == "__main__":
    asyncio.run(main())
