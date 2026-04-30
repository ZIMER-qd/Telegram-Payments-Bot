from ast import Call

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from aiogram.utils.keyboard import InlineKeyboardBuilder 
from app.api.services import requests as rq


class ProductType(CallbackData, prefix='types'):
    name: str


premium = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить подписку", callback_data=ProductType(name='subscription').pack())],
    [InlineKeyboardButton(text="Купить функции", callback_data=ProductType(name='function').pack())],
    [InlineKeyboardButton(text="Доступ к каналу", callback_data=ProductType(name='channel').pack())]
])


class ProductCode(CallbackData, prefix='subs'):
    code: str


async def output_products(type_name: str):
    products = await rq.get_all_products_by_type(type_name)
    builder = InlineKeyboardBuilder()
    
    for product in products:
        builder.button(
            text=product.name, 
            callback_data=ProductCode(code=product.code).pack()
        )
    builder.button(
        text='🔙 Назад',
        callback_data='back'
    )
    builder.adjust(1)
    return builder.as_markup()