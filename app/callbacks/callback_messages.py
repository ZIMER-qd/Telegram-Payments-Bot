from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.utils.create_invite_link import create_link
from app.database import requests as rq

router = Router()


@router.callback_query(F.data == 'channel_')
async def give_private_channel(query: CallbackQuery):
    invite = await create_link(query.bot)
    await rq.add_user_product(query.from_user.id, "private_channel_1")
    await query.message.answer(f"Ваша ссылка на канал:\n\n{invite}")