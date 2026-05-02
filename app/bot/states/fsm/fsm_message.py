import asyncio

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states.dice_game import DiceGame
from app.bot.utils.validators import check_number


router = Router()


@router.message(DiceGame.user_number)
async def set_number(message: Message, state: FSMContext):
    num = message.text.strip()
    error = check_number(num)
    
    if error:
        return await message.answer(error)
    
    dice_message = await message.answer_dice(emoji="🎲")
    dice_value = dice_message.dice.value
    
    await asyncio.sleep(4)

    if int(num) == dice_value:
        await message.answer("Поздравляю, вы победили 🏆!\nУ вас хорошая интуиция.")
    else:
        await message.answer("Вы не угадали число 😞.\nПовезёт в другой раз.")

    await state.clear()