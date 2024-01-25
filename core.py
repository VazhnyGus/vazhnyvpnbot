import sqlite3 as sq
import csv
from typing import Optional, Tuple, List
from datetime import date, timedelta

from admins import is_admin
from outlineapi import get_key_from_api, delete_key_from_api, get_usage


MIB = 9.5367431640625e-07


def init_db():
    with sq.connect("db/vpn.db") as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS keys (
            key_id INTEGER NOT NULL UNIQUE,
            key EXT NOT NULL UNIQUE,
            user_id TEXT NOT NULL)"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS users (
            user_id TEXT NOT NULL,
            user_name TEXT NOT NULL,
            expiry_date INTEGER NOT NULL)"""
        )
    with sq.connect("db/admins.db") as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS admins (
            id INTEGER NOT NULL UNIQUE,
            user_id TEXT NOT NULL UNIQUE,
            user_name TEXT NOT NULL,
            PRIMARY KEY(id))"""
        )


def add_new_user(user_id, user_name) -> Optional[str]:
    with sq.connect("db/vpn.db") as db:
        c = db.cursor()
        c.execute(f"SELECT COUNT(user_id) FROM users WHERE user_id = '{user_id}'")
        is_new = c.fetchall()[0][0]
        if not is_new:
            if user_name:
                username = user_name.replace("_", "\\_")
                c.execute(
                    f"INSERT INTO users (user_id, user_name, expiry_date) VALUES ('{user_id}', '{username}', 1095362)"
                )
                return f"🛠 Добавлен новый пользователь @{username}. Установите дату оплаты"
            else:
                c.execute(
                    f"INSERT INTO users (user_id, user_name, expiry_date) VALUES ('{user_id}', 'NoName', 1095362)"
                )
                return "🛠 Добавлен новый пользователь, у которого нет username. Поменяй имя и установи дату оплаты"
        else:
            return None


def change_username(user_id: str, user: str, user_name: str) -> str:
    if is_admin(user_id):
        with sq.connect("db/vpn.db") as db:
            c = db.cursor()
            c.execute(f"UPDATE users SET user_name = '{user_name}\\_changed' WHERE user_id = '{user}'")
            return f"Имя для пользователя с id {user} изменено на {user_name}"
    else:
        return "У вас нет доступа к данному действию"


def get_new_key(user_id) -> Optional[str]:
    key, key_id = get_key_from_api()
    if key:
        with sq.connect("db/vpn.db") as db:
            c = db.cursor()
            c.execute(f"INSERT INTO keys (key_id, key, user_id) VALUES ({key_id}, '{key}', '{user_id}')")
        return key
    return None


def get_all_keys(user_id) -> str:
    with sq.connect("db/vpn.db") as db:
        c = db.cursor()
        c.execute(f"SELECT key FROM keys WHERE user_id='{user_id}'")
        keys_raw = c.fetchall()
    if keys_raw:
        keys = "🔑 Список твоих ключей:"
        for key in keys_raw:
            keys += f"\n\n`{key[0]}`"
        return keys
    else:
        return "🤷🏻‍♂️ У тебя пока нет созданных ключей"


def get_expiry_date(user_id) -> str:
    with sq.connect("db/vpn.db") as db:
        c = db.cursor()
        c.execute(f"SELECT expiry_date FROM users WHERE user_id = '{user_id}'")
        expiry_date = date.fromordinal(c.fetchall()[0][0])
    delta = (expiry_date - date.today()).days
    f_date = expiry_date.strftime('%d.%m.%Y')
    if delta < 0:
        return f"Ну как там с деньгами? Оплата закончилась еще {f_date} 🤷🏻‍♂️"
    elif delta < 2:
        return f"Оплата закончится {f_date}. Завтра последний день. Оплати, пожалуйста 🙏🏻"
    elif delta < 7:
        return f"Оплата закончится {f_date}. Осталась меньше недели. Рекомендую продлить уже сейчас 😉"
    else:
        return f"Оплата закончится {f_date}. Пока можешь не беспокоиться по поводу продления 🕺🏻"


def get_expired() -> Tuple[List[str], List[Tuple[str, str]]]:
    check_date = date.today() + timedelta(days=6)
    almost_expired = []
    expired = []
    with sq.connect("db/vpn.db") as db:
        c = db.cursor()
        c.execute(f"SELECT user_id, user_name, expiry_date FROM users WHERE expiry_date < {check_date.toordinal()}")
        users_raw = c.fetchall()
    for user in users_raw:
        user_id = user[0]
        user_name = user[1]
        expiry_date = user[2]
        if expiry_date < date.today().toordinal():
            expired.append((user_id, user_name))
        else:
            almost_expired.append(user_id)
    return almost_expired, expired


