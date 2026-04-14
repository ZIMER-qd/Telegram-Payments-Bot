import asyncio
import logging
from aiogram import Dispatcher, types
from app.services.bot_instance import bot


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

dp = Dispatcher()


async def set_commands():
    commands = [
        types.BotCommand(command='start', description='Запуск')
    ]

    await bot.set_my_commands(commands)


async def main():
    
    dp.include_routers()

    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
   

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped!")
    