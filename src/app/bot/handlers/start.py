from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka import FromDishka

from src.app.database.repo import UserRepo

router = Router()

@router.message(CommandStart())
async def cmd_start(
    message: Message,
    user_repo: FromDishka[UserRepo]
):
    # Добавляем пользователя в базу через репозиторий
    user = await user_repo.add_user(
        telegram_id=message.from_user.id
    )

    await message.answer(
        f"Привет! \n"
        f"Ты успешно зарегистрирован в базе под ID: {user.id}"
    )