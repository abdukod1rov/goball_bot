from datetime import datetime
from typing import Union, Any
from pydantic import EmailStr
from pydantic import BaseModel, Field, field_validator, ValidationError
import re


def concepts():
    """
    By default, models are mutable and field values can be changed through attribute assignment.
    """


def validate_phone_number(phone_number: str) -> str:
    """
    Validate the format of a phone number.
    Raises a ValueError if the phone number is invalid.
    """
    pattern = r'^+\d{12}$'
    if not re.match(pattern, phone_number):
        raise ValueError('Invalid phone number')
    return phone_number


class UserPhoneNumber(BaseModel):
    phone_number: str

    _validate_phone_number = field_validator(__field='phone_number')(validate_phone_number)


class UserBase(BaseModel):
    phone_number: str = Field(
        description='User telefon raqami. Unique bo\'lish kerak',
        pattern=r'^8\d{9}',
        examples=['8908211633', ]
    )
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    username: Union[str, None] = None

    _validate_phone_number = field_validator(__field='phone_number')(validate_phone_number)


class UserOut(UserBase):
    id: int = Field(frozen=True)  # immutable
    tg_id: int
    is_active: bool  # 3 dots means it is required
    is_staff: bool
    is_superuser: bool
    last_login: Union[datetime, None] = None
    date_joined: datetime


class UserLogin(BaseModel):
    phone_number: str = Field(
        description='User telefon raqami. Unique bo\'lish kerak',
        pattern=r'^8\d{9}',
        examples=['8908211633', ]
    )
    password: str

    _validate_phone_number = field_validator(__field='phone_number')(validate_phone_number)


class UserInCreate(BaseModel):
    tg_id: int = ...
    phone_number: str = ...



class UserAdminInCreate(UserInCreate):
    is_staff: bool = True


class UserSuperAdminCreate(UserAdminInCreate):
    is_superuser: bool = True


class UserInUpdate(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    is_active: Union[bool, None] = None
    is_staff: Union[bool, None] = None
    is_superadmin: Union[bool, None] = None
    password: Union[str, None] = None


class UserInDb(UserBase):
    hashed_password: str


class UserWithToken(UserBase):
    access_token: str


class UserLogInResponse(BaseModel):
    user: UserWithToken


# class UserInDbCheck(BaseModel):
#     phone_number: str
#     username: str
#     email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone_number: Union[str, None] = None
