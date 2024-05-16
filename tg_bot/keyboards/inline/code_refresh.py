from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def code_refresh_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='🔄 Kodni yangilash', callback_data='code_refresh')
    return builder.as_markup()

