from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, LabeledPrice

from app.utils.create_invite_link import create_link
from app.database import requests as rq
from app.keyboards import inline

from config import config 

router = Router()


# @router.callback_query(F.data == 'channel')
# async def give_private_channel(query: CallbackQuery):
#     invite = await create_link(query.bot)
#     await rq.add_user_product(query.from_user.id, "private_channel_1")
#     await query.message.answer(f"Ваша ссылка на канал:\n\n{invite}")


@router.callback_query(inline.ProductType.filter())
async def output_product(query: CallbackQuery, callback_data: inline.ProductType):
    data = await rq.get_all_products_by_type(callback_data.name)
    text = ''

    for product in data:
        text += f'{product.name} - {product.price} UAH.\n'
    with suppress(TelegramBadRequest):   
        await query.message.edit_text(
            f"Выберите тариф:\n\n{text}",
            reply_markup=await inline.output_products(callback_data.name)
        )
    await query.answer()


@router.callback_query(inline.ProductCode.filter())
async def give_invoice(query: CallbackQuery, callback_data: inline.ProductCode, bot: Bot):
    product = await rq.get_product_by_code(callback_data.code)

    await bot.send_invoice(
        chat_id=query.from_user.id,
        title=product.name,
        description='Оплата',
        payload=product.code,
        provider_token=config.provider_token.get_secret_value(),
        currency='UAH',
        prices=[LabeledPrice(label=product.name, amount=product.price * 100)]
    )