from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base
from datetime import datetime

from sqlalchemy import BigInteger, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()
metadata = Base.metadata


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=text('now()'))
