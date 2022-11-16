from aiogram import Bot, Dispatcher

from bot import main_dispatcher, ai_bot
from models.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import config


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASS}@"
        f"{config.POSTGRES_HOST}/{config.POSTGRES_DB}",
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    bot.__setattr__('db', async_sessionmaker)
    await bot.delete_webhook()

if __name__ == "__main__":
    main_dispatcher.startup.register(on_startup)
    main_dispatcher.run_polling(ai_bot)
