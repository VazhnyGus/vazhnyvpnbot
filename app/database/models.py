from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.utils.config import config


engine = create_async_engine(config.database_url)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str]
    payment_date: Mapped[int]
    is_admin: Mapped[bool]


class Key(Base):
    __tablename__ = "keys"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    access_url: Mapped[str]
    user: Mapped[int]


async def create_tables_async() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
