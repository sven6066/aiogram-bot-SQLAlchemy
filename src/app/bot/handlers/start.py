from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka

from src.app.bot.dialogs.add_car import AddCar
from src.app.bot.keyboards.reply import get_main_keyboard
from src.app.database.repo import UserRepo

class Form(StatesGroup):
    name = State()
    age = State()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Добро пожаловать в бота для создания ТС в пилоте",
                         reply_markup=get_main_keyboard())

@router.message(F.text == "Создать ТС 🚗")
async def start_dialog_add_car(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddCar.choice_server, mode=StartMode.RESET_STACK)


# @router.message(CommandStart())
# async def cmd_start(
#     message: Message,
#     user_repo: FromDishka[UserRepo],
#     state: FSMContext,
# ):
#     # Добавляем пользователя в базу через репозиторий
#     user = await user_repo.add_user(
#         telegram_id=message.from_user.id
#     )
#
#     await state.set_state(Form.name)
#
#     await message.answer(
#         f"Привет! \n"
#         f"Ты успешно зарегистрирован в базе под ID: {user.id}"
#     )
#
# @router.message(Form.name)
# async def process_name(
#     message: Message,
#     state: FSMContext,
# ):
#     await state.update_data(name = message.text)
#     await message.answer("Че стало?")
#     await state.set_state(Form.age)