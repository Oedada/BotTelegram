from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

change_pos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Погода сейчас',  callback_data='weather_now')],
    [InlineKeyboardButton(text='Прогноз',  callback_data='wheather_forecast')]
])


