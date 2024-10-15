from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.middlewares import UserExistingMiddleware
from app.markups import main_markup
from app.services.users import create_new_key, check_payment_date, get_all_keys, make_new_admin
from app.utils.escape import escape


user_router = Router()
user_router.message.middleware(UserExistingMiddleware())


@user_router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        f"С возвращением, {escape(message.from_user.first_name)} 👋🏻",
        reply_markup=main_markup
    )


@user_router.message(F.text == "Проверить дату оплаты")
async def handle_check_payment_date(message: Message) -> None:
    msg = await check_payment_date(message.from_user.id)
    await message.answer(escape(msg), reply_markup=main_markup)


@user_router.message(F.text == "Посмотреть список ключей")
async def handle_get_all_keys(message: Message) -> None:
    msg = await get_all_keys(message.from_user.id)
    await message.answer(msg, reply_markup=main_markup)


@user_router.message(F.text == "Получить новый ключ")
async def handle_create_new_key(message: Message) -> None:
    msg = await create_new_key(message.from_user.id)
    await message.answer(msg, reply_markup=main_markup)


@user_router.message(Command("make_me_admin"))
async def handle_make_me_admin(message: Message) -> None:
    password = message.text.removeprefix("/make_me_admin ")
    msg = await make_new_admin(message.from_user.id, password)
    await message.answer(msg, reply_markup=main_markup)
