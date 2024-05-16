# from datetime import datetime
# import sqlalchemy as sa
# from sqlalchemy.orm import relationship
#
# from tg_bot.models.base import Base, BaseModel
# from tg_bot.models.user import User
#
#
# class LoginAttempt(Base):
#     __tablename__ = 'login_attempt'
#
#     """ Describes a single registration attempt with an identifier """
#
#     id = sa.Column(sa.Integer(), primary_key=True)
#     hashed_code = sa.Column(
#         sa.String(), index=True, nullable=False
#     )
#     timestamp = sa.Column(sa.DateTime(), default=datetime.utcnow)
#
#     user_id = sa.Column(sa.Integer(), sa.ForeignKey("user_account.id"), nullable=False)
#     user = relationship(User, uselist=False)
#
#     # Possibly, add more meta info ? status, IP, etc
#
#     def is_valid(self) -> bool:
#         return (
#                 datetime.utcnow() - self.timestamp
#         ).seconds < 30
