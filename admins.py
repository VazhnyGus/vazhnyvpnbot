import sqlite3 as sq
from typing import List

from config import config


ADMIN_PASSWORD = config("ADMIN_PASSWORD")


def create_admin(user_id: str, user_name: str, password: str) -> str:
    if not is_admin(user_id):
        if password == ADMIN_PASSWORD:
            with sq.connect("db/admins.db") as db:
                c = db.cursor()
                c.execute(f"INSERT INTO admins (user_id, user_name) VALUES ('{user_id}', '{user_name}')")
            return "🛠 Вы успешно добавлены в список администраторов"
        else:
            return "Пароль для добавления администратора указан неверно"
    else:
        return "Вы уже администратор"


def delete_admin(user_id: str) -> str:
    if is_admin(user_id):
        with sq.connect("db/admins.db") as db:
            c = db.cursor()
            c.execute(f"DELETE FROM admins WHERE user_id='{user_id}'")
        return "🛠 Вы удалены из списка администраторов"
    else:
        return "Вы не администратор"


def get_admins(user_id: str) -> str:
    if is_admin(user_id):
        with sq.connect("db/admins.db") as db:
            c = db.cursor()
            c.execute("SELECT user_name FROM admins")
            admins = c.fetchall()
        admins_str = "🛠 Список администраторов:\n"
        for admin in admins:
            admins_str += f"\n@{admin[0]}"
        return admins_str
    else:
        return "У вас нет доступа к списку администраторов"


def get_admins_ids() -> List[str]:
    with sq.connect("db/admins.db") as db:
        c = db.cursor()
        c.execute("SELECT user_id FROM admins")
        admins_raw = c.fetchall()
        admins = []
        for admin in admins_raw:
            admins.append(admin[0])
        return admins


def is_admin(user_id: str) -> bool:
    with sq.connect("db/admins.db") as db:
        c = db.cursor()
        c.execute(f"SELECT COUNT(id) FROM admins WHERE user_id='{user_id}'")
        return c.fetchall()[0][0]
