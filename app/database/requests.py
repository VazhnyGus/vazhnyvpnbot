from zoneinfo import reset_tzpath

from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, Key
from app.models import UserInfo


async def check_admin(user_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        return user.is_admin


async def check_user(user_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        return True if user is not None else False


async def add_user_to_db(user_id: int, name: str) -> None:
    async with async_session() as session:
        user = User(id=user_id, name=name, payment_date=766644, is_admin=False)
        session.add(user)
        await session.commit()


async def add_key_to_db(key_id: int, access_url: str, user_id: int) -> None:
    async with async_session() as session:
        key = Key(id=key_id, access_url=access_url, user=user_id)
        session.add(key)
        await session.commit()


async def get_user_info_from_db(user_id: int) -> UserInfo | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        if user:
            user_keys = await session.scalars(select(Key).where(Key.user == user_id))
            return UserInfo(user.name, user.id, user.payment_date, [(key.id, key.access_url) for key in user_keys.all()])
        else:
            return None


async def get_users_from_db() -> list[User]:
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users.all()


async def delete_key_from_db(key_id: int) -> bool:
    async with async_session() as session:
        key = await session.scalar(select(Key).where(Key.id == key_id))
        if key:
            session.delete(key)
            await session.commit()
            return True
        else:
            return False


async def delete_user_from_db(user_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        session.delete(user)
        await session.commit()


async def change_payment_date_in_db(user_id: int, payment_date: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        if user:
            user.payment_date = payment_date
            await session.commit()
            return True
        else:
            return False


async def set_admin(user_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        user.is_admin = True
        await session.commit()


async def get_admins_ids() -> list[int]:
    async with async_session() as session:
        users = await session.scalars(select(User))
        return [user.id for user in users.all() if user.is_admin == True]
