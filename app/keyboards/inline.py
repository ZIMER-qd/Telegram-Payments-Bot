from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import keyboards

premium = InlineKeyboardMarkup(keyboards=[
    [InlineKeyboardButton(text="Купить подписку", callback_data='subscription_')],
    [InlineKeyboardButton(text="Купить функции", callback_data='function_')],
    [InlineKeyboardButton(text="Доступ к каналу", callback_data='channel_')],
])