def delete_key(user_id: str, key_id: int) -> str:
    if is_admin(user_id):
        if _check_key(key_id):
            with sq.connect("db/vpn.db") as db:
                c = db.cursor()
                c.execute(f"DELETE FROM keys WHERE key_id={key_id}")
            if delete_key_from_api(key_id):
                return f"🛠 Ключ {key_id} успешно удален"
            else:
                return f"🛠 Ключ {key_id} удален из базы данных, но при удалении из Outline произошла ошибка"
        else:
            return f"🛠 Ключ {key_id} не существует"
    else:
        return "У вас нет доступа к данному действию"


def get_users(user_id: str) -> str:
    if is_admin(user_id):
        with sq.connect("db/vpn.db") as db:
            c = db.cursor()
            c.execute("SELECT * FROM users")
            users_raw = c.fetchall()
        users = "🛠 Список текущих пользователей:\n\n"
        for user in users_raw:
            users += f"@{user[1]} id: `{user[0]}` ({date.fromordinal(user[2]).strftime('%d.%m.%Y')})\n"
        return users
    else:
        return "У вас нет доступа к данному действию"


def get_user(user_id: str, user: str) -> str:
    if is_admin(user_id):
        with sq.connect("db/vpn.db") as db:
            c = db.cursor()
            c.execute(f"SELECT * FROM users WHERE user_id = '{user}'")
            user_raw = c.fetchall()[0]
            expiry_date = date.fromordinal(user_raw[2]).strftime('%d.%m.%Y')
            expired = date.today().toordinal() > user_raw[2]
            user_data = f"🛠 Информация о пользователе @{user_raw[1]}:\n\nid: `{user_raw[0]}`\nОкончание оплаты: {expiry_date} {'(expired)' if expired else ''}\n\nСписок ключей пользователя:"
            c.execute(f"SELECT key_id, key FROM keys WHERE user_id = '{user}'")
            keys_raw = c.fetchall()
            for key in keys_raw:
                usage = round(MIB * get_usage(key[0]), 2) 
                user_data += f"\n\nid: `{key[0]}` (использовано: {usage} MiB)\n`{key[1]}`"
        return user_data
    else:
        return "У вас нет доступа к данному действию"


def change_exp_date(user_id: str, user: str, expiry_date: str) -> str:
    if is_admin(user_id):
        with sq.connect("db/vpn.db") as db:
            ordinal_expiry_date = date.fromisoformat(expiry_date).toordinal()
            c = db.cursor()
            c.execute(f"UPDATE users SET expiry_date='{ordinal_expiry_date}' WHERE user_id='{user}'")
        return f"🛠 Для пользователя {user} установлена дата окончания {expiry_date}"
    else:
        return "У вас нет доступа к данному действию"


def export_data(user_id: str) -> Optional[str]:
    if is_admin(user_id):
        with sq.connect("db/vpn.db") as db:
            c = db.cursor()
            c.execute("SELECT * FROM users")
            users = c.fetchall()
            b_users = []
            for user in users:
                c.execute(f"SELECT key_id, key  FROM keys WHERE user_id = '{user[0]}'")
                user_keys = c.fetchall()
                if len(user_keys) == 0:
                    b_users.append([user[0], user[1], date.fromordinal(user[2]).strftime('%d.%m.%Y')])
                    continue
                for key in user_keys:
                    usage = round(MIB * get_usage(key[0]), 2)
                    expiry_date = date.fromordinal(user[2]).strftime('%d.%m.%Y')
                    b_users.append([user[0], user[1], expiry_date, key[0], key[1], usage])
        with open(f"export.csv", "w", newline="") as csv_file:
            field_names = ["user_id", "user_name", "expiry_date", "key_id", "key", "usage"]
            w = csv.writer(csv_file, delimiter=";")
            w.writerow(field_names)
            for u in b_users:
                w.writerow(u)
        return None
    else:
        return "У вас нет доступа к данному действию"


def _check_key(key_id: int) -> bool:
    with sq.connect("db/vpn.db") as db:
        c = db.cursor()
        c.execute(f"SELECT COUNT(key_id) FROM keys WHERE key_id={key_id}")
        return c.fetchall()[0][0]
