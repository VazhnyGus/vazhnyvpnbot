from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Any, Awaitable

from app.database.requests import check_admin, check_user, add_user_to_db
from app.markups import start_markup


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        is_admin = await check_admin(event.from_user.id)
        if is_admin:
            return await handler(event, data)
        else:
            await event.answer("У вас нет доступа к данному действию")


class UserExistingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        is_user = await check_user(event.from_user.id)
        if is_user:
            return await handler(event, data)
