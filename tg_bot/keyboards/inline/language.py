from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tg_bot.data.data import languages


def language_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code, name in languages.items():
        builder.button(text=name, callback_data=name)

    return builder.as_markup()
