import asyncio
import logging
from aiogram import Bot, Dispatcher
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from src.app.bot.handlers.start import router as start_router
from src.app.core.ioc import DbProvider
import os


async def main():
    logging.basicConfig(level=logging.INFO)

    # 1. Инициализация бота
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    # 2. Регистрируем роутеры
    dp.include_router(start_router)

    # 3. Настраиваем Dishka
    # Создаем контейнер и передаем туда наш провайдер
    container = make_async_container(DbProvider())

    # Интегрируем контейнер в Aiogram (магия setup_dishka)
    setup_dishka(container=container, router=dp, auto_inject=True)

    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        # Не забываем закрыть контейнер при выходе
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())