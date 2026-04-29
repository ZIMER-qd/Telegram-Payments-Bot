from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery

from app.api.services import requests as rq
from app.bot.utils.create_invite_link import create_link


router = Router()


@router.pre_checkout_query()
async def pre_chekout(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def success_payment(message: Message):
    """Giving a product to the user and recording this product in the database"""

    code = message.successful_payment.invoice_payload

    product = await rq.get_product_by_code(code)

    if product.type == 'channel':
        link = await create_link(message.bot)

        await rq.add_user_product(
            message.from_user.id,
            product.code,
            product.duration_days
        )
        await message.answer(f"Вот ссылка: {link}")
    elif product.type == 'function':
        await rq.add_user_product(
            message.from_user.id,
            product.code,
            product.duration_days
        )
    elif product.type == 'subscription':
        await rq.add_user_product(
            message.from_user.id,
            product.code,
            product.duration_days
        )