# from aiogram import Router, F
# from aiogram.types import Message, FSInputFile
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from asyncio import create_task, sleep
#
# router = Router()
# admin_chat_id = -4869221063
#
# class GameRegState(StatesGroup):
#     waiting_for_receipt = State()
#
# @router.message(F.text == "/регистрация")
# async def game_register(message: Message, state: FSMContext):
#     await message.answer(
#         "Чтобы записаться на ближайший матч, переведи сумму 50000 сум на карту: 8600 1234 5678 9012\n"
#         "После оплаты, пожалуйста, пришли скриншот или фото чека сюда."
#     )
#     await state.set_state(GameRegState.waiting_for_receipt)
#
#     async def remind():
#         await sleep(900)
#         if await state.get_state() == GameRegState.waiting_for_receipt:
#             await message.answer("Напоминаем! Для участия нужно оплатить и прислать чек.")
#
#     async def timeout():
#         await sleep(3600)
#         if await state.get_state() == GameRegState.waiting_for_receipt:
#             await message.answer("Время для оплаты истекло, твоя регистрация на игру отменена.")
#             await state.clear()
#
#     create_task(remind())
#     create_task(timeout())
#
# @router.message(GameRegState.waiting_for_receipt, F.photo | F.document)
# async def handle_receipt(message: Message, state: FSMContext):
#     full_name = message.from_user.full_name
#     phone = "неизвестно"
#     await message.answer("Спасибо! Твоя заявка отправлена на проверку.")
#
#     await message.bot.send_message(
#         chat_id=admin_chat_id,
#         text=f"Участник: {full_name}\nТелефон: {phone}\nПрислал чек для участия."
#     )
#     if message.photo:
#         await message.bot.send_photo(chat_id=admin_chat_id, photo=message.photo[-1].file_id)
#     elif message.document:
#         await message.bot.send_document(chat_id=admin_chat_id, document=message.document.file_id)
#
#     await state.clear()
