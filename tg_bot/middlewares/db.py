from abc import ABC
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.orm import sessionmaker

from aiogram import BaseMiddleware
from aiogram.types import Message

from tg_bot.repo.repository import SQLAlchemyRepos


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)


class DbSessionMiddleware(BaseMiddleware, ABC):
    skip_patterns = ["error", "update"]

    def __init__(self, session_pool: sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def pre_process(self, obj, data, *args):
        session = self.session_pool()
        data['session'] = session
        repo = SQLAlchemyRepos(session)
        data['repo'] = repo

    async def post_process(self, obj, data, *args):
        session = data.get("session")
        if session:
            await session.close()
            del data["session"]
            del data["repo"]
