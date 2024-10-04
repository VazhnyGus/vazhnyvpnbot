from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.middlewares import IsAdminMiddleware
from app.services.admins import get_users, get_user, delete_user, delete_key, change_payment_date


admin_router = Router()
admin_router.message.middleware(IsAdminMiddleware())


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
