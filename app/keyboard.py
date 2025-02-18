from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
twoday = (datetime.now() + timedelta(2)).weekday()
threeday = (datetime.now() + timedelta(3)).weekday()
weekdays = {0: "Понедельник", 1:"Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресение"}

change_pos = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Погода сейчас',  callback_data='weather_now')],
    [InlineKeyboardButton(text='Прогноз',  callback_data='wheather_forecast')]
])
select_day = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Завтра',  callback_data='tomorrow')],
    [InlineKeyboardButton(text='Послезавтра',  callback_data='after_tomorrow')],
    [InlineKeyboardButton(text=weekdays[twoday],  callback_data='aa_tomorrow')]
])
weather = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Посмотреть погоду")]
], resize_keyboard=True)
