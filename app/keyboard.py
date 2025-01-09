from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data_weather import CITIES_RUSSAIN_ENGLISH

services = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Погода")],
    [KeyboardButton(text="Переводчик")]
])


change_city = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сменить город', callback_data='change_city')]
])


async def cities_kb():
    keyboard = InlineKeyboardBuilder()
    for city in sorted(CITIES_RUSSAIN_ENGLISH.keys()):
        keyboard.add(InlineKeyboardButton(text=city, callback_data=CITIES_RUSSAIN_ENGLISH[city]))
    return keyboard.adjust(3).as_markup()