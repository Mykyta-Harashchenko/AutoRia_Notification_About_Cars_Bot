from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


async def get_start_kb() -> KeyboardButton:
    return KeyboardButton(text="Поставити нагадування")
