import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka
from dishka import FromDishka
from redis import Redis

from src.app.bot.handlers.start import router as start_router
from src.app.bot.middlewares.auth import AuthMiddleware
from src.app.core.ioc import DbProvider, RedisProvider
import os

from src.app.database.repo import UserRepo


async def main():
    logging.basicConfig(level=logging.INFO)

    container = make_async_container(DbProvider(), RedisProvider())

    storage = await container.get(RedisStorage)

    # 1. Инициализация бота
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=storage)

    # 2. Регистрируем роутеры
    dp.include_router(start_router)

    # 3. Настраиваем Dishka
    # Интегрируем контейнер в Aiogram (магия setup_dishka)
    setup_dishka(container=container, router=dp, auto_inject=True)

    dp.update.outer_middleware(AuthMiddleware())

    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        # Не забываем закрыть контейнер при выходе
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())