from outline_vpn import OutlineServerErrorException
from datetime import date

from app.services.outline import create_new_outline_key
from app.database.requests import add_key_to_db, get_user_info_from_db, set_admin
from app.utils.config import config


KEY_PRICE = 100


async def create_new_key(user_id: int) -> str:
    try:
        key = await create_new_outline_key()
        key_id = key.key_id
        access_url = key.access_url
        await add_key_to_db(key_id, access_url, user_id)
        return (f"Вот твой новый ключ 🔑\n\n`{access_url}`\n\nСкопируй, нажав на него, и добавь в приложение Outline"
                f"\n\n💰 Не забудь оплатить его")
    except OutlineServerErrorException:
        return "😔 Не удалось выпустить новый ключ\. Обратись за помощью к администратору"


async def check_payment_date(user_id: int) -> str:
    user_info = await get_user_info_from_db(user_id)
    quantity_of_keys = len(user_info.keys)
    str_payment_date = date.fromordinal(user_info.payment_date)
    delta = (str_payment_date - date.today()).days
    str_payment_date = str_payment_date.strftime('%d.%m.%Y')
    renewal_cost_text = f"\n\nСтоимость продления на месяц: {KEY_PRICE * quantity_of_keys}₽"
    if delta < 0:
        return f"Ну как там с деньгами? Оплата закончилась еще {str_payment_date} 🤷🏻‍♂️" + renewal_cost_text
    elif delta < 7:
        return (f"Оплата закончится меньше, чем через неделю \({str_payment_date}\). "
                f"Рекомендую продлить уже сейчас 😉") + renewal_cost_text
    else:
        return f"Оплата закончится {str_payment_date}. Пока можешь не беспокоиться по поводу продления 🕺🏻"


async def get_all_keys(user_id: int) -> str:
    user_info = await get_user_info_from_db(user_id)
    msg = "🔑 Список твоих ключей:"
    for key in user_info.keys:
        key_id, access_url = key
        msg += f"\n\n{key_id}: `{access_url}`"
    return msg


async def make_new_admin(user_id: int, password: str) -> str:
    if password == config.admin_password:
        await set_admin(user_id)
        return "🛠 Теперь вы администратор"
    else:
        return "🛠 Неверный пароль"
