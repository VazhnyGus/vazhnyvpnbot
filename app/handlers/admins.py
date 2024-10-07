from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.middlewares import IsAdminMiddleware
from app.services.admins import get_users, get_user, delete_user, delete_key, change_payment_date, get_list_of_users
from app.utils.escape import escape


admin_router = Router()
admin_router.message.middleware(IsAdminMiddleware())


class MessageState(StatesGroup):
    message = State()


@admin_router.message(Command('users'))
async def handle_users(message: Message) -> None:
    msg = await get_users()
    await message.answer(msg)


@admin_router.message(Command('user'))
async def handle_user(message: Message) -> None:
    user_id = int(message.text.removeprefix("/user "))
    msg = await get_user(user_id)
    await message.answer(msg)


@admin_router.message(Command('delete_user'))
async def handle_delete_user(message: Message) -> None:
    user_id = int(message.text.removeprefix("/delete_user "))
    msg = await delete_user(user_id)
    await message.answer(msg)


@admin_router.message(Command('delete_key'))
async def handle_delete_key(message: Message) -> None:
    key_id = int(message.text.removeprefix("/delete_key "))
    msg = await delete_key(key_id)
    await message.answer(msg)


@admin_router.message(Command('set_date'))
async def handle_set_date(message: Message) -> None:
    user_id, date = message.text.removeprefix("/set_date ").split()
    msg = await change_payment_date(int(user_id), date)
    await message.answer(msg)


@admin_router.message(Command('message'))
async def handle_message(message: Message, state: FSMContext) -> None:
    msg = message.text.removeprefix("/message ")
    await state.set_state(MessageState.message)
    await state.update_data(message=msg)
    await message.answer(f"🛠 Вы уверены, что хотите массово отправить сообщение?\n\n>{escape(msg)}")


@admin_router.message(MessageState.message)
async def handle_message_confirm(message: Message, state: FSMContext) -> None:
    if message.text.lower() == "да":
        data = await state.get_data()
        users = await get_list_of_users()
        for user in users:
            await message.bot.send_message(user, escape(data["message"]))
    else:
        await message.answer("🛠 Отправка отменена")
