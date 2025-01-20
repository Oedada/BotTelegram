from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import CommandStart

import aiohttp
from config import API_KEY
from app.user_processor import users_db
from datetime import datetime, timedelta
twoday = (datetime.now() + timedelta(2)).weekday()
threeday = (datetime.now() + timedelta(3)).weekday()
weekdays = {0: "Понедельник", 1:"Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресение"}

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
    db.set_user_param(message.from_user.id, 'longitude', "%.20f" % message.location.longitude)
    db.save()
    await message.answer('Ваша позиция обработана, выберите, какую погоду вы хотите получить.', reply_markup=kb.change_pos)


@router.callback_query(F.data == "weather_now")
async def weather_now(callback: CallbackQuery):
    data = db.get_user_data(str(callback.from_user.id))
    lon = data['longitude']
    lat = data['latitude']
    weather = await get_weather(lon, lat, time=0)
    return callback.message.answer(weather)


@router.callback_query(F.data == "wheather_forecast")
async def wheather_forecast(callback: CallbackQuery):
    return callback.message.answer("Выберите день", reply_markup=kb.select_day)


@router.callback_query(F.data == "tomorrow")
async def wheather_tommorow(callback: CallbackQuery):
    data = db.get_user_data(str(callback.from_user.id))
    lon = data["longitude"]
    lat = data['latitude']
    return callback.message.answer("Завтра: \n" + (await get_weather(lon, lat, 1)))


@router.callback_query(F.data == "after_tomorrow")
async def wheather_tommorow(callback: CallbackQuery):
    data = db.get_user_data(str(callback.from_user.id))
    lon = data["longitude"]
    lat = data['latitude']
    return callback.message.answer("Послезавтра: \n" + (await get_weather(lon, lat, 2)))


@router.callback_query(F.data == "aa_tomorrow")
async def wheather_tommorow(callback: CallbackQuery):
    data = db.get_user_data(str(callback.from_user.id))
    lon = data["longitude"]
    lat = data['latitude']
    return callback.message.answer(weekdays[twoday] + ":\n" + (await get_weather(lon, lat, 3)))


@router.callback_query(F.data == "aaa_tomorrow")
async def wheather_tommorow(callback: CallbackQuery):
    data = db.get_user_data(str(callback.from_user.id))
    lon = data["longitude"]
    lat = data['latitude']
    return callback.message.answer(weekdays[threeday] + ":\n" + (await get_weather(lon, lat, 4)))



async def get_weather(longitude, latitude, time) -> str:
    '''Return string contain information about weather'''
    if time == 0:
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': API_KEY
        }
        weather = await get_api_response('https://api.openweathermap.org/data/2.5/weather/', params)
        temp = str(round(weather['main']['temp'] - 273.15, 1)) + ' °С'
        cloud = ('пасмурно' if weather['clouds']['all'] >= 80 else 'ясно')
        wind = str(round(weather['wind']['speed'], 1)) + ' м/с'
        answer = f'Сейчас {temp}, {cloud}, скорость ветра {wind}'
        return answer
    else:
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': API_KEY
        }
        weathers = await get_api_response('https://pro.openweathermap.org/data/2.5/forecast', params)
        weathers = weathers["list"]
        true_weather = []
        for wheather in weathers:
            weather_time = datetime.utcfromtimestamp(wheather["dt"]).strftime('%Y-%m-%d %H:%M:%S')
            if weather_time.split(" ")[0] != datetime.now().strftime('%Y-%m-%d'):
                true_weather.append(wheather)
        weathers = true_weather
        morning = true_weather[3+(time-1)]
        noon = true_weather[5+(time-1)  ]
        evening = true_weather[7+(time-1)]
        night =  true_weather[8+(time-1)]

        temp = str(round(morning['main']['temp'] - 273.15, 1)) + ' °С'
        cloud = ('пасмурно' if morning['clouds']['all'] >= 80 else 'ясно')
        wind = str(round(morning['wind']['speed'], 1)) + ' м/с'
        morning_string = f'{temp}, {cloud}, скорость ветра {wind}'

        temp = str(round(noon['main']['temp'] - 273.15, 1)) + ' °С'
        cloud = ('пасмурно' if noon['clouds']['all'] >= 80 else 'ясно')
        wind = str(round(noon['wind']['speed'], 1)) + ' м/с'
        noon_string = f'{temp}, {cloud}, скорость ветра {wind}'

        temp = str(round(evening['main']['temp'] - 273.15, 1)) + ' °С'
        cloud = ('пасмурно' if evening['clouds']['all'] >= 80 else 'ясно')
        wind = str(round(evening['wind']['speed'], 1)) + ' м/с'
        evening_string = f'{temp}, {cloud}, скорость ветра {wind}'

        temp = str(round(night['main']['temp'] - 273.15, 1)) + ' °С'
        cloud = ('пасмурно' if night['clouds']['all'] >= 80 else 'ясно')
        wind = str(round(night['wind']['speed'], 1)) + ' м/с'
        night_string = f'{temp}, {cloud}, скорость ветра {wind}'

        answer = "Утром: " + morning_string + "\n" + "Днём: " + noon_string + "\n" + "Вечером: " + evening_string + "\n" + "Ночь: " + night_string
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
