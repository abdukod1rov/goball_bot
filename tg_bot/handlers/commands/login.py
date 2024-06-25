from aiogram import types, Router
from aiogram.filters import Command
import secrets

from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage import redis
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from tg_bot.keyboards.inline.code_refresh import code_refresh_markup
from tg_bot.redis_connect import get_redis_connection
from tg_bot.repo import user_repo


# Function to generate a random secret key
def generate_secret_key():
    return secrets.token_hex(20)  # 16 bytes (32 hex characters)


# Function to generate a One Time Password (OTP) using the secret key
def generate_otp(length=4) -> str:
    # Defining the characters allowed in the OTP
    allowed_characters = "0123456789"

    # Generating a random OTP using the secret key and allowed characters
    otp = ''.join(secrets.choice(allowed_characters) for _ in range(length))

    return otp


router = Router()


# @router.message(Command('login'))
# async def login(message: types.Message):
#     user = await user_repo.UserRepo.get_user(user_id=message.from_user.id)
#     if user is not None:
#         passcode = await user_repo.UserRepo.add_attempt(user)
#         print('passcode is: ', passcode)
#         print(user)
#         print(user.tg_id, user.phone_number)
#         await message.answer(text=f'🔒 Kodingiz: `{str(passcode)}`', parse_mode=ParseMode.MARKDOWN,
#                              reply_markup=code_refresh_markup())
#     else:
#         await message.answer(text='OK!')
@router.message(Command('login'))
async def login(message: types.Message):

    user_id = message.from_user.id
    redis_conn = await get_redis_connection()
    if redis_conn is None:
        await message.answer(text="Serverda xatolik,iltimos keyinroq urunib ko'ring!")
        return
    existing_code = await redis_conn.get(str(user_id))

    # We need to check if the user already has been provided with the passcode
    if existing_code:
        await message.answer(text="Eski kodingiz hali ham kuchda ☝️", show_alert=True)
        return
    else:
        passcode = generate_otp()
        # Ensure the passcode is unique before assigning it to the user
        while True:
            if await redis_conn.setnx(str(passcode), str(user_id)):
                # If the passcode is successfully set, exit the loop
                break
            else:
                # If the passcode already exists, generate a new one
                passcode = generate_otp()
        print('passcode is: ', passcode)

        # Set the expiration time for the passcode key
        await redis_conn.expire(str(passcode), 30)  # Set expire time 2 minutes
        # Store the passcode associated with the user ID
        await redis_conn.set(str(user_id), str(passcode), ex=30)  # Set expire time
        await message.answer(text=f'🔒 Kodingiz: `{str(passcode)}`', parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=code_refresh_markup())


@router.callback_query(lambda call: call.data.startswith('code_refresh'))
async def code_callback(query: CallbackQuery):
    user_id = query.from_user.id
    redis_conn = await get_redis_connection()
    if redis_conn is None:
        await query.answer(text="Serverda xatolik,iltimos keyinroq urunib ko'ring!", show_alert=True)
        return
    existing_code = await redis_conn.get(str(user_id))

    # We need to check if the already has been provided with the passcode
    if existing_code:
        await query.answer(text="Eski kodingiz hali ham kuchda ☝️", show_alert=True)
        return
    else:
        passcode = generate_otp()
        print('passcode is: ', passcode)
        await redis_conn.set(f'{user_id}', str(passcode), ex=30)  # Set expire time 2 minutes
        await redis_conn.set(f"{passcode}", str(user_id), ex=30)  # Set expire time for 2 minutes

        await query.message.edit_text(text=f'🔒 Kodingiz: `{str(passcode)}`', parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=code_refresh_markup())
        # await query.message.answer(text=f'🔒 Kodingiz: `{str(passcode)}`', parse_mode=ParseMode.MARKDOWN,
        #                            reply_markup=code_refresh_markup())
        return


# @router.message(Command('start'))
# async def cmd_start(message: types.Message, ) -> None:
#     user_id = message.from_user.id
#     if await UserRepo.get_user(user_id=user_id) is None:
#         await message.answer(text="Iltimos telefon raqamingizni kiriting", reply_markup=contact_share_button)
#
