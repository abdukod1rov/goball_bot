import datetime
from datetime import datetime as time_date

from pydantic import BaseModel, Field

from tg_bot.repo import UserRepo


class OTPTime(BaseModel):
    created_at: datetime.datetime = Field(alias='createdAt', default=time_date.now())
    expires: int = Field(default=60 * 5)  # 300 seconds == 5 minutes


class OTPSchema(BaseModel):
    phone_number: str
    otp: str



