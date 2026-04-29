from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, LabeledPrice

from app.api.services import requests as rq
from app.bot.keyboards import inline

from config import config 

router = Router()


@router.callback_query(F.data == 'back')
async def get_back(query: CallbackQuery):
    """Return to menu"""

    text = "Здравствуйте\n\n" \
           "Это тестовый бот <b>Payments</b>\n" \
           "Какие есть возможности:\n"
    await query.message.edit_text(text, reply_markup=inline.premium)


@router.callback_query(inline.ProductType.filter())
async def output_product(query: CallbackQuery, callback_data: inline.ProductType):
    """Display tariffs by product type"""

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
    """Display invoice or a message that the product has already been purchased"""

    await query.answer()
    product = await rq.get_product_by_code(callback_data.code)
    if product.type != 'channel' and product.type != 'subscription':
        check = await rq.check_product_by_user(query.from_user.id, product.code)
        if check:
            return await query.message.answer("У вас уже куплена эта функция.")

    await bot.send_invoice(
        chat_id=query.from_user.id,
        title=product.name,
        description='Оплата',
        payload=product.code,
        provider_token=config.provider_token.get_secret_value(),
        currency='UAH',
        prices=[LabeledPrice(label=product.name, amount=product.price * 100)],
    )