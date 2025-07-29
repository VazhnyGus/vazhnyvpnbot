import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from app.handlers.admins import admin_router
from app.handlers.users import user_router
from app.database.models import create_tables_async
from app.utils.config import config


async def main() -> None:
    await create_tables_async()
    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        filename="/app/external/logs/.log",
        level=logging.ERROR,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    asyncio.run(main())
