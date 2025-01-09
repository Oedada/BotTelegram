import asyncio
import logging

import requests

from aiogram import Bot, Dispatcher
from app.handlers import router as main_router
from app.weather_handlers import router as weather_router
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()





async def main():
    dp.include_routers(main_router, weather_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")