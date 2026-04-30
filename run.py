import asyncio
import logging
from aiogram import Dispatcher, types
from app.bot.core.bot_instance import bot
from app.bot.core.http_client import create_http_client, close_http_client
from app.bot.middlewares import middlewares

from app.bot.handlers import command_router, answer_router
from app.bot.callbacks import callback_router
from app.bot.states import fsmessage_router


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

dp = Dispatcher()


async def set_commands():
    commands = [
        types.BotCommand(command='start', description='Запуск'),
        types.BotCommand(command='primelink', description='Платная функция'),
        types.BotCommand(command='game', description='Платная функция'),
        types.BotCommand(command='secretphoto', description='Платная функция'),
        types.BotCommand(command='sub_mode', description='Доступно по подписке'),
        types.BotCommand(command='profile', description='Профиль'),
    ]

    await bot.set_my_commands(commands)


async def startup():
    await create_http_client()

    for mw in middlewares:
        dp.message.middleware(mw)
        dp.callback_query.middleware(mw)

    dp.include_routers(
        command_router,
        callback_router,
        answer_router,
        fsmessage_router
    )

    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)


async def shutdown():
    await close_http_client()


async def main():
    await startup()

    await dp.start_polling(bot)
   

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped!")
    