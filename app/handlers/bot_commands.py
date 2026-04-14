from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.keyboards import inline

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    """Launching and welcoming the bot"""

    await state.clear()
    text = "Здравствуйте\n\n" \
           "Это тестовый бот <b>Payments</b>\n" \
           "Какие есть возможности:\n"
    await message.answer(text, reply_markup=inline.premium)