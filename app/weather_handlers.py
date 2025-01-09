from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.filters import CitiesFilter

import aiohttp
from config import API_KEY
from app.data_weather import CITIES_ENGLISH_RUSSAIN
from app.user_processor import users_db


import app.keyboard as kb

db = users_db()
router = Router()

@router.callback_query(CitiesFilter(F.data))
async def select_city(callback: CallbackQuery):
    '''Write down data about user\'s city and sends user a message with weather'''
    db.set_user_param(str(callback.from_user.id), 'city', callback.data)
    db.save()
    await callback.message.answer(await get_weather(callback.data))


@router.callback_query(F.data == 'change_city')
async def change_city(callback: CallbackQuery):
    '''Once again sends user a message with list of cities'''
    await callback.message.answer('Выберите свой город', reply_markup=await kb.cities_kb())


@router.message(F.text == 'Погода')
async def weather_main(message: Message):
    '''Main function which distributes registered and not registered users,
    if user is registered sends him a weather message'''
    user_id = str(message.from_user.id)
    if user_id in db.get_registred_ids():
        city = db.get_user_data(user_id)['city']
        await message.answer(await get_weather(city), reply_markup=kb.change_city)
    else:
        await message.answer('Выберите свой город', reply_markup=await kb.cities_kb())


async def get_weather(city) -> str:
    '''Return string contain information about weather'''
    weather = await get_api_response('http://api.weatherapi.com/v1/current.json'+"?key="+API_KEY+"&q="+city)
    weather = weather['current']
    temp_c = str(weather['temp_c']) + ' °С'
    cloud = ('пасмурно' if weather['cloud'] <= 80 else 'ясно')
    wind = str(round(weather['wind_kph']/3.6, 1)) + ' м/с'
    answer = f'В городе {CITIES_ENGLISH_RUSSAIN[city]} сейчас {temp_c}, {cloud}, скорость ветра {wind}'
    return answer


async def get_api_response(url):
    '''Get all weather information from <http://api.weatherapi.com/>.
    Return dictionairy if it is successful else error code.'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.json()
                return content
            else:
                print(f"failed to get data from {url} with error code: {response.status}")
                return None
