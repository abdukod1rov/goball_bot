from datetime import datetime
import re
from sqlalchemy import String, TIMESTAMP, text, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates, Relationship

from .base import Base
from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(Integer, nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(server_default=text('true'), nullable=False)
    # email: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    last_login: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(server_default=text('false'), nullable=False)
    is_staff: Mapped[bool] = mapped_column(server_default=text('false'), nullable=False)

    stadiums = Relationship('Stadium', back_populates='owner', uselist=True, passive_deletes=True)
    roles = Relationship('Role', secondary='user_roles', passive_deletes=True, back_populates='users')

    @validates('email')
    def validate_email(self, key, email):
        # assert len(email) > 10
        # assert @ in mail
        if email is not None:
            if '@' not in email:
                raise ValueError('invalid email address, bor togirla')
            return email

    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        """
        Example phone number --> 8908211633

        """
        pattern = r'^8\d{9}'
        pattern = r'^8\d{9}$'
        if not re.match(pattern, phone_number):
            raise ValueError('invalid phone number')
        return phone_number

    def __repr__(self):
        return f'User(id={self.id!r}, phone={self.phone_number!r}, roles: {self.roles})'
