from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

premium = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить подписку", callback_data='subscription_')],
    [InlineKeyboardButton(text="Купить функции", callback_data='function_')],
    [InlineKeyboardButton(text="Доступ к каналу", callback_data='channel_')]
])