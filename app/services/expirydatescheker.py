import asyncio
from aiogram import Bot
from datetime import date

from app.database.requests import get_users_from_db, get_user_info_from_db
from app.utils.escape import escape
from app.services.users import KEY_PRICE


EXPIRY_DATES_CHECKING_INTERVAL = 5


async def check_expired_dates(bot: Bot) -> None:
    while True:
        await asyncio.sleep(EXPIRY_DATES_CHECKING_INTERVAL * 86400)
        users = await get_users_from_db()
        users_with_expired_dates = [user for user in users if date.fromordinal(user.payment_date) < date.today()]
        for user in users_with_expired_dates:
            user_info = await get_user_info_from_db(user.id)
            user_keys_quantity = len(user_info.keys)
            msg = (f"💸 Оплата закончилась {escape(date.fromordinal(user.payment_date).strftime('%d.%m.%Y'))}\n"
                   f"Внеси {KEY_PRICE * user_keys_quantity}₽ или более для продления обслуживания")
            await bot.send_message(user.id, msg)
        admins = [user.id for user in users if user.is_admin is True]
        for admin in admins:
            expired = "\n".join([
                f"`{user.id}` \| {escape(user.name)} \| "
                f"{escape(date.fromordinal(user.payment_date).strftime('%d.%m.%Y'))}" for user in users_with_expired_dates
            ])
            msg = f"🛠 У этих пользователей кончилась оплата:\n\n{expired}"
            await bot.send_message(admin, msg)
