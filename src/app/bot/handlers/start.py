from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dishka import FromDishka

from src.app.database.repo import UserRepo

class Form(StatesGroup):
    name = State()
    age = State()

router = Router()

@router.message(CommandStart())
async def cmd_start(
    message: Message,
    user_repo: FromDishka[UserRepo],
    state: FSMContext,
):
    # Добавляем пользователя в базу через репозиторий
    user = await user_repo.add_user(
        telegram_id=message.from_user.id
    )

    await state.set_state(Form.name)

    await message.answer(
        f"Привет! \n"
        f"Ты успешно зарегистрирован в базе под ID: {user.id}"
    )

@router.message(Form.name)
async def process_name(
    message: Message,
    state: FSMContext,
):
    await state.update_data(name = message.text)
    await message.answer("Че стало?")
    await state.set_state(Form.age)