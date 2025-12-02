from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    главное меню
    """
    builder = ReplyKeyboardBuilder()
    builder.button(text="Создать ТС 🚗")
    builder.button(text="Описание 📄")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)