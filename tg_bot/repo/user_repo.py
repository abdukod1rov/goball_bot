from typing import Union

from .base_repo import BaseSQLAlchemyRepo
from .managers import get_passcode_hash
from ..database import new_session
from ..models.user import User
from ..schemas.user_schema import UserInCreate
from ..models import UserProfile
from sqlalchemy import insert, select, update


class UserRepo:

    @classmethod
    async def add_user(cls, user_data: UserInCreate):
        async with new_session() as session:
            user_dict = user_data.model_dump()
            sql = insert(User).values(**user_dict)
            result = await session.execute(sql)
            await session.flush()
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def create_profile(cls, user_id: int, first_name: str, last_name: str = None, username: str = None):
        """
        Here we create a profile page for each new user
        :parameters -> first_name is required
        since not each user has telegram username, we need to get first name
        username and last_name will be also added to the database unless they're null
        """
        async with new_session() as session:
            sql = insert(UserProfile).values(user_id=user_id, first_name=first_name, last_name=last_name,
                                             username=username)
            result = await session.execute(sql)
            await session.flush()
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def get_profile(cls, user_id: int):
        async with new_session() as session:
            sql = select(UserProfile).filter(UserProfile.user_id == user_id)
            result = await session.execute(sql)
            return result.scalar_one_or_none()

    @classmethod
    async def get_user(cls, user_id: int) -> Union[User, None]:
        async with new_session() as session:
            sql = select(User).where(User.tg_id == user_id)
            result = await session.execute(sql)
            user = result.scalar_one_or_none()
            return user

    @classmethod
    async def get_users(cls) -> list[User]:
        async with new_session() as session:
            sql = select(User)
            request = await session.execute(sql)
            return request.scalar()

    @classmethod
    async def update_phone_number(cls, user_id: int, phone_number: str):
        async with new_session() as session:
            sql = update(User).values(phone_number=phone_number).where(User.tg_id == user_id
                                                                       ).returning(User)
            result = await session.execute(sql)
            await session.commit()
            return result.scalar_one_or_none()
