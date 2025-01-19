from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import CommandStart

import aiohttp
from config import API_KEY
from app.user_processor import users_db


import app.keyboard as kb

db = users_db()
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Здраствуйте отправте вашу геопозицию, для определения погоды.")


@router.message(F.location)
async def change_city(message: Message):
    '''Once again sends user a message with list of cities'''
    db.set_user_param(message.from_user.id, 'latitude', "%.20f" % message.location.latitude)
    print(message.location.latitude)
    db.save()
    db.set_user_param(message.from_user.id, 'longitude', "%.20f" % message.location.longitude)
    print(message.location.longitude)
    db.save()
    await message.answer('Ваша позиция обработана, выберите, какую погоду вы хотите получить.', reply_markup=kb.change_pos)


@router.callback_query(F.data == "weather_now")
async def change_city(callback: CallbackQuery):
    data = db.get_user_data(callback.from_user.id)
    lon = data['longitude']
    lat = data['latitude']
    weather = await get_weather(lon, lat, time=0)
    return callback.message.answer(weather)


async def get_weather(longitude, latitude, time) -> str:
    '''Return string contain information about weather'''
    #https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': API_KEY
    }
    weather = await get_api_response('https://api.openweathermap.org/data/2.5/weather/', params)
    temp = str(round(weather['main']['temp'] - 273.15, 1)) + ' °С'
    cloud = ('пасмурно' if weather['clouds']['all'] >= 80 else 'ясно')
    wind = str(round(weather['wind']['speed'], 1)) + ' м/с'
    answer = f'В городе сейчас {temp}, {cloud}, скорость ветра {wind}'
    return answer


async def get_api_response(url, params):
    '''Get all weather information from <https://api.openweathermap.org/data/2.5/weather>.
    Return dictionairy if it is successful else error code.'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                content = await response.json()
                return content
            else:
                print(f"failed to get data from {url} with error code: {response.status}")
                return None
