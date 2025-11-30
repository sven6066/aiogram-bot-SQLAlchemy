from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka import FromDishka, AsyncContainer
from dishka.integrations.aiogram import CONTAINER_NAME

from src.app.database.repo import UserRepo


class AuthMiddleware(BaseMiddleware):

    # def __init__(self,
    #              # user_repo: UserRepo
    #              ):
    #     self.user_repo =

    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any],
                       ) -> Any:

        container: AsyncContainer = data[CONTAINER_NAME]
#TODO понять почему не выдаёт сообщение если пользователя нет в белом списке. понять как работает data[CONTAINER_NAME]
        # 2. Получаем UserRepo из контейнера (асинхронно)
        user_repo = await container.get(UserRepo)

        user = data.get("event_from_user")

        white_list = await user_repo.get_whitelist()
        print(white_list)

        if not user or user.id not in white_list:
            bot = data.get("bot")
            if bot and hasattr(event, "from_user"):
                await bot.send_message(event.from_user.id, f"Доступ запрещён ваш id: {event.from_user.id}")
            return

        return await handler(event, data)

