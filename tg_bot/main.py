import asyncio
import logging
import sys
from os import getenv
from aiogram import Router
from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage import redis
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods.get_user_profile_photos import GetUserProfilePhotos
from redis.connection import ConnectionError
from handlers.commands.start import router as start_router
from handlers.commands.login import router as login_router

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7095775641:AAFG0dMZzCMVDAyfdh0wPg77cpjx-oXchj4"

router = Router()

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     """
#     This handler receives messages with `/start` command
#     """
#     # Most event objects have aliases for API methods that can be called in events' context
#     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
#     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
#     # method automatically or call API method directly via
#     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
#     await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message(Command('photos'))
async def get_profile_photos(message: types.Message):
    '''
    Get the user profile photos
    '''
    profile_pics = await bot.get_user_profile_photos(message.from_user.id)
    if profile_pics.total_count > 0:
        await message.answer('good')
        await message.answer_photo(dict((profile_pics.photos[0][0])).get('file_id'))
        return
    await message.answer('u dont have profile pictures', show_alert=True)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    dp.include_router(router)
    dp.include_router(start_router)
    dp.include_router(login_router)
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)
        await r.set('OK', 'True')
        # Now you can reuse `r` throughout your application
    except ConnectionError as e:
        # Handle connection error gracefully
        print("Failed to connect to Redis:", e)
        return
    await bot.send_message(chat_id=1324271506, text="Bot started!")
    await dp.start_polling(bot, on_startup=on_startup(r))

    # await bot.send_message(chat_id=1324271506, text="Bot started!")

async def go():
    ...
async def on_startup(redis_conn: redis.Redis):
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
