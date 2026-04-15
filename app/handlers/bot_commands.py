from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from app.services.bot_instance import bot

from app.keyboards import inline
from app.database import requests as rq

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    """Launching and welcoming the bot"""

    await rq.set_user(message.from_user.id, message.from_user.first_name)
    await state.clear()
    text = "Здравствуйте\n\n" \
           "Это тестовый бот <b>Payments</b>\n" \
           "Какие есть возможности:\n"
    await message.answer(text, reply_markup=inline.premium)