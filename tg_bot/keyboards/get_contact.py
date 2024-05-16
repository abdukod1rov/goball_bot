from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_share_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Kontakni yuborish", request_contact=True),]
],resize_keyboard=True)
