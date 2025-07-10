from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from asyncio import create_task, sleep
from football_app.models import Player
from aiogram import types

router = Router()
group_chat_id = -1002761093639
my_chat_id = 528077024


class RegisterState(StatesGroup):
    name = State()
    phone = State()

@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Это бот для регистрации на футбол.\nКак тебя зовут?")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def ask_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📞 Отправить номер", request_contact=True, one_time_keyboard=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Отправь свой номер", reply_markup=kb)
    await state.set_state(RegisterState.phone)

@router.message(RegisterState.phone, F.contact)
async def finish_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    phone = message.contact.phone_number
    telegram_id = message.from_user.id

    await sync_to_async(Player.objects.update_or_create)(
        telegram_id=telegram_id,
        defaults={"full_name": name, "phone": phone},
    )

    await message.bot.send_message(
        chat_id=group_chat_id,
        text=f"✅ Новый игрок зарегистрировался:\n\n👤 Имя: {name}\n📞 Телефон: {phone}\n🆔 Telegram ID: {telegram_id}"
    )

    await state.clear()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚽ Записаться на игру", callback_data="register_game")]
        ]
    )

    await message.answer(
        "Ты зарегистрирован в сообществе. Теперь ты сможешь записываться на игры.",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "👇 Нажми, чтобы записаться на ближайшую игру:",
        reply_markup=keyboard
    )

class GameRegState(StatesGroup):
    waiting_for_receipt = State()

@router.callback_query(F.data == "register_game")
async def handle_register_game(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Чтобы записаться на ближайший матч, переведи сумму 1000 тг на карту: +7 707 495 17 99 (Kaspi Мирас) 4400430244219793\n"
        "После оплаты, пожалуйста, пришли скриншот или фото чека сюда."
    )
    await state.set_state(GameRegState.waiting_for_receipt)
    await callback.answer()

    async def remind():
        await sleep(900)
        if await state.get_state() == GameRegState.waiting_for_receipt:
            await callback.message.answer("Напоминаем! Для участия нужно оплатить и прислать чек.")

    async def timeout():
        await sleep(3600)
        if await state.get_state() == GameRegState.waiting_for_receipt:
            await callback.message.answer("⏰ Время для оплаты истекло, твоя регистрация на игру отменена.")
            await state.clear()

    create_task(remind())
    create_task(timeout())


@router.message(GameRegState.waiting_for_receipt, F.photo | F.document)
async def handle_receipt(message: Message, state: FSMContext):
    telegram_id = message.from_user.id

    try:
        player = await sync_to_async(Player.objects.get)(telegram_id=telegram_id)
        full_name = player.full_name
        phone = player.phone
        player.is_registered_for_game = True
        await sync_to_async(player.save)()
    except Player.DoesNotExist:
        full_name = message.from_user.full_name
        phone = "неизвестно"

    await message.answer("Спасибо! Твоя заявка отправлена на проверку.")

    await message.bot.send_message(
        chat_id=group_chat_id,
        text=f"📥 Новый чек от игрока:\n👤 Имя: {full_name}\n📞 Телефон: {phone}"
    )

    if message.photo:
        await message.bot.send_photo(chat_id=group_chat_id, photo=message.photo[-1].file_id)
    elif message.document:
        await message.bot.send_document(chat_id=group_chat_id, document=message.document.file_id)

    await state.clear()

@router.message(F.text == "/remind")
async def remind_players(message: Message):
    if message.chat.id != my_chat_id:
        return  # Только админ может запускать

    players = await sync_to_async(list)(
        Player.objects.filter(is_registered_for_game=True)
    )

    success_count = 0
    for player in players:
        try:
            await message.bot.send_message(
                chat_id=player.telegram_id,
                text="⚽ Напоминаем! Завтра состоится футбол. До встречи на поле!"
            )
            success_count += 1
        except Exception as e:
            print(f"Не удалось отправить игроку {player.telegram_id}: {e}")

    await message.answer(f"✅ Напоминание отправлено {success_count} участникам.")

@router.message(F.text == "/players")
async def list_registered_players(message: Message):
    if message.chat.id != my_chat_id:
        return  # Только админ может просматривать список

    players = await sync_to_async(list)(Player.objects.all())

    if not players:
        await message.answer("Нет зарегистрированных игроков.")
        return

    msg = "📋 <b>Список зарегистрированных игроков:</b>\n\n"
    for idx, player in enumerate(players, start=1):
        msg += f"{idx}. 👤 {player.full_name} | 📞 {player.phone}\n"

    await message.answer(msg, parse_mode="HTML")


