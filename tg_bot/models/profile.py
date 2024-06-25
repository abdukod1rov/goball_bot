from sqlalchemy import Integer, ForeignKey, String, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

class UserProfile(BaseModel):
    __tablename__ = 'user_profile'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(155), nullable=False)
    last_name: Mapped[str] = mapped_column(String(155), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    photo = Column(String(255), nullable=True)

    user = relationship('User', backref='profile')
