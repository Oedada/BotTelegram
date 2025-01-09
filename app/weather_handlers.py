from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

import aiohttp
import json
from config import API_KEY
from app.data_weather import CITIES_ENGLISH_RUSSAIN
from app.user_processor import users_db
db = users_db()

import app.keyboard as kb

from app.filters import CitiesFilter

router = Router()

@router.callback_query(CitiesFilter(F.data))
async def select_city(callback: CallbackQuery):
    db.set_user_city(str(callback.from_user.id), callback.data)
    db.save()
    await callback.message.answer(await get_weather(callback.data))


@router.callback_query(F.data == 'change_city')
async def select_city(callback: CallbackQuery):
    await callback.message.answer('Выберите свой город', reply_markup=await kb.cities_kb())


@router.message(F.text == 'Погода')
async def weather_main(message: Message):
    user_id = str(message.from_user.id)
    if user_id in db.get_registred_ids():
        city = db.get_user_data(user_id)['city']
        await message.answer(await get_weather(city), reply_markup=kb.change_city)
    else:
        await message.answer('Выберите свой город', reply_markup=await kb.cities_kb())
 
async def get_weather(city) -> str:
    weather = await get_api_response('http://api.weatherapi.com/v1/current.json'+"?key="+API_KEY+"&q="+city)
    weather = weather['current']
    temp_c = str(weather['temp_c']) + ' °С'
    cloud = ('пасмурно' if weather['cloud'] <= 80 else 'ясно')
    wind = str(round(weather['wind_kph']/3.6, 1)) + ' м/с'
    answer = f'В городе {CITIES_ENGLISH_RUSSAIN[city]} сейчас {temp_c}, {cloud}, скорость ветра {wind}'
    return answer


async def get_api_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.json()
                return content
            else:
                print(f"failed to get data from {url} with error code: {response.status}")
                return None