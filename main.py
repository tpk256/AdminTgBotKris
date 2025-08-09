import asyncio
import logging


import pydotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config_reader import config
from handlers import dp as dispatcher


env = pydotenv.Environment()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = dispatcher


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())