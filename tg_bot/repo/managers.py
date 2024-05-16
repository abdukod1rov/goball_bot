from typing import Optional

from passlib.context import CryptContext

from tg_bot.database import new_session
from tg_bot.models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_passcode(plain_passcode, hashed_passcode):
    return pwd_context.verify(plain_passcode, hashed_passcode)


def get_passcode_hash(passcode):
    return pwd_context.hash(passcode)



