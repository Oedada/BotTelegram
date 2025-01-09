from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.keyboard as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Здраствуйте, пожайлуста, выберите сервис.", reply_markup=kb.services)
