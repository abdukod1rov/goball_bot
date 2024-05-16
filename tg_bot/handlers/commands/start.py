from aiogram import types, F
from aiogram import Router
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import Command

from tg_bot.handlers.commands.login import generate_otp
from tg_bot.keyboards.inline.code_refresh import code_refresh_markup
from tg_bot.keyboards.inline.language import language_markup
from tg_bot.repo.repository import SQLAlchemyRepos
from tg_bot.repo.user_repo import UserRepo
from tg_bot.schemas.user_schema import UserInCreate
from tg_bot.keyboards import contact_share_button
from tg_bot.redis_connect import get_redis_connection

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, ) -> None:
    await message.answer(text="Iltimos telefon raqamingizni kiriting", reply_markup=contact_share_button)
    return
    #
    # else:
    #     existing_code = await redis_conn.get(str(user_id))
    #
    #     # We need to check if the user already has been provided with the passcode
    #     if existing_code:
    #         await message.answer(text="Eski kodingiz hali ham kuchda ☝️", show_alert=True)
    #         return
    #     passcode = generate_otp()
    #     print('passcode is: ', passcode)
    #     await redis_conn.set(f'{user_id}', str(passcode), ex=30)  # Set expire time 2 minutes
    #     await redis_conn.set(f"{passcode}", str(user_id), ex=30)  # Set expire time for 2 minutes
    #     await message.answer(text=f'🔒 Kodingiz: `{str(passcode)}`', parse_mode=ParseMode.MARKDOWN,
    #                          reply_markup=code_refresh_markup())
    #     return


@router.message(F.contact)
async def cmd_contact(message: types.Message) -> None:
    user_id = message.from_user.id
    phone_number = str(message.contact.phone_number)
    user = await UserRepo.get_user(user_id=user_id)
    if user is None:
        user_to_add = UserInCreate(phone_number=phone_number, tg_id=user_id)
        new_user = await UserRepo.add_user(user_to_add)
        if new_user is None:
            await message.answer(text="Serverda xatolik,iltimos keyinroq urunib ko'ring!", show_alert=True)
    else:
        modified_phone_number = phone_number[3:]
        await UserRepo.update_phone_number(user_id=user_id, phone_number=modified_phone_number)
    redis_conn = await get_redis_connection()
    if redis_conn is None:
        await message.answer(text="Serverda xatolik,iltimos keyinroq urunib ko'ring!", show_alert=True)
        return
    existing_code = await redis_conn.get(str(user_id))

    # We need to check if the user already has been provided with the passcode
    if existing_code:
        await message.answer(text="Eski kodingiz hali ham kuchda ☝️")
        return
        # await redis_conn.delete(str(user_id), str(existing_code))
    passcode = generate_otp()
    print('passcode is: ', passcode)
    await redis_conn.set(f'{user_id}', str(passcode), ex=30)  # Set expire time 2 minutes
    await redis_conn.set(f"{passcode}", str(user_id), ex=30)  # Set expire time for 2 minutes
    await message.answer(text=f'🔒 Kodingiz: `{str(passcode)}`', parse_mode=ParseMode.MARKDOWN,
                         reply_markup=code_refresh_markup())
    await message.answer(text="🔑 Yangi kod olish uchun /login ni bosing")
    return
