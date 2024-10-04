from datetime import date

from app.database.requests import (get_users_from_db, get_user_info_from_db, delete_user_from_db,
                                   delete_key_from_db, change_payment_date_in_db)
from app.utils.escape import escape


async def get_users() -> str:
    users = await get_users_from_db()
    return (
        "🛠 Список текущих пользователей:\n\n" +
        "\n".join([
            f"`{user.id}` \| {escape(user.name)} \| "
            f"{escape(date.fromordinal(user.payment_date).strftime('%d.%m.%Y'))}" for user in users
        ])
    )


async def get_user(user_id: int) -> str:
    user = await get_user_info_from_db(user_id)
    if user:
        name = escape(user.name)
        payment_date = escape(date.fromordinal(user.payment_date).strftime('%d.%m.%Y'))
        keys = "\n\n".join(
            [f"id: `{key_id}`\n`{access_url}`" for key_id, access_url in user.keys]
        )
        return (f"🛠 Информация о пользователе `{user_id}`\n\n"
                f"Имя: {name}\nОкончание оплаты: {payment_date}\n\n"
                f"Список ключей пользователя:\n\n{keys}")
    else:
        return f"🛠 Пользователя `{user_id}` не существует"


async def delete_user(user_id: int) -> str:
    user = await get_user_info_from_db(user_id)
    if user:
        keys_quantity = len(user.keys)
        if keys_quantity > 0:
            return (f"🛠 У пользователя `{user.user_id}` есть действующие ключи\. Сначала удалите их")
        else:
            await delete_user_from_db(user_id)
            return f"🛠 Пользователь `{user_id}` удален"
    else:
        return f"🛠 Пользователя `{user_id}` не существует"



async def delete_key(key_id: int) -> str:
    if await delete_key_from_db(key_id):
        return f"🛠 Ключ `{key_id}` успешно удален"
    else:
        return f"🛠 Ключа с id `{key_id}` не существует"


async def change_payment_date(user_id: int, payment_date: str) -> str:
    ordinal_payment_date = date.fromisoformat(payment_date).toordinal()
    if await change_payment_date_in_db(user_id, ordinal_payment_date):
        return (f"🛠 Для пользователя `{user_id}` установлена дата "
                f"{escape(date.fromordinal(ordinal_payment_date).strftime('%d.%m.%Y'))}")
    else:
        return f"🛠 Пользователя `{user_id}` не существует"
