from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from app.services.bot_instance import bot

from app.keyboards import inline
from app.database import requests as rq

from app.states.dice_game import DiceGame
from app.utils.check_product import has_access
from app.utils import format_text as ft

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


@router.message(Command('primelink'))
async def primelink(message: Message, user_products: set):
    if not has_access(user_products, 'func_2'):
       return await message.answer("У вас нет доступа к этой функции.") 
    
    await message.answer("Prime Link:\n\n'<a href='https://a-z-animals.com/media/2024/02/GettyImages-1410187446.jpg'>Открыть изображение</a>'",
                         parse_mode='HTML')


@router.message(Command('game'))
async def game(message: Message, user_products: set, state: FSMContext):
    if not has_access(user_products, 'func_1'):
       return await message.answer("У вас нет доступа к этой функции.")
    
    await state.set_state(DiceGame.user_number)
    await message.answer("Попробуйте угадать какое число покажут кости.")



@router.message(Command('secretphoto'))
async def secretphoto(message: Message, user_products: set):
    if not has_access(user_products, 'func_3'):
       return await message.answer("У вас нет доступа к этой функции.")
    photo = FSInputFile(r'D:\All_Py_Project\Python_Project\Telegram_bots\TgBot_Payments\app\data\secretphoto.jpeg')

    await message.answer_photo(
        photo=photo,
        caption="Секретное фото"
    ) 


@router.message(Command('profile'))
async def user_profile(message: Message):
    data = await rq.get_user_purchases(message.from_user.id)
    text = ft.formatting_user_status(data)
    await message.answer(text)