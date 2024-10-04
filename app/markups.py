from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Начать пользоваться")]],
    resize_keyboard=True
)

new_key_markup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Получить новый ключ")]],
    resize_keyboard=True
)

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Проверить дату оплаты")],
        [KeyboardButton(text="Посмотреть список ключей")],
        [KeyboardButton(text="Получить новый ключ")],
    ],
    resize_keyboard=True
)
