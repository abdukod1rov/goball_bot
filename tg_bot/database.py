from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from tg_bot.config import load_config
from tg_bot.misc.req_func import make_connection_string

config = load_config('bot.ini')
connection = make_connection_string(config.db)

engine = create_async_engine(connection, future=True, echo=False)

new_session = async_sessionmaker(autoflush=False, bind=engine, autocommit=False)
