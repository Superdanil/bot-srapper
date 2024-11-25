import asyncio
import logging

from aiogram import Bot, Dispatcher

from routers import unknown_command_router, support_router
from routers import wikipedia_router
from core.settings import settings


async def main():
    dp = Dispatcher()
    dp.include_routers(wikipedia_router, support_router, unknown_command_router)
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
