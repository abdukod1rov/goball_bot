import asyncio
import logging
from tg_bot.misc.req_func import make_connection_string
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from tg_bot.handlers.commands.start import router as start_router
from tg_bot.handlers.commands.login import router as login_router
from tg_bot.config import load_config
from tg_bot.models.base import Base, metadata

logger = logging.getLogger(__name__)


async def crate_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",

    )
    logger.error('Starting the bot')
    config = load_config('bot.ini')
    print(config)
    connection = make_connection_string(config.db)
    print('connection', connection)
    engine = create_async_engine(connection, future=True, echo=False
                                 )

    session_fabric = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    storage = MemoryStorage()
    bot = Bot(config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    dp.include_router(start_router)
    dp.include_router(login_router)
    # metadata.create_all(bind=engine)
    await crate_tables(engine=engine)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
