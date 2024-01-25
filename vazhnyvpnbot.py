import asyncio
from telebot.async_telebot import AsyncTeleBot, types

from admins import create_admin, delete_admin, get_admins, get_admins_ids
from core import (init_db, delete_key, get_users, change_exp_date, add_new_user,
                  get_new_key, get_all_keys, get_expiry_date, get_expired,
                  export_data, get_user, change_username)
from config import config


BOT_TOKEN = config("BOT_TOKEN")


bot = AsyncTeleBot(token=BOT_TOKEN)


def _main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    check_date_button = types.KeyboardButton("Проверить дату оплаты")
    get_keys_button = types.KeyboardButton("Список ключей")
    get_new_key_button = types.KeyboardButton("Получить новый ключ")
    markup.add(check_date_button, get_keys_button, get_new_key_button)
    return markup


@bot.message_handler(commands="setadmin")
async def set_admin(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    message_text = message.text.split(" ")
    password = message_text[1]
    result = create_admin(user_id, user_name, password)
    await bot.send_message(user_id, result)


@bot.message_handler(commands="unsetadmin")
async def unset_admin(message):
    user_id = message.from_user.id
    result = delete_admin(user_id)
    await bot.send_message(user_id, result)


@bot.message_handler(commands="admins")
async def admins(message):
    user_id = message.from_user.id
    result = get_admins(user_id)
    await bot.send_message(user_id, result)


@bot.message_handler(commands="removekey")
async def remove_key(message):
    user_id = message.from_user.id
    message_text = message.text.split(" ")
    key_id = message_text[1]
    result = delete_key(user_id, int(key_id))
    await bot.send_message(user_id, result)


@bot.message_handler(commands="users")
async def users(message):
    user_id = message.from_user.id
    result = get_users(user_id)
    await bot.send_message(user_id, result, parse_mode="Markdown")


@bot.message_handler(commands="user")
async def get_user_cmd(message):
    user_id = message.from_user.id
    message_text = message.text.split(" ")
    user = message_text[1]
    result = get_user(user_id, user)
    await bot.send_message(user_id, result, parse_mode="Markdown")


@bot.message_handler(commands="setdate")
async def set_date(message):
    user_id = message.from_user.id
    message_text = message.text.split(" ")
    user = message_text[1]
    date = message_text[2]
    result = change_exp_date(user_id, user, date)
    await bot.send_message(user_id, result)


@bot.message_handler(commands="changename")
async def change_name(message):
    user_id = message.from_user.id
    message_text = message.text.split(" ")
    user = message_text[1]
    user_name = message_text[2]
    result = change_username(user_id, user, user_name)
    await bot.send_message(user_id, result)


@bot.message_handler(commands="export")
async def export(message):
    user_id = message.from_user.id
    result = export_data(user_id)
    if not result:
        with open("export.csv", "rb") as f:
            await bot.send_document(user_id, f)
    else:
        await bot.send_message(user_id, result)


@bot.message_handler(commands="start")
async def start(message):
    start_button = types.KeyboardButton("Начать пользоваться")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(start_button)
    await bot.send_message(
        message.from_user.id,
        "Добро пожаловать в бота VazhnyVPN 👋🏻\nНажми на кнопку, чтобы перейти к меню\n\n👇👇👇",
        reply_markup=markup
    )


@bot.message_handler(content_types=["text"])
async def main(message):
    text = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    if text == "Начать пользоваться":
        is_new = add_new_user(user_id, user_name)
        if is_new:
            admin_ids = get_admins_ids()
            for admin_id in admin_ids:
                await bot.send_message(admin_id, is_new)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            get_new_key_button = types.KeyboardButton("Получить новый ключ")
            markup.add(get_new_key_button)
            await bot.send_message(
                user_id,
                "Кажется, ты новенький 🐣 \nТебе нужно получить новый ключ. Для этого нажми на кнопку ниже\n\n👇👇👇",
                reply_markup=markup
            )
        else:
            await bot.send_message(
                user_id,
                "Я знаю, что ты уже пользуешься VazhnyVPN 🐥\nТы можешь посмотреть дату оплаты, список ключей или получить еще один.\nВыбери соответствующее действие ниже\n\n👇👇👇",
                reply_markup=_main_markup()
            )
    elif text == "Получить новый ключ":
        key = get_new_key(user_id)
        admin_ids = get_admins_ids()
        if key:
            for admin_id in admin_ids:
                await bot.send_message(admin_id, f"🛠 @{user_name} только что получил новый ключ. Проверь, оплатил ли он его")
            await bot.send_message(
                user_id,
                f"Вот твой новый ключ 🔑\n\n`{key}`\n\nСкопируй, нажав на него, и добавь его в приложение Outline\n\n💰 Не забудь оплатить его",
                reply_markup=_main_markup(),
                parse_mode="Markdown"
            )
        else:
            for admin_id in admin_ids:
                await bot.send_message(admin_id, f"🛠 @{user_name} не смог получить ключ. Что-то пошло не так")
            await bot.send_message(
                user_id,
                "😿 Не удалось получить ключ. Обратись к @egorgovorukhin"
            )

    elif text == "Список ключей":
        keys = get_all_keys(user_id)
        await bot.send_message(
            user_id,
            keys,
            reply_markup=_main_markup(),
            parse_mode="Markdown"
        )
    elif text == "Проверить дату оплаты":
        expiry_text = get_expiry_date(user_id)
        await bot.send_message(
            user_id,
            expiry_text
        )


async def check_expired():
    while True:
        almost_expired, expired = get_expired()
        if len(almost_expired) > 0:
            for user in almost_expired:
                await bot.send_message(user, "До окончания оплаты осталось меньше недели 📆\nОбратись к @egorgovorukhin, чтобы продлить обслуживание")
        if len(expired) > 0:
            expired_str = "🛠 У этих пользователей кончилась оплата:\n"
            for user in expired:
                await bot.send_message(user[0], "У тебя закончилась оплата ⌛\n Обратись к @egorgovorukhin, чтобы продлить обслуживание")
                expired_str += f"\n@{user[1]}"
            admin_ids = get_admins_ids()
            for admin_id in admin_ids:
                await bot.send_message(admin_id, expired_str)
        await asyncio.sleep(604800)


async def m():
    await asyncio.gather(bot.polling(none_stop=True), check_expired())


if __name__ == "__main__":
    init_db()
    asyncio.run(m())
