from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from app.data_weather import CITIES_ENGLISH


class CitiesFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text
        self.cities = CITIES_ENGLISH

    async def __call__(self, callback: CallbackQuery) -> bool:
        return (callback.data in self.cities)
