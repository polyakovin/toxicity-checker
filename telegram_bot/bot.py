import os
import asyncio
from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher

from handlers.text import router as text_router
from handlers.photo import router as photo_router
from handlers.barcode import router as barcode_router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(barcode_router)
    dp.include_router(photo_router)
    dp.include_router(text_router)

    logger.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